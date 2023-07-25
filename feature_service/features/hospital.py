from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class Hospital(RegExBase):
    feature_type = FeatureType.hospital
    rules = Feature.Feature_Cache.regex_hospital()
    vector_length = len(rules)
