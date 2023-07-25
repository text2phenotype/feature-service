import unittest

from feature_service.feature_set.factory import get_features
from feature_service.feature_set.vectorization import feature_information_required_for_matrix

class TestBiomed1352(unittest.TestCase):
    def test_default_vector_all_features(self):
        features = get_features()
        actual_output = feature_information_required_for_matrix(features)

        # test all default vectors are as expected in the output and of len vector length
        for feat in features:
            self.assertEqual(feat.default_vector, actual_output[feat.feature_type.name])
            self.assertEqual(len(actual_output[feat.feature_type.name]), feat.vector_length)
