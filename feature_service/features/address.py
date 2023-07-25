from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class Address(RegExBase):
    feature_type = FeatureType.address
    rules = Feature.Feature_Cache.regex_address()
    vector_length = len(rules)
