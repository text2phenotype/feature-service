from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class Analyte(RegExBase):
    feature_type = FeatureType.analyte
    rules = Feature.Feature_Cache.regex_analyte()
    vector_length = len(rules)
