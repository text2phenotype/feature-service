from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase

from text2phenotype.constants.features import FeatureType


class ContactInfo(RegExBase):
    feature_type = FeatureType.contact_info
    extra_feature_count = 6
    rules = Feature.Feature_Cache.regex_contact_info()
    vector_length = len(rules)
