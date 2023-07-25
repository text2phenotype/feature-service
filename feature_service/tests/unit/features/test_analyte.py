import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.analyte import Analyte


class AnalyteTests(unittest.TestCase):
    feature = Analyte()
    text = "Pt taking 10mg of Mg.  Kind of..."

    def test_annotate(self):
        annotations = list(self.feature.annotate(self.text))

        self.assertEqual(1, len(annotations))

        self.assertTupleEqual((18, 20), annotations[0][0])

    def test_vectorize(self):
        machine_annotation = annotation.annotate_text(self.text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {4: [0, 0, 0, 1, 0, 0, 0, 0, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
