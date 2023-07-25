from feature_service.features.feature import Feature
from text2phenotype.common.speech import PartOfSpeechBin
from text2phenotype.constants.features import FeatureType


class SpeechBin(Feature):
    feature_type = FeatureType.speech_bin
    vector_length = len(PartOfSpeechBin)
    annotated_feature = FeatureType.speech
    pos_bin_index = PartOfSpeechBin.get_pos_bin_dict()
    requires_annotation = False

    def vectorize_token(self, token, **kwargs):
        pos_bin: str = self.pos_bin_index.get(str(token))
        if pos_bin == 'FW-Symb':
            pos_bin = 'FW_Symb'
        if pos_bin == 'com-dep-wd':
            pos_bin = 'com_dep_wd'
        if pos_bin:
            vector = self.default_vector.copy()
            vector[list(PartOfSpeechBin.__members__.keys()).index(pos_bin)] = 1
            return vector
