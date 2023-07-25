from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class Case(Feature):
    feature_type = FeatureType.case
    vector_length = 3
    annotated_feature = 'token'
    requires_annotation = False

    def vectorize_token(self, token: str, **kwargs) -> list:
        vector = None
        if token.isupper():
            vector = [1, 0, 0]
        elif token.islower():
            vector = [0, 1, 0]
        elif token.istitle():
            vector = [0, 0, 1]
        return vector
