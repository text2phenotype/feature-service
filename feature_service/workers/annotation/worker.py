import json
from typing import Iterator

from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType
from text2phenotype.tasks.rmq_worker import RMQConsumerTaskWorker
from text2phenotype.tasks.task_enums import (
    TaskEnum,
    WorkType,
)
from text2phenotype.tasks.task_info import (
    AnnotationTaskInfo,
    FDLTaskInfo,
)

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.feature_set.annotation import annotate_text


class AnnotateTaskWorker(RMQConsumerTaskWorker):
    QUEUE_NAME = FeatureServiceEnv.ANNOTATE_TASKS_QUEUE.value
    TASK_TYPE = TaskEnum.annotate
    RESULTS_FILE_EXTENSION = AnnotationTaskInfo.RESULTS_FILE_EXTENSION
    WORK_TYPE = WorkType.chunk
    NAME = 'AnnotateTaskWorker'
    ROOT_PATH = FeatureServiceEnv.root_dir

    def do_work(self) -> AnnotationTaskInfo:
        task_result: AnnotationTaskInfo = self.init_task_result()

        document_text = self.download_object_str(self.work_task.text_file_key)
        operations_logger.debug(f'Total text length: {len(document_text)}', tid=self.tid)

        job_task = self.get_job_task()

        feature_types: Iterator[FeatureType] = map(FeatureType, job_task.required_features)

        if FeatureServiceEnv.FDL_ENABLED.value:
            fdl_results_key = FDLTaskInfo.get_fdl_result_file_key(self.work_task.document_id,
                                                                  self.work_task.redis_key)
            fdl_str = self.download_object_str(fdl_results_key)
            fdl_data = json.loads(fdl_str)

            if not fdl_data:
                raise SystemError('FDL data is expected but not found in S3')

            operations_logger.info(f'FDL data downloaded for {len(fdl_data)} features', tid=self.tid)
        else:
            operations_logger.info('FDL worker is not enabled in the current environment. '
                                   'Text will be annotated in the usual way via cTakes', tid=self.tid)
            fdl_data = None

        operations_logger.debug('Beginning Annotation Task', tid=self.tid)

        annotations = annotate_text(document_text,
                                    set(feature_types),
                                    tid=self.tid,
                                    fdl_data=fdl_data)

        task_result.results_file_key = self.upload_results(annotations.to_json())

        return task_result
