from abc import ABC
from typing import List

from feature_service.features.feature import Feature


class BinaryFeature(Feature, ABC):
    """Feature that allows for binary vectorization."""
    vector_length = 1
    requires_annotation = False

    def __init__(self, has_polarity: bool = False):
        """Ctor."""
        super().__init__()
        self._has_polarity = has_polarity

        self._bin_vector = [0]
        if self._has_polarity:
            self._bin_vector.append(0)
            self.vector_length += 1

    @property
    def default_vector(self) -> List[int]:
        return self._bin_vector

    @property
    def zero_vector(self) -> List[int]:
        return [0] * self.vector_length
