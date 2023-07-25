import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.personnel import HospitalPersonnel


class HospitalPersonnelTests(unittest.TestCase):
    feature = HospitalPersonnel()
    text = "Surgery performed by Doctors Smith and Simon"

    def test_annotate(self):
        annotations = list(self.feature.annotate(self.text))

        self.assertEqual(1, len(annotations))

        self.assertTupleEqual((21, 28), annotations[0][0])

    def test_vectorize(self):
        machine_annotation = annotation.annotate_text(self.text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {3: [0, 1, 0, 0, 0, 0, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
