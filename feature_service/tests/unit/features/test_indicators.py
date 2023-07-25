import unittest

from feature_service.features.indicators import PhiIndicatorWords
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class PhiIndicatorWordsTests(AnnotateTestsBase, MatchHintVectorizeBase):
    feature = PhiIndicatorWords()

    def test_annotate(self):
        actual = self.feature.annotate(self.TEST_INPUT_CAROLYN)

        self.assertEqual(2, self.find_match_count('FROM', actual))
        self.assertEqual(4, self.find_match_count('ON', actual))
        self.assertEqual(2, self.find_match_count('TO', actual))
        self.assertEqual(3, self.find_match_count('DATE', actual))

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(self.feature)

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(self.feature)


if __name__ == '__main__':
    unittest.main()
