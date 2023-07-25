import re
from text2phenotype.constants.features.feature_type import FeatureType

from feature_service.features.feature import Feature
from feature_service.features.regex import RegExBase


class ImagingRegex(RegExBase):
    feature_type = FeatureType.imaging_regex
    rules = Feature.Feature_Cache.regex_imaging_rules()
    re_flags = re.IGNORECASE
    vector_length = len(rules)