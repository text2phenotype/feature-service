from typing import List

from text2phenotype.constants.features import FeatureType

from feature_service.features.hint import MatchHint
from feature_service.features.feature import Feature


class RaceEthnicity(MatchHint):
    feature_type = FeatureType.race_ethnicity_regex

    WHITE = ['white', 'caucasian']
    ASIAN = ['asian']
    AFRICAN_AMERICAN = ['black', 'african', 'african american']
    HISPANIC = ['hispanic', 'latino']
    NATIVE = ['native', 'native american', 'american indian', 'alaska native']
    ISLANDER = ['hawaiian', 'pacific islander']

    DEFINITIONS = {
        'WHITE': WHITE,
        'ASIAN': ASIAN,
        'AFRICAN_AMERICAN': AFRICAN_AMERICAN,
        'HISPANIC': HISPANIC,
        'NATIVE': NATIVE,
        'ISLANDER': ISLANDER
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS) + 1

    def vectorize_token(self, token: dict, **kwargs) -> List[int]:
        vector = super().vectorize_token(token=token, **kwargs)
        # add a binary is any race vector entry
        vector[-1] = sum(vector) >= 1
        return vector