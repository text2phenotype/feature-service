from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint

from text2phenotype.constants.features import FeatureType


class PhiIndicatorWords(MatchHint):
    feature_type = FeatureType.phi_indicator_words

    FROM = ['from']

    BY = ['by']

    ON = ['on']

    TO = ['to']

    SUBJECT = ['subject']

    DATE = ['date']

    DEFINITIONS = {
        'FROM': FROM,
        'BY': BY,
        'ON': ON,
        'TO': TO,
        'SUBJECT': SUBJECT,
        'DATE': DATE
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
