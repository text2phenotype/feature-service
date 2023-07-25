import inspect
from typing import (
    Iterable,
    Set,
)

from text2phenotype.constants.features import FeatureType

from feature_service import features
from feature_service.features.feature import Feature


FEATURE_MAP = {obj.feature_type: obj
               for name, obj in inspect.getmembers(features)
               if inspect.isclass(obj) and issubclass(obj, Feature)}


def get_annotation_features(feature_types: Iterable[FeatureType] = None) -> Set[Feature]:
    feature_set: Set[Feature] = get_features(feature_types=feature_types)

    already_viewed: Set[FeatureType] = set()
    features_for_annotation: Set[Feature] = set()

    for feature_object in feature_set:
        if not feature_object.requires_annotation:
            if feature_object.annotated_feature is not None \
                and feature_object.annotated_feature != 'token':

                feature_class = FEATURE_MAP[feature_object.annotated_feature]
                feature_object = feature_class()
            else:
                continue

        if feature_object.feature_type not in already_viewed:
            features_for_annotation.add(feature_object)
            already_viewed.add(feature_object.feature_type)

    return features_for_annotation


def get_features(feature_types: Iterable[FeatureType] = None) -> Set[Feature]:
    if not feature_types:
        feature_types = [feature_type for feature_type in FeatureType]

    feature_set: Set[Feature] = set()

    for feature_type in feature_types:
        if feature_type in FEATURES_TO_EXCLUDE_ALWAYS:
            continue

        try:
            feature_class = FEATURE_MAP[feature_type]
        except Exception:
            raise NotImplementedError(f'No such feature type: {feature_type}')

        feature = feature_class()
        feature_set.add(feature)

    return feature_set


FEATURES_TO_EXCLUDE_ALWAYS = {FeatureType.npi_binary, FeatureType.npi}
