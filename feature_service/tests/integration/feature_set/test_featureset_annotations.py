import unittest

from feature_service.feature_set.annotation import annotate_text

from text2phenotype.common.featureset_annotations import DocumentTypeAnnotation
from text2phenotype.constants.features.feature_type import FeatureType


class DocumentTypeAnnotationTests(unittest.TestCase):
    def test_ctor(self):
        text = """Admission date: 1/1/2020
Chief complaint: SOB
"""
        
        annotations = DocumentTypeAnnotation(annotate_text(text,
                                                           {FeatureType.loinc_section,
                                                            FeatureType.date_comprehension,
                                                            FeatureType.aspect_line})).to_dict()

        expected_features = {'token', 'range', 'date_comprehension', 'loinc_section', 'aspect_line'}

        self.assertSetEqual(expected_features, set(annotations.keys()))
        self.assertListEqual(['Admission date', 'Chief complaint'], annotations['token'])
        self.assertListEqual([[0, 14], [25, 40]], annotations['range'])
        self.assertEqual(0, len(annotations['date_comprehension']))
        self.assertDictEqual({0: ['encounter'], 1: ['problem']}, annotations['aspect_line'])
        self.assertSetEqual({'0', '1'}, set(annotations['loinc_section'].keys()))


if __name__ == '__main__':
    unittest.main()
