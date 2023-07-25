from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint


class FamilyHistory(MatchHint):
    feature_type = FeatureType.family_history

    FAMILY_HISTORY = ['family history', 'family history of', 'FHX']
    HEREDITY = ['ancestry', 'heredity']
    PEDIGREE = ['family tree', 'pedigree', 'pedigree chart']

    DEFINITIONS = {
        'FAMILY_HISTORY': FAMILY_HISTORY,
        'HEREDITY': HEREDITY,
        'PEDIGREE': PEDIGREE
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)


class SocialHistory(MatchHint):
    feature_type = FeatureType.social_history

    ALCOHOL = ['alcohol use history', 'admits to alcohol use', 'alcohol use', 'social alcohol drinker',
               'drinks socially', 'History of alcohol', 'heavy drinking', 'drinks']
    SOCIAL = ['social history', 'student', 'works', 'job', 'career', 'profession', 'professional']
    MARITAL = ['married', 'divorced']

    DEFINITIONS = {
        'ALCOHOL': ALCOHOL,
        'SOCIAL': SOCIAL,
        'MARITAL': MARITAL
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)


class PersonalHistory(MatchHint):
    feature_type = FeatureType.personal_history

    PERSONAL_HISTORY = ['personal history', 'personal history of', 'with history of',
                        'patient history', 'patient has history', 'patient has a history of',
                        'brief history', 'medication history', 'surgical history',
                        'history of present illness', 'HPI',
                        'past surgical history', 'past cardiac history',
                        'personal medical history', 'patient medical history',
                        'past medical history', 'PMH']

    DEFINITIONS = {
        'PERSONAL_HISTORY': PERSONAL_HISTORY
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)


class History(MatchHint):
    feature_type = FeatureType.history

    HISTORY_OF = ['history of', 'h/o', 'hx']

    DEFINITIONS = {
        'HISTORY_OF': HISTORY_OF
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)
