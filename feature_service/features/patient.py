from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class Patient(RegExBase):
    feature_type = FeatureType.patient
    rules = Feature.Feature_Cache.regex_patient()
    vector_length = len(rules)
