from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class HospitalPersonnel(RegExBase):
    feature_type = FeatureType.hospital_personnel
    rules = Feature.Feature_Cache.regex_hospital_personnel()
    vector_length = len(rules)
