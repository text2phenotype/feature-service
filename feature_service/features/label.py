from abc import ABC
from enum import Enum

from feature_service.features.feature import Feature


class _LabelFeature(Feature, ABC):
    labelEnum: Enum = None
    requires_annotation = False

    def __init__(self, binary_classifier=False):
        if binary_classifier:
            self.vector_length = 2
        else:
            self.vector_length = len(self.labelEnum)
        super().__init__()

        self.default_vector[0] = 1
        self.binary_classifier = binary_classifier

    def feature_zero(self, size: int = None) -> list:
        if size is None:
            size = len(self.labelEnum.__members__)
        return super().feature_zero(size)

    def vectorize_token(self, token: dict, **kwargs):
        vector = self.zero_vector.copy()
        if self.binary_classifier:
            vector[1] = 1
        else:
            vector[self.labelEnum.from_brat(token[0]).value.column_index] = 1
        return vector
