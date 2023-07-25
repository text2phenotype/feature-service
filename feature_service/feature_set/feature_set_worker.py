from threading import Lock
from typing import (
    Callable,
)

from text2phenotype.common.featureset_annotations import (
    MachineAnnotation,
    Vectorization,
)
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType


class FeatureSetAnnotationWorker:
    def __init__(self,
                 feature_type: str,
                 annotate_function: Callable,
                 aggregate_function: Callable,
                 text: str,
                 annotations: MachineAnnotation,
                 **kwargs):
        super().__init__()
        self.feature_type = feature_type
        self.non_locking = annotate_function
        self.aggregate = aggregate_function
        self.text = text
        self.annotations = annotations
        self.token_ranges = annotations.range_to_token_idx_list
        self.kwargs = kwargs

    def run(self):
        operations_logger.debug(f'Beginning annotation for feature: {self.feature_type}', tid=self.kwargs.get('tid'))
        individual_feature_annotations = self.non_locking(self.text, **self.kwargs)
        operations_logger.debug(f'Annotations for feature type: {self.feature_type} completed, beginning aggregation',
                                tid=self.kwargs.get('tid'))
        aggregated_annotations = self.aggregate(individual_feature_annotations, len(self.annotations),
                                                self.token_ranges)
        self.annotations.add_item(self.feature_type, aggregated_annotations)


class FeatureSetVectorizationWorker:
    def __init__(self,
                 feature: FeatureType,
                 vectorization_function: Callable,
                 vectors_lock: Lock,
                 vectors: Vectorization,
                 tokens: MachineAnnotation,
                 **kwargs):
        super().__init__()
        self.feature = feature
        self.non_locking = vectorization_function
        self.vectors_lock = vectors_lock
        self.vectors = vectors
        self.tokens = tokens
        self.kwargs = kwargs

    def run(self):
        operations_logger.debug(f'Beginning vectorization for feature {self.feature.name}', tid=self.kwargs.get('tid'))
        result = self.non_locking(self.tokens, feature_name=self.kwargs.get('feature_name'))
        operations_logger.debug(f'Vectorization for feature {self.feature.name} complete, acquiring lock',
                                tid=self.kwargs.get('tid'))
        with self.vectors_lock:
            self.vectors.add_item(self.feature.name, result)
        operations_logger.debug(f'Releasing lock for feature {self.feature.name}', tid=self.kwargs.get('tid'))
