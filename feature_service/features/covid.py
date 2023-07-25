import re

from text2phenotype.constants.features import FeatureType

from feature_service.features.clinical import Clinical
from feature_service.features.hint import MatchHint
from feature_service.features.regex import RegExBase
from feature_service.features.feature import (
    Feature,
    FeatureConfigName,
)
from feature_service.nlp import nlp_cache
from feature_service.nlp.nlp_reader import ClinicalReader


class CovidRegex(RegExBase):
    feature_type = FeatureType.regex_covid
    rules = Feature.Feature_Cache.regex_covid_rules()
    vector_length = len(rules)
    re_flags = re.IGNORECASE


class CovidDeviceRegex(RegExBase):
    feature_type = FeatureType.covid_device_regex
    rules = Feature.Feature_Cache.regex_covid_device_rules()
    vector_length = len(rules)
    re_flags = re.IGNORECASE


class CovidDeviceMatchHint(MatchHint):
    feature_type = FeatureType.covide_device_hint

    TRACH = ['trach', 'trache', 'tracheostomy', 'tracheastomy', 'endotracheal']
    TUBE = ['tube', 'tubes', 'ETT', 'ET', 'TT']
    VENT_TYPE = ['bag-mask', 'mechanical', 'mechanically']
    VENT = ['ventsuport', 'vent', 'MV', 'oscillator']

    DEFINITIONS = {
        'TRACH': TRACH,
        'TUBE': TUBE,
        'VENT_TYPE': VENT_TYPE,
        'VENT': VENT
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)


# TODO: remove once new UMLS is in the wild (2020-09-23)
class CovidRepresentation(Clinical):
    feature_type = FeatureType.covid_representation
    config_name = FeatureConfigName.covid

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.covid_repr))
