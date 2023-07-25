from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint


class TimeQualifier(MatchHint):
    feature_type = FeatureType.time_qualifier

    DATE = ['date']
    START = ['start', 'onset']
    STOP = ['stop']

    DEFINITIONS = {
        'DATE': DATE,
        'START': START,
        'STOP': STOP
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
