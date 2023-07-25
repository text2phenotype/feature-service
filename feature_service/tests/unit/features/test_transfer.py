import unittest

from feature_service.features.transfer import Transfer
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class TransferTests(AnnotateTestsBase, MatchHintVectorizeBase):
    feature = Transfer()
    text = 'Pt discharged on 6/27.'

    def test_annotate(self):
        annotations = list(self.feature.annotate(self.text))

        self.assertEqual(1, len(annotations))
        self.assertEqual('DISCHARGED', annotations[0][1][0])

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(self.feature)

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(self.feature)


if __name__ == '__main__':
    unittest.main()
