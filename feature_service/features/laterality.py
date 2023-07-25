from text2phenotype.constants.features import FeatureType
from feature_service.features.hint import MatchHint
from feature_service.features.feature import Feature


class Laterality(MatchHint):
    feature_type = FeatureType.laterality

    LATERALITY = ['upper', 'lower', 'right', 'left', 'middle', 'middle', 'front', 'rear']

    DEFINITIONS = {
        'LATERALITY': LATERALITY
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
