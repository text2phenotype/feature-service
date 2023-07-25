import copy
from unittest.mock import patch

from text2phenotype.common.featureset_annotations import Vectorization
from text2phenotype.tasks.task_info import AnnotationTaskInfo
from text2phenotype.tests.fixtures import john_stevens
from text2phenotype.tests.mocks.task_testcase import TaskTestCase

from feature_service.workers.vectorization.worker import VectorizeTaskWorker


class TestVectorizeWorker(TaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.worker = VectorizeTaskWorker()
        self.chunk_task = copy.deepcopy(john_stevens.CHUNK_TASK)
        self.job_task = copy.deepcopy(john_stevens.JOB_TASK)

        self.set_initial_work_task(self.chunk_task)

        self.s3_container[john_stevens.CHUNK_TEXT_FILE_KEY] = john_stevens.EXTRACTED_TEXT_FILE.read_bytes()
        annotate_file_key = john_stevens.get_result_file_key(AnnotationTaskInfo)
        self.s3_container[annotate_file_key] = john_stevens.ANNOTATIONS_RESULT_FILE.read_bytes()

        self.fake_redis_client.set(self.chunk_task.redis_key, self.chunk_task.json())
        self.fake_redis_client.set(self.job_task.redis_key, self.job_task.json())

        fixture = Vectorization()
        fixture.fill_from_json(john_stevens.VECTORIZATION_RESULT_FILE.read_text())
        patcher = patch('feature_service.workers.vectorization.worker.vectorize_from_annotations', return_value=fixture)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_do_work(self):
        task_result = self.worker.do_work()
        self.assertIsNotNone(task_result.results_file_key)
        self.assertIsNotNone(self.s3_container.get(task_result.results_file_key))
