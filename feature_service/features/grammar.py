from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class Grammar(RegExBase):
    feature_type = FeatureType.grammar
    rules = Feature.Feature_Cache.regex_grammar()
    vector_length = len(rules)
