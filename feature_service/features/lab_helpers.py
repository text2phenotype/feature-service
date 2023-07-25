from feature_service.features.feature import Feature
from feature_service.features.hint import MatchHint
from text2phenotype.common.feature_data_parsing import probable_lab_unit
from text2phenotype.constants.features.feature_type import FeatureType

from feature_service.features.feature import Feature


class LabUnitProbable(Feature):
    annotated_feature = 'token'
    vector_length = 1
    feature_type = FeatureType.lab_unit_probable
    requires_annotation = False

    def vectorize_token(self, token: str, **kwargs):
        if probable_lab_unit(token):
            return [1]


class LabValuePhrases(MatchHint):
    feature_type = FeatureType.lab_value_phrases

    LAB_VALUE_NORMAL = ['wnl', 'within normal limits', 'w/in normal limits', 'unremarkable', 'normal']
    LAB_VALUE_ABNORMAL = ['abnormal', 'remarkable', 'elevated', 'differential', 'critical']
    LAB_VALUE_POSITIVE = ['positive', 'affirmative', 'reactive', 'detected']
    LAB_VALUE_NEGATIVE = ['negative', 'non-reactive', 'not detected']

    LAB_VALUE_DESCRIPTORS = ['level', 'count', 'rate', 'fraction', 'ratio']

    LAB_TEST_TERMS = ['profile', 'stain', 'culture', 'panel', 'screen', 'test', 'titer', 'swab']


    DEFINITIONS = {
        'LAB_VALUE_NORMAL': LAB_VALUE_NORMAL,
        'LAB_VALUE_ABNORMAL': LAB_VALUE_ABNORMAL,
        'LAB_VALUE_POSITIVE': LAB_VALUE_POSITIVE,
        'LAB_VALUE_NEGATIVE': LAB_VALUE_NEGATIVE,
        'LAB_VALUE_DESCRIPTORS': LAB_VALUE_DESCRIPTORS,
        'LAB_TEST_TERMS': LAB_TEST_TERMS
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))
    vector_length = len(CONST_KEYS)

