from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint

from text2phenotype.constants.features import FeatureType


class Transfer(MatchHint):
    feature_type = FeatureType.transfer

    DISCHARGED = ['discharged']

    DEFINITIONS = {
        'DISCHARGED': DISCHARGED
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
