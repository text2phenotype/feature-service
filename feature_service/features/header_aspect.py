from text2phenotype.ccda.section import Aspect
from text2phenotype.constants.features import FeatureType

from feature_service.features.feature import Feature


class HeaderAspect(Feature):
    feature_type = FeatureType.header_aspect
    vector_length = len(Aspect)
    annotated_feature = FeatureType.header
    requires_annotation = False

    def vectorize_token(self, token: dict, **kwargs):
        vector = self.default_vector.copy()
        for hit in token:
            aspect = list(hit.values())[0][7:]
            vector[Aspect[aspect].value] = 1
        return vector
