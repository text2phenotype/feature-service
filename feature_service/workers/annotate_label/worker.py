import os
from typing import List, Callable

from feature_service import RESULTS_PATH
from feature_service.active.annotator_disagreement import AnnotatorDisagreement
from feature_service.active.api_disagreement import ApiDisagreement
from feature_service.common.data_source import FeatureServiceDataSource
from feature_service.document_type_vocab.document_type_vocab import DocumentTypeVocab
from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.jobs.job_metadata import JobMetadata

from text2phenotype.common.log import operations_logger
from text2phenotype.tasks.rmq_worker import RMQConsumerWorker
from text2phenotype.tasks.task_enums import TaskEnum
from text2phenotype.tasks.task_info import TaskInfo


class AnnotateLabelTaskWorker(RMQConsumerWorker):
    QUEUE_NAME = FeatureServiceEnv.LABEL_TASKS_QUEUE.value

    def __init__(self, metadata: JobMetadata):
        super().__init__()
        self.metadata: JobMetadata = metadata

    def do_work(self) -> TaskInfo:
        task_result = self.init_task_result()

        operations_logger.info('Saving job metadata')
        self.metadata.save()

        data_source = FeatureServiceDataSource(**self.metadata.__dict__)
        job_metadata = JobMetadata(**self.metadata.__dict__)
        operations_logger.info(self.metadata.__dict__)

        failed_dir = os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.metadata.job_id, 'failed_files')
        if not os.path.isdir(failed_dir):
            os.mkdir(failed_dir)

        self.__run_job(self.metadata, data_source, failed_dir, job_metadata)

        self.data_source.save(self.job_metadata.job_id)

        operations_logger.info('Saving data source json, job complete!')

        return task_result

    def __run_job(self, data_source: FeatureServiceDataSource, failed_dir: str, job_metadata: JobMetadata):
        if self.metadata.annotator_disagreement:
            self.__run_annotator_disagreement(data_source)
        elif self.metadata.api_disagreement:
            self.__run_api_disagreement(data_source)
        elif self.metadata.demographics_to_deid:
            self.__run_demo_to_deid(data_source)
        elif self.metadata.label_annotations:
            self.__label_annotations(data_source, failed_dir)
        elif self.metadata.label_annotations_blank:
            self.__add_blank_label(data_source)
        elif self.metadata.feature_set_annotate:
            self.__annotate(data_source, failed_dir, job_metadata)
        elif self.metadata.add_annotation:
            self.__add_annotation(data_source, failed_dir)
        elif self.metadata.update_annotation:
            self.__update_annotation(data_source, failed_dir)
        elif self.metadata.test_doc_classifier:
            self.__run_document_classifier(data_source, False)
        elif self.metadata.train_doc_classifier:
            self.__run_document_classifier(data_source, True)

    def __run_document_classifier(self, data_source: FeatureServiceDataSource, do_training: bool):
        doc_classifier = DocumentTypeVocab(data_source=data_source, job_id=self.metadata.job_id,
                                           model_file_name=self.metadata.doc_type_model_file_name)

        if not os.path.isdir(os.path.join(RESULTS_PATH, self.metadata.job_id)):
            os.mkdir(os.path.join(RESULTS_PATH, self.metadata.job_id))

        if do_training:
            doc_classifier.train()
            subdir = 'train'
        else:
            doc_classifier.test()
            subdir = 'test'

        data_source.sync_up(os.path.join(RESULTS_PATH, self.metadata.job_id),
                            os.path.join('models', subdir, self.metadata.job_id))

    def __run_annotator_disagreement(self, data_source: FeatureServiceDataSource):
        operations_logger.info('Creating annotator disagreement csv')
        AnnotatorDisagreement(data_source=data_source, job_metadata=self.metadata).annotator_disagreement()
        data_source.sync_up(os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.metadata.job_id),
                            os.path.join('models', 'annotator_disagreement', self.metadata.job_id))

    def __run_api_disagreement(self, data_source: FeatureServiceDataSource):
        operations_logger.info('Creating API disagreement csv')
        ApiDisagreement(data_source=data_source, job_metadata=self.metadata).disagreement()
        data_source.sync_up(os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.metadata.job_id),
                            os.path.join('reports', 'api_disagreement', self.metadata.job_id))

    def __annotate(self, data_source: FeatureServiceDataSource, failed_dir: str, job_metadata: JobMetadata):
        self.__run_annotation(data_source.feature_set_annotate, self.metadata, data_source, failed_dir,
                              job_metadata.subdivision_split_points(), job_metadata.split_fs_subdivisions)

    def __update_annotation(self, data_source: FeatureServiceDataSource, failed_dir: str):
        self.__run_annotation(data_source.update_features, self.metadata, data_source, failed_dir)

    def __run_annotation(self, annotate_fx: Callable, data_source: FeatureServiceDataSource, failed_dir: str):
        operations_logger.info('Starting feature annotation step')
        failed_files = annotate_fx(self.metadata.features)
        self.__write_failed_files(failed_files, failed_dir, self.metadata, data_source)
        operations_logger.info(f'Feature annotation step complete with {len(failed_files)} failed files')

    def __write_failed_files(self, failed_files: List[str], failed_dir: str, data_source: FeatureServiceDataSource):
        failed_files_path = os.path.join(failed_dir, 'feature_annotation_failures.txt')
        with open(failed_files_path, 'w') as failed_file:
            failed_file.writelines(failed_files)
        data_source.sync_up(failed_dir, os.path.join('annotation_reports', self.metadata.job_id))
