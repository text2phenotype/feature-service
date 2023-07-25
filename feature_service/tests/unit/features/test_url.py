import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.url import URL


class UrlTests(unittest.TestCase):
    feature = URL()
    url_text = 'The Text2phenotype website can be found at https://www.text2phenotype.com/'
    ip_text = 'The default feature IP is http://127.0.0.1:8000'

    def test_annotate_url(self):
        annotations = self.feature.annotate(self.url_text)

        self.assertEqual(4, len(annotations))

        for annotation in annotations:
            for key in annotation[1][0].keys():
                self.assertTrue(key.startswith('$URL'))

    def test_annotate_ip(self):
        annotations = self.feature.annotate(self.ip_text)

        self.assertEqual(2, len(annotations))

        for annotation in annotations:
            for key in annotation[1][0].keys():
                self.assertTrue(key == '$URL4' or key == '$IP')

    def test_vectorize_url(self):
        machine_annotation = annotation.annotate_text(self.url_text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {9: [0, 1, 1, 1, 1], 7: [0, 0, 1, 0, 0], 8: [0, 0, 1, 0, 0]}

        self.assertDictEqual(expected, observed)

    def test_vectorize_ip(self):
        machine_annotation = annotation.annotate_text(self.ip_text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {7: [1, 0, 0, 0, 1], 8: [0, 0, 0, 0, 1]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
