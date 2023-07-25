from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.tasks.task_enums import TaskEnum, WorkType
from text2phenotype.tasks.task_info import VectorizeTaskInfo
from text2phenotype.tasks.rmq_worker import RMQConsumerTaskWorker

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.feature_set.vectorization import vectorize_from_annotations


class VectorizeTaskWorker(RMQConsumerTaskWorker):
    QUEUE_NAME = FeatureServiceEnv.VECTORIZE_TASKS_QUEUE.value
    TASK_TYPE = TaskEnum.vectorize
    RESULTS_FILE_EXTENSION = VectorizeTaskInfo.RESULTS_FILE_EXTENSION
    WORK_TYPE = WorkType.chunk
    NAME = 'VectorizeTaskWorker'
    ROOT_PATH = FeatureServiceEnv.root_dir

    def do_work(self) -> VectorizeTaskInfo:
        task_result = self.init_task_result()
        tid = self.tid

        # get annotations from storage
        tokens = self.get_json_results_from_storage(TaskEnum.annotate)

        job_task = self.get_job_task()
        vectors = vectorize_from_annotations(MachineAnnotation(json_dict_input=tokens),
                                             feature_types=job_task.required_features,
                                             tid=tid)

        task_result.results_file_key = self.upload_results(vectors.to_json())

        return task_result
