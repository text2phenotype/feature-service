from feature_service.constants import PartOfSpeechBin
from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class Speech(Feature):
    feature_type = FeatureType.speech
    vector_length = len(PartOfSpeechBin.get_pos_bin_dict())
    requires_annotation = False
    pos_bin_sorted = sorted(PartOfSpeechBin.get_pos_bin_dict().keys())

    def __init__(self):
        super().__init__()
        self.default_vector[self.pos_bin_sorted.index('NULL')] = 1

    def vectorize_token(self, token: str, **kwargs):
        if token in self.pos_bin_sorted:
            vector = self.zero_vector.copy()
            vector[self.pos_bin_sorted.index(token)] = 1
            return vector
