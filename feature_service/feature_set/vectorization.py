from threading import Lock
from typing import (
    List,
    Set,
)

from text2phenotype.apm.metrics import text2phenotype_capture_span
from text2phenotype.common.featureset_annotations import MachineAnnotation, Vectorization, DefaultVectors
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.annotation import run_thread_list
from feature_service.feature_set.factory import get_features
from feature_service.features.feature import Feature


@text2phenotype_capture_span()
def vectorize_from_annotations(tokens: MachineAnnotation,
                               feature_types: Set[FeatureType] = None,
                               tid: str = None) -> Vectorization:
    """
    :param tokens: list of token dictionary,
    :param binary_classifier: whether we want to train a binary classifier or multi-class
    :param feature_types: the features to vectorize
    :param tid: transaction id
    """
    if not tokens.to_dict():
        return Vectorization()

    operations_logger.debug('Beginning Vectorization Task', tid=tid)
    features = get_features(feature_types)

    vectors_lock = Lock()

    vectors = Vectorization(default_vectors=feature_information_required_for_matrix(features))

    thread_list = []

    for feature in features:
        workers = feature.get_vectorization_workers(tokens=tokens, vectors=vectors, vectors_lock=vectors_lock, tid=tid)
        for worker in workers:
            thread_list.append(worker)

    run_thread_list(thread_list,  tid=tid)

    operations_logger.debug('Vectorization Task Complete', tid=tid)
    return vectors


def feature_information_required_for_matrix(features: List[Feature]) -> DefaultVectors:
    output = dict()
    for feat in features:
        output[feat.feature_type.name] = feat.default_vector
    return DefaultVectors(output)

