import unittest

from text2phenotype.constants.features.feature_type import FeatureType
from feature_service.feature_set.factory import get_annotation_features

class TestBiomed1459(unittest.TestCase):
    def test_get_annotation_features(self):
        feature_types = [FeatureType.lab_hepc_attributes, FeatureType.lab_hepc, FeatureType.speech, FeatureType.word2vec_mimic]
        features = get_annotation_features(feature_types)
        self.assertEqual(len(features), 1)
        expected_feature_types = {FeatureType.lab_hepc}
        self.assertSetEqual({feat.feature_type for feat in features}, expected_feature_types)

