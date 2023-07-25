from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType
# TODO: move icd9/10 features to here?


class ICD(RegExBase):
    feature_type = FeatureType.icd
    rules = Feature.Feature_Cache.regex_icd()
    vector_length = len(rules)
