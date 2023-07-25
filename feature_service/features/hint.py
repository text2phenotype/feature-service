from typing import List

from feature_service.features.binary_feature import BinaryFeature
from feature_service.features.feature import Feature


class MatchHint(Feature):
    ####################
    # NOTE: set feature_type to your FeatureType.feature_name
    # Example: FeatureType.polarity
    feature_type = None

    def annotate(self, text: str, **kwargs):
        matches = list()
        for feature_name in self.DEFINITIONS.keys():
            token_list = self.DEFINITIONS[feature_name]
            matches.extend(self.match_hints(text, token_list, feature_name))
        return matches

    def vectorize_token(self, token: dict, **kwargs) -> List[int]:
        vector = self.default_vector.copy()
        token = set(token)
        for key in self.CONST_KEYS:
            if key in token:
                vector[self.CONST_KEYS[key]] = 1
        return vector


    ################################################################################
    # DEFINITIONS: dict with format {key1 : list1, key2:list2}
    #
    # TODO: @andymc refactor MatchHints with examples
    #
    DEFINITIONS = {
        'KEY1': ['longer phrase to match first', 'shortest phrase to match last'],
        'KEY2': ['example', 'documentation'],
    }

    CONST_KEYS = Feature.feature_dict(sorted(list(DEFINITIONS.keys())))

    vector_length = len(CONST_KEYS)


class MatchHintBinary(MatchHint, BinaryFeature):
    ####################
    # NOTE: set feature_type to your FeatureType.feature_name
    # Example: FeatureType.polarity
    feature_type = None

    def vectorize_token(self, token: dict, **kwargs) -> List[int]:
        vector = self.default_vector.copy()
        for key in self.CONST_KEYS:
            if key in token:
                vector[0] = 1

                return vector
