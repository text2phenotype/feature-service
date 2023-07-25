import re
from typing import List

from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint
from feature_service.features.regex import RegExBase


class Pain(MatchHint):
    feature_type = FeatureType.pain

    # https://www.disabled-world.com/health/pain/scale.php
    PAIN_0 = ['no pain', 'without pain', 'without any pain']
    PAIN_1 = ['very mild pain', 'mild pain', 'pain', 'itch']
    PAIN_2 = ['minor pain', 'discomfort', 'discomforting', 'dull pain', 'achy', 'aches']
    PAIN_3 = ['very noticeable pain', 'noticeable pain', 'tolerable pain', 'tolerates pain', 'tolerates', 'tolerated',
              'raw pain']

    PAIN_4 = ['moderate pain', 'distressing pain', 'toothache', 'bee sting', 'minor trauma', 'distressing pain',
              'pain distressing', 'pain distress']
    PAIN_5 = ['strong pain', 'piercing pain', 'sprained ankle', 'mild back pain', 'very distressed', 'very distressing',
              'raw pain', 'pain is raw']
    PAIN_6 = ['intense pain', 'pain is intense', 'piercing pain', 'pain piercing', 'bad back pain',
              'stabbing pain', 'pain is stabbing']

    PAIN_7 = ['severe pain', 'very intense pain', 'pain is very intense', 'disabled', 'cannot live alone',
              'severe back pain', 'migraine headache', 'migraine']
    PAIN_8 = ['horrible pain', 'no longer think clearly', 'suicide']
    PAIN_9 = ['excruciating pain', 'no longer think clearly', 'cannot think clearly', 'suicide']
    PAIN_10 = ['worst pain possible', 'unimaginable pain', 'severe accident', 'lost consciousness']

    PAIN_MIN = list(set(PAIN_0 + PAIN_1 + PAIN_2 + PAIN_3))
    PAIN_MOD = list(set(PAIN_4 + PAIN_5 + PAIN_6))
    PAIN_MAX = list(set(PAIN_7 + PAIN_8 + PAIN_9 + PAIN_10))

    DEFINITIONS = {
        'PAIN_MIN': PAIN_MIN,
        'PAIN_MOD': PAIN_MOD,
        'PAIN_MAX': PAIN_MAX
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)


class Frequency(MatchHint):
    feature_type = FeatureType.frequency

    RECURRENT = ['recurrent', 'recurrence', 'recurrently']

    MULTIPLE = ['repeated', 'multiple']

    INCREASE = ['increase', 'increased']

    DECREASE = ['decrease', 'decreased']

    DEFINITIONS = {
        'RECURRENT': RECURRENT,
        'MULTIPLE': MULTIPLE,
        'INCREASE': INCREASE,
        'DECREASE': DECREASE
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)


class Severity(MatchHint):
    feature_type = FeatureType.severity

    SEVERE = ['severe', 'severity']

    ACUTE = ['acute', 'sudden', 'acute on chronic', 'rapid onset', 'worsen quickly', 'much worse']

    CHRONIC = ['chronic', 'slow onset', 'persistent']

    ILLNESS = SEVERE + ACUTE + CHRONIC

    MODERATE = ['moderate', 'moderately']

    MAXIMUM = ['max', 'maximum']
    MINIMUM = ['min', 'minimum']

    COMPLICATION = ['complication', 'complications']

    COMPLAINS = ['complaint', 'complains', 'complains of', 'complaining of', 'complained']

    PRIMARY = ['primary', 'major']
    SECONDARY = ['secondary', 'secondary to']

    DIFFICULTY = ['difficulty', 'difficulty with', 'trouble', 'trouble with', 'having trouble with']

    MILD = ['mild', 'only mild', 'subtle', 'fair', 'limited', 'minor', 'low grade', 'low-grade', 'trace', 'tolerated',
            'diffuse']

    NORMAL = ['normal']
    NORMAL_NO = ['abnormal', 'abnormality', 'abnormalities']

    IMPORTANT = ['important', 'remarkable', 'serious']
    IMPORTANT_NO = ['unimportant', 'unremarkable', 'negligible']

    SIGNIFICANT = ['significant', 'sufficient', 'remarkable']
    SIGNIFICANT_NO = ['insignificant', 'insufficient', 'insufficiency']

    # TODO: @andy refactor
    INFECTION = ['infection', 'bacteria', 'bacterial', 'virus']
    HEADACHE = ['headache', 'h/a']
    VOMIT = ['n/v', 'nausea and vomit', 'nausea', 'vomit']
    STATUS_POST = ['s/p', 'status post']
    CONSISTENT_WITH = ['c/w', 'consistent with']
    PRESENTS_WITH = ['p/w', 'presents with', 'presenting with']

    DEFINITIONS = {
        'SEVERE': SEVERE,
        'ACUTE': ACUTE,
        'CHRONIC': CHRONIC,
        'COMPLICATION': COMPLICATION,
        'DIFFICULTY': DIFFICULTY,
        'COMPLAINS': COMPLAINS,
        'MODERATE': MODERATE,
        'MAXIMUM': MAXIMUM,
        'MINIMUM': MINIMUM,
        'PRIMARY': PRIMARY,
        'SECONDARY': SECONDARY,
        'INFECTION': INFECTION,
        'MILD': MILD,
        'NORMAL': NORMAL,
        'NORMAL_NO': NORMAL_NO,
        'IMPORTANT': IMPORTANT,
        'IMPORTANT_NO': IMPORTANT_NO,
        'SIGNIFICANT': SIGNIFICANT,
        'SIGNIFICANT_NO': SIGNIFICANT_NO,

        # TODO: @andy later refactor these into separate module
        'HEADACHE': HEADACHE,
        'VOMIT': VOMIT,
        'STATUS_POST': STATUS_POST,
        'CONSISTENT_WITH': CONSISTENT_WITH,
        'PRESENTS_WITH': PRESENTS_WITH
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)


# TODO: this should probably not exist as a standalone
class TumorFocality(MatchHint):
    feature_type = FeatureType.multifocal

    # MULTIFOCAL = ['multifocal', 'multiple', 'multifocality', 'multi-focal']
    MULTIFOCAL = ['multifocal', 'multifocality', 'multi-focal']
    MULTIPLE = ['multiple']

    DEFINITIONS = {
        'MULTIFOCAL': MULTIFOCAL,
        'MULTIPLE': MULTIPLE
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS) + 1

    def vectorize_token(self, token: dict, **kwargs) -> List[int]:
        vector = super().vectorize_token(token, **kwargs)

        if any(vector):
            vector[-1] = 1

        return vector


# TODO: move to onc module?
class LVI(RegExBase):
    feature_type = FeatureType.lvi
    re_flags = re.IGNORECASE
    rules = {
        '$LVI': r'\bLVI\b',
        '$LVI_POS': r'\+LVI|LVI\+', # TODO: allow for spacing
        '$LVI_NEG': r'-LVI|LVI-',   # TODO: allow for spacing
        '$INVASION': r'invasion',
        '$LYMPH': r'lymphatic|lymphovascular'
    }
    vector_length = len(rules)
