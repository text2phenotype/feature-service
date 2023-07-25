from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint


class Predisposal(MatchHint):
    feature_type = FeatureType.predisposal

    RISK = ['risk', 'risk of', 'at risk for', 'at risk of', 'risk factors', 'risk factor', 'exposed', 'exposed to']

    DEFINITIONS = {
        'RISK': RISK
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)