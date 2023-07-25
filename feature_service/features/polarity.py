from text2phenotype.constants.features import FeatureType
from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint


class Polarity(MatchHint):
    """
    SEE ALSO: https://github.com/mongoose54/negex/blob/master/negex.python/negex_triggers.txt
    """

    feature_type = FeatureType.polarity

    NO = ['no', 'not', 'none', 'false']
    YES = ['yes', 'true']
    POSITIVE = ['positive', 'certain', 'confirm', 'confirmed', 'affirmative', 'affirm', 'established', 'proven',
                'proved', 'reactive', 'present']
    NEGATIVE = ['negative', 'negative for', 'absent', 'fails', 'fails to', 'did not', 'nonreactive', 'non-reactive',
                'absent']

    ADMIT = ['patient admits', 'patient admits to']
    DENY = ['patient denies', 'denies', 'denied', 'denying', 'declined']

    WITHOUT = ['without', 'without evidence', 'without any evidence of', 'without indication',
               'no indications of', 'no indication of', 'no indications for', 'no indication for',
               'without sign', 'without sign of', 'insufficient']

    EVIDENCE = ['evidence']

    CHANGE = ['change', 'changes', 'changed', 'increased', 'decreased', 'worse', 'better']

    CHANGE_NO = ['no change', 'no changes', 'unchanged', 'stayed the same',
                 'did not change', 'no increase', 'no increase', 'no decrease']

    UNCERTAIN = ['uncertain', 'unknown', 'argue',
                 'contradict', 'contradicts', 'contradictory',
                 'not certain if', 'not certain of', 'not certain whether',
                 'does not recall', 'no known', 'not known', 'cannot remember',
                 'no sign', 'no new', 'no other']

    UNSPECIFIED = ['unspecified']

    RULEOUT = ['rule out', 'rules out', 'ruled out', 'ruled out for',
               'rules him out', 'rules her out', 'rules the patient out']

    RULEOUT_NO = ['not rule out', 'not be ruled out', 'cannot rule out', 'can not rule out']

    DEFINITIONS = {
        'YES': YES,
        'NO': NO,
        'POSITIVE': POSITIVE,
        'NEGATIVE': NEGATIVE,
        'ADMIT': ADMIT,
        'DENY': DENY,
        'WITHOUT': WITHOUT,
        'EVIDENCE': EVIDENCE,
        'CHANGE': CHANGE,
        'CHANGE_NO': CHANGE_NO,
        'UNCERTAIN': UNCERTAIN,
        'UNSPECIFIED': UNSPECIFIED,
        'RULE_OUT': RULEOUT,
        'RULEOUT_NO': RULEOUT_NO
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))

    vector_length = len(CONST_KEYS)
