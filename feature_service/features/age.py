from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class Age(RegExBase):
    feature_type = FeatureType.age
    rules = Feature.Feature_Cache.regex_age()
    vector_length = len(rules)
