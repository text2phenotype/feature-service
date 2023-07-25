import connexion

from feature_service.feature_set.annotation import annotate_text
from feature_service.feature_set.vectorization import vectorize_from_annotations
from text2phenotype.apiclients.feature_service import FeatureRequest
from text2phenotype.common.featureset_annotations import MachineAnnotation


def annotate(feature_request: FeatureRequest = None):
    if connexion.request.is_json:
        req = FeatureRequest.from_dict(connexion.request.get_json())
    else:
        req = FeatureRequest.from_dict(feature_request)
    result = annotate_text(req.text, req.features, tid=req.tid)
    return result.to_dict()


def vectorize(feature_request: FeatureRequest = None):
    if connexion.request.is_json:
        req = FeatureRequest.from_dict(connexion.request.get_json())
    else:
        req = FeatureRequest.from_dict(feature_request)
    return vectorize_from_annotations(MachineAnnotation(json_dict_input=req.tokens), req.features,
                                      tid=req.tid).to_dict()


def annotate_vectorize(feature_request: FeatureRequest = None):
    if connexion.request.is_json:
        req = FeatureRequest.from_dict(connexion.request.get_json())
    else:
        req = FeatureRequest.from_dict(feature_request)
    annotations = annotate_text(req.text, req.features, tid=req.tid)
    vectors = vectorize_from_annotations(annotations, req.features, tid=req.tid)
    return {'annotations': annotations.to_dict(), 'vectors': vectors.to_dict()}
