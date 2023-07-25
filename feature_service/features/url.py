from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class URL(RegExBase):
    feature_type = FeatureType.url
    rules = Feature.Feature_Cache.regex_url()
    vector_length = len(rules)
