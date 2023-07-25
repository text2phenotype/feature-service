import copy

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.tests.fixtures import john_stevens
from text2phenotype.tests.mocks.task_testcase import TaskTestCase

from feature_service.workers.annotation.worker import AnnotateTaskWorker


class TestAnnotationWorker(TaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.worker = AnnotateTaskWorker()
        self.chunk_task = copy.deepcopy(john_stevens.CHUNK_TASK)
        self.job_task = copy.deepcopy(john_stevens.JOB_TASK)

        self.set_initial_work_task(self.chunk_task)

        self.s3_container[john_stevens.CHUNK_TEXT_FILE_KEY] = john_stevens.EXTRACTED_TEXT_FILE.read_bytes()

        self.fake_redis_client.set(self.chunk_task.redis_key, self.chunk_task.json())
        self.fake_redis_client.set(self.job_task.redis_key, self.job_task.json())

        fixture = MachineAnnotation()
        fixture.fill_from_json(john_stevens.ANNOTATIONS_RESULT_FILE.read_text())

    def test_do_work(self):
        task_result = self.worker.do_work()
        self.assertIsNotNone(task_result.results_file_key)
        self.assertIsNotNone(self.s3_container.get(task_result.results_file_key))
