from feature_service.features.pathology_report import PathologyReport
from feature_service.tests.integration.features.annotate_tests import MatchHintVectorizeBase


class PathologyReportVectorizeTests(MatchHintVectorizeBase):
    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(PathologyReport())

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(PathologyReport())
