from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class BloodPressure(RegExBase):
    feature_type = FeatureType.blood_pressure
    rules = Feature.Feature_Cache.regex_bp()
    vector_length = len(rules)
