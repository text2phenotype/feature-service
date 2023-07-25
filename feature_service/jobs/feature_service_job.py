import os

from text2phenotype.common.log import operations_logger

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.jobs.job_metadata import JobMetadata
from feature_service.active.annotator_disagreement import AnnotatorDisagreement
from feature_service.active.api_disagreement import ApiDisagreement
from feature_service.common.data_source import FeatureServiceDataSource
from feature_service import RESULTS_PATH
from feature_service.document_type_vocab.document_type_vocab import DocumentTypeVocab


class FeatureServiceJob:
    def __init__(self, **kwargs):
        self.job_metadata = JobMetadata(**kwargs)
        operations_logger.info('Saving job metadata')
        self.job_metadata.save()
        self.data_source = FeatureServiceDataSource(**kwargs)
        operations_logger.info(self.job_metadata.__dict__)
        operations_logger.info(self.data_source.__dict__)

        failed_dir = os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.job_metadata.job_id, 'failed_files')
        if not os.path.isdir(failed_dir):
            os.mkdir(failed_dir)

        if self.job_metadata.annotator_disagreement:
            operations_logger.info('Creating annotator disagreement csv')
            ann_disagree = AnnotatorDisagreement(data_source=self.data_source, job_metadata=self.job_metadata)
            ann_disagree.annotator_disagreement()
            self.data_source.sync_up(os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.job_metadata.job_id),
                                     os.path.join('models', 'annotator_disagreement', self.job_metadata.job_id))

        if self.job_metadata.api_disagreement:
            operations_logger.info('Creating API disagreement csv')
            ApiDisagreement(data_source=self.data_source, job_metadata=self.job_metadata).disagreement()
            self.data_source.sync_up(os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.job_metadata.job_id),
                                     os.path.join('reports', 'api_disagreement', self.job_metadata.job_id))

        if self.job_metadata.feature_set_annotate or self.job_metadata.update_annotation:
            operations_logger.info('Starting feature annotation step')
            if self.job_metadata.feature_set_annotate:
                failed_files = self.data_source.feature_set_annotate(self.job_metadata.features,
                                                                     subdivisions=self.job_metadata.subdivision,
                                                                     split_data=self.job_metadata.split_fs_subdivisions)
            else:
                failed_files = self.data_source.update_features(self.job_metadata.features,
                                                                subdivisions=self.job_metadata.subdivision,
                                                                split_data=self.job_metadata.split_fs_subdivisions)

            self.write_failed_files(failed_files, failed_dir)
            operations_logger.info(f'Feature annotation step complete with {len(failed_files)} failed files')

        if self.job_metadata.test_doc_classifier or self.job_metadata.train_doc_classifier:
            doc_classifier = DocumentTypeVocab(data_source=self.data_source,
                                               job_id=self.job_metadata.job_id,
                                               model_file_name=self.job_metadata.doc_type_model_file_name)
            if not os.path.isdir(os.path.join(RESULTS_PATH,  self.job_metadata.job_id)):
                os.mkdir(os.path.join(RESULTS_PATH,  self.job_metadata.job_id))
            if self.job_metadata.train_doc_classifier:
                doc_classifier.train()
                self.data_source.sync_up(os.path.join(RESULTS_PATH, self.job_metadata.job_id),
                                         os.path.join('models', 'train', self.job_metadata.job_id))
            if self.job_metadata.test_doc_classifier:
                doc_classifier.test()
                self.data_source.sync_up(os.path.join(RESULTS_PATH, self.job_metadata.job_id),
                                         os.path.join('models', 'test', self.job_metadata.job_id))


        self.data_source.save(self.job_metadata.job_id)
        operations_logger.info('Saving data source json, job complete!')

    def write_failed_files(self, failed_files, failed_dir):
        failed_files_path = os.path.join(failed_dir, 'feature_annotation_failures.txt')
        with open(failed_files_path, 'w') as failed_file:
            failed_file.writelines(failed_files)
        self.data_source.sync_up(failed_dir, os.path.join('annotation_reports', self.job_metadata.job_id))
