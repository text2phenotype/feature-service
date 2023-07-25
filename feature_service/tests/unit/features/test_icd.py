import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.icd import ICD


class ICDTests(unittest.TestCase):
    feature = ICD()

    def test_annotate_full(self):
        text = 'Pt complains of abdominal pain (ICD-789.0)'

        annotations = list(self.feature.annotate(text))

        self.assertEqual(3, len(annotations))

        self.assertEqual('$ICD-9_1', next(iter(annotations[0][1][0].keys())))
        self.assertEqual('$ICD-9_2', next(iter(annotations[1][1][0].keys())))
        self.assertEqual('$ICD', next(iter(annotations[2][1][0].keys())))

    def test_vectorize(self):
        text = 'Pt complains of abdominal pain (ICD10-R10.0)'

        machine_annotation = annotation.annotate_text(text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {6: [1, 1, 1, 0, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
