from collections import defaultdict
import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features import CovidDeviceRegex, CovidDeviceMatchHint
from feature_service.tests.integration.features.annotate_tests import MatchHintVectorizeBase

record_text = 'Pt was put on mechanical ventilator for 96 hrs.'


class TestCovideDeviceRegex(unittest.TestCase):
    def test_annotate(self):
        annotations = list(CovidDeviceRegex().annotate(record_text))

        span, _ = annotations[0]

        self.assertTupleEqual((25, 35), span)

    def test_vectorize(self):
        feature = CovidDeviceRegex()

        machine_annotation = annotation.annotate_text(record_text, feature_types=[feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[feature.feature_type])

        observed = vectors.output_dict[feature.feature_type].input_dict

        expected = {5: [1]}

        self.assertDictEqual(expected, observed)


class TestCovidDeviceMatchHint(MatchHintVectorizeBase):
    def test_annotate(self):
        actual = CovidDeviceMatchHint().annotate(record_text)

        self.assertEqual(len(actual), 1)

        counts_by_type = defaultdict(int)
        for i in actual:
            counts_by_type[i[1][0]] += 1

        self.assertEqual(counts_by_type['VENT_TYPE'], 1)

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(CovidDeviceMatchHint())

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(CovidDeviceMatchHint())


if __name__ == '__main__':
    unittest.main()
