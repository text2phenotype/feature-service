import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.hospital import Hospital
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class HospitalTests(AnnotateTestsBase, MatchHintVectorizeBase):
    feature = Hospital()

    def test_annotate(self):
        actual = self.feature.annotate(self.TEST_INPUT_CAROLYN)

        self.assertTrue(self.find_match('$HOSPITAL_1', actual))

    def test_vectorize(self):
        text = 'Pt transferred from CU Medical Center'

        machine_annotation = annotation.annotate_text(text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {4: [0, 1], 5: [1, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
