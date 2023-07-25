import inspect
import unittest

from feature_service import features
from feature_service.feature_set import factory
from feature_service.features.binary_feature import BinaryFeature
from feature_service.features.feature import Feature

from text2phenotype.constants.features import FeatureType


class TestFactory(unittest.TestCase):
    def test_get_features_default(self):
        feature_map = {}

        # make sure multiple features not mapping to the same feature type
        for obj in inspect.getmembers(features):
            if not (inspect.isclass(obj) and issubclass(obj, Feature)):
                continue

            self.assertNotIn(obj.feature_type, feature_map,
                             msg=f'Feature type {obj.feature_type} already exists in feature map.')

            feature_map[obj.feature_type] = obj

    def test_get_features_with_feature_list(self):
        feature_types = [FeatureType.clinical, FeatureType.morphology, FeatureType.case]

        features = factory.get_features(feature_types)

        self.assertEqual(len(feature_types), len(features))
        for feature in features:
            self.assertIn(feature.feature_type, feature_types,
                          msg=f'Feature {feature.feature_type} should not be in feature set.')


if __name__ == '__main__':
    unittest.main()
