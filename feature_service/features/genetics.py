from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint

from text2phenotype.constants.features.feature_type import FeatureType


class GenticTestInterpretation(MatchHint):
    feature_type = FeatureType.genetic_test_interpretation

    POSITIVE = ['positive', 'pos', '\+\s?']
    NEGATIVE = ['negative', 'neg', 'not present', '-\s?']
    WILD_TYPE = ['wild type', 'wild-type', 'WT']
    VUS = ['VUS']
    MUTATED = ['mutant', 'mutants', 'mutation', 'mutational', 'mutated', 'mutations']

    DEFINITIONS = {
        'POSITIVE': POSITIVE,
        'NEGATIVE': NEGATIVE,
        'WILD_TYPE': WILD_TYPE,
        'VUS': VUS,
        'MUTATED': MUTATED
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
