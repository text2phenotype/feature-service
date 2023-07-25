from collections import defaultdict

from feature_service.features import Severity, Pain, Frequency
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class SeverityTests(AnnotateTestsBase, MatchHintVectorizeBase):
    def test_annotate(self):
        actual = Severity().annotate(self.TEST_INPUT_CAROLYN)

        self.assertEqual(len(actual), 27)

        counts_by_type = defaultdict(int)
        for i in actual:
            counts_by_type[i[1][0]] += 1
        # there should be 5 hits for severe

        self.assertEqual(counts_by_type['SEVERE'], 5)
        self.assertEqual(counts_by_type['ACUTE'], 1)
        self.assertEqual(counts_by_type['CHRONIC'], 1)
        self.assertEqual(counts_by_type['COMPLAINS'], 2)
        self.assertEqual(counts_by_type['MINIMUM'], 2)
        self.assertEqual(counts_by_type['PRIMARY'], 2)
        self.assertEqual(counts_by_type['SECONDARY'], 1)
        self.assertEqual(counts_by_type['MILD'], 4)
        self.assertEqual(counts_by_type['NORMAL'], 5)
        self.assertEqual(counts_by_type['SIGNIFICANT'], 1)
        self.assertEqual(counts_by_type['SIGNIFICANT_NO'], 2)
        self.assertEqual(counts_by_type['VOMIT'], 1)

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(Severity())

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(Severity())


class PainTests(MatchHintVectorizeBase, AnnotateTestsBase):
    def test_annotate(self):
        actual = Pain().annotate(self.TEST_INPUT_CAROLYN)

        self.assertEqual(len(actual), 2)

        counts_by_type = defaultdict(int)
        for i in actual:
            counts_by_type[i[1][0]] += 1

        self.assertEqual(counts_by_type['PAIN_MIN'], 2)

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(Pain())

    def test_vectorize_min(self):
        self._test_vectorize('achy', Pain(), [Pain.CONST_KEYS['PAIN_MIN']])

    def test_vectorize_mod(self):
        self._test_vectorize('sprained ankle', Pain(), [Pain.CONST_KEYS['PAIN_MOD']])

    def test_vectorize_max(self):
        self._test_vectorize('suicide', Pain(), [Pain.CONST_KEYS['PAIN_MAX']])


class FrequencyTests(AnnotateTestsBase, MatchHintVectorizeBase):
    def test_annotate(self):
        actual = Frequency().annotate(self.TEST_INPUT_CAROLYN)

        self.assertEqual(len(actual), 1)

        counts_by_type = defaultdict(int)
        for i in actual:
            counts_by_type[i[1][0]] += 1

        self.assertEqual(counts_by_type['RECURRENT'], 1)

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(Frequency())

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(Frequency())
