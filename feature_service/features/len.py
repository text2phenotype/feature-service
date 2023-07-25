from text2phenotype.constants.features import FeatureType
from feature_service.features.feature import Feature


class Len(Feature):
    feature_type = FeatureType.len
    vector_length = 3
    annotated_feature='token'
    requires_annotation = False

    def vectorize_token(self, token: dict, **kwargs):
        token_len = len(token)
        low = int(token_len <= 3)
        med = int(token_len in range(4, 10))
        high = int(token_len >= 10)
        vector = [low, med, high]
        return vector
