import json

from feature_service.constants import SmokingStatus
from feature_service.features.feature import (
    Feature,
    FeatureConfigName,
)
from feature_service.features.hint import MatchHint
from feature_service.features.regex import RegExBase
from feature_service.nlp import nlp_cache
from text2phenotype.common.log import operations_logger

from text2phenotype.constants.features import FeatureType


class Smoking(Feature):
    NLP_KEY = 'smokingStatus'
    feature_type = FeatureType.smoking
    vector_length = len(SmokingStatus)
    config_name = FeatureConfigName.smoking

    # @chunk_annotations()
    def annotate(self, text: str, fdl_data: dict = None, **kwargs):
        if fdl_data:
            operations_logger.debug(f'Using FDL results for the '
                                    f'feature - {self.feature_type.value}, '
                                    f'config - {self.config_name.value}')
            data = self._update_data(fdl_data)
            text_key = 'Text'
            status_key = 'Status'
        else:
            data = nlp_cache.smoking(text)
            text_key = 'text'
            status_key = 'status'

        annotations = []

        for sentence in data['sentences']:
            text_info = sentence[text_key]

            annotations.append(((int(text_info[1]), int(text_info[2])),  [SmokingStatus[sentence[status_key]].name]))

        return annotations

    def vectorize_token(self, token, **kwargs):
        vector = self.default_vector.copy()
        vector[SmokingStatus[token[0]].value] = 1

        return vector


class SmokingKeywords(MatchHint):
    feature_type = FeatureType.smoking_keywords

    DEFINITIONS = {
        'CIGARETTE': ['cig', 'cigs', 'cigarette', 'cigarettes'],
        'CIGAR': ['cigar', 'cigars'],
        'SMOKER': ['smoker', 'smokes'],
        'SMOKING': ['smoking'],
        'TOBACCO': ['tobacco', 'tobaccos', 'tob'],
        'FORMER_SMOKER': ['smoked', 'distant', 'former'],
        'NICOTINE': ['nicotine'],
        'CURRENT_SMOKER': ['current', 'cessation', 'continues', 'active'],
        'AMOUNT': ['pack', 'packs', 'per', 'day', 'month', 'ppd', 'year'],
        'DURATION': ['yrs', 'years', 'py', 'year', 'pack']
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))

    vector_length = len(CONST_KEYS)


class SmokingRegex(RegExBase):
    feature_type = FeatureType.smoking_regex
    re_flags = 0
    rules = RegExBase.Feature_Cache.regex_smoking()
    vector_length = len(rules)
