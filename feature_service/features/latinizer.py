from typing import List

from feature_service.features.feature import Feature
from text2phenotype.constants.features import FeatureType

from feature_service.common.latin import (
    Latin,
    LatinTypes,
)
from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.features.binary_feature import BinaryFeature


class Latinizer(Feature):
    feature_type = FeatureType.latinizer
    vector_length = len(LatinTypes)+2
    annotated_feature = 'token'
    requires_annotation = False

    def vectorize_token(self, token, **kwargs) -> List[int]:
        """onehot encoding of annotated token (list of binary)"""
        latin_list = FeatureCache().latin_resources()

        matches = self.match_all(token, latin_list)
        if matches:
            vector = self.default_vector.copy()
            for match in matches:
                if match.is_prefix():
                    vector[0] = 1
                if match.is_suffix():
                    vector[1] = 1
                vector[LatinTypes[match.ftr.lower()].value+2] = 1

            return vector

    @staticmethod
    def match_all(token, sorted_list: List[Latin]) -> List[Latin]:
        matches = []
        for entry in sorted_list:
            if entry.relax(token):
                matches.append(entry)
        return matches


class LatinizerBinary(BinaryFeature):
    feature_type = FeatureType.latinizer_binary
    annotated_feature = 'token'

    def vectorize_token(self, token, **kwargs) -> List[int]:
        if Latinizer.match_all(token, FeatureCache().latin_resources()):
            return [1]
