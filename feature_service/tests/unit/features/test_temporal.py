from feature_service.features.temporal import TimeQualifier
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class TimeQualifierTests(AnnotateTestsBase, MatchHintVectorizeBase):
    def test_annotate(self):
        actual = TimeQualifier().annotate(self.TEST_INPUT_CAROLYN)

        self.assertTrue(self.find_polarity_type_match('DATE', actual, 'DATE'))

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(TimeQualifier())

    def test_vectorize(self):
        self._test_vectorize_all_definitions(TimeQualifier())
