from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class Gender(RegExBase):
    feature_type = FeatureType.gender
    rules = Feature.Feature_Cache.regex_gender()
    vector_length = len(rules)
