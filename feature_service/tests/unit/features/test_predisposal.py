from collections import defaultdict

from feature_service.features.predisposal import Predisposal
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class PredisposalTests(AnnotateTestsBase, MatchHintVectorizeBase):
    def test_annotate(self):
        actual = Predisposal().annotate(self.TEST_INPUT_CAROLYN)

        self.assertEqual(len(actual), 4)

        counts_by_type = defaultdict(int)
        for i in actual:
            counts_by_type[i[1][0]] += 1

        self.assertEqual(counts_by_type['RISK'], 4)

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(Predisposal())

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(Predisposal())
