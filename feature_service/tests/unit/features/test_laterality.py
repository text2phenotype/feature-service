import unittest

from text2phenotype.constants.features.feature_type import FeatureType
from feature_service.feature_set.annotation import annotate_text
from feature_service.feature_set.vectorization import vectorize_from_annotations


class LateralityTest(unittest.TestCase):
    TXT = "RIGHT lobe, left inferior nodule, middle earth, upper middle class"
    def test_annotation_vectorization(self):
        annotation = annotate_text(self.TXT, feature_types=[FeatureType.laterality])
        expected_annotation = {10: ['LATERALITY'], 0: ['LATERALITY'], 7: ['LATERALITY', 'LATERALITY'],
                    11: ['LATERALITY', 'LATERALITY'], 3: ['LATERALITY']}
        vectorization = vectorize_from_annotations(tokens=annotation, feature_types=[FeatureType.laterality])
        expected_vectors = {10: [1], 0: [1], 7: [1], 11: [1], 3: [1]}
        self.assertDictEqual(annotation[FeatureType.laterality].to_dict(), expected_annotation)
        self.assertDictEqual(vectorization[FeatureType.laterality].to_dict(), expected_vectors)
