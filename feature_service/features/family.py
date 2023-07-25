from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint
from feature_service.feature_set.lvg import titlecase

from text2phenotype.constants.features import FeatureType


class Family(MatchHint):
    feature_type = FeatureType.family

    MATERNAL = titlecase(['maternal', 'mother', 'mom', 'grandmother', 'grand-mother'])
    PATERNAL = titlecase(['paternal', 'father', 'dad', 'grandfather', 'grand-father'])
    SIBLING = ['sibling', 'brother', 'sister']
    AUNT_UNCLE = ['aunt', 'uncle']
    COUSIN = ['cousin']
    CHILD = ['child', 'children', 'offspring']
    MARITAL = ['wife', 'husband']

    RELATIVES = list(set(MATERNAL + PATERNAL + SIBLING + AUNT_UNCLE + MARITAL + CHILD + COUSIN))

    DEFINITIONS = {
        'RELATIVES': RELATIVES
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
