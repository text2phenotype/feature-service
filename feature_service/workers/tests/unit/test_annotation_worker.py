import unittest
from unittest import mock

from text2phenotype.tasks.document_info import DocumentInfo
from text2phenotype.tasks.framework import TasksConstants
from text2phenotype_tasks.workers import AnnotateTaskWorker


class TestAnnotationWorkerTokenize(unittest.TestCase):

    @mock.patch("workers.annotation.annotation_worker.annotate_text")
    @mock.patch("workers.annotation.annotation_worker.BioMedClient")
    @mock.patch("workers.annotation.annotation_worker.get_storage_service")
    def test_annotation_worker_success(self, mock_storage_service, mock_biomed, mock_annotate):
        """ Base case testing the result when a successful call """

        mock_annotate.return_value = {"some annotation": "some value"}

        document_info = DocumentInfo("doc id")
        document_info.text_file_key = "source_document.txt"
        document_info.version = "1.0"

        target = AnnotateTaskWorker()
        target.init_document(document_info, {"task operations": [1]})

        result = target.do_work()

        # in the end, we should have success
        self.assertTrue(result.success)

        # verify biomed call to get features from the operations
        mock_biomed.return_value.get_required_features.assert_called()

        # verify the results file was uploaded to storage
        self.assertEqual(result.results_information["annotation file"],
                         f"{TasksConstants.RESULTS_FOLDER}/1.0/{TasksConstants.ANNOTATE_FOLDER_NAME}"
                         f"/source_document.ann.json")

    @mock.patch("workers.annotation.annotation_worker.annotate_text")
    @mock.patch("workers.annotation.annotation_worker.BioMedClient")
    @mock.patch("workers.annotation.annotation_worker.get_storage_service")
    def test_annotation_worker_storage_fail(self, mock_storage_service, mock_biomed, mock_annotate):
        """ Test failure when initializing storage """

        mock_storage_service.side_effect = IOError("some io error")

        document_info = DocumentInfo("doc id")
        document_info.text_file_key = "source_document.txt"
        document_info.version = "1.0"

        target = AnnotateTaskWorker()
        target.init_document(document_info, {"task operations": [1]})

        result = target.do_work()

        # in the end, we should not have success
        self.assertFalse(result.success)


