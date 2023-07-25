import json
import os
from math import ceil
from typing import (
    List,
    Optional,
    Set,
)

from feature_service.resources import DOCUMENT_TYPE_VOCAB_MODEL
from text2phenotype.common import common
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType

from feature_service.feature_service_env import FeatureServiceEnv

# default train/test split for subdivisions
DEFAULT_TRAIN_TEST_SPLIT_DICT = {'train': .8, 'test': .2}

class JobMetadata:
    def __init__(self,
                 job_id: str = None,
                 feature_set_annotate: bool = False,
                 update_annotation: bool = False,
                 features: Set[FeatureType] = None,
                 annotator_disagreement: bool = False,
                 annotator_categories: List[str] = None,
                 train_doc_classifier: bool = False,
                 test_doc_classifier: bool = False,
                 doc_type_model_file_name: str = DOCUMENT_TYPE_VOCAB_MODEL,
                 api_disagreement: bool = False,
                 subdivisions: [list, dict] = DEFAULT_TRAIN_TEST_SPLIT_DICT,
                 split_fs_subdivisions: bool = False,
                 **kwargs):
        self.job_id: str = job_id
        self.feature_set_annotate: bool = feature_set_annotate
        self.update_annotation = update_annotation
        self.features: Set[FeatureType] = features if features is not None else {feature_type for feature_type in FeatureType}
        self.annotator_disagreement: bool = annotator_disagreement
        self.api_disagreement: bool = api_disagreement
        self.annotator_categories: List[str] = [a.lower() for a in annotator_categories] if annotator_categories else []
        self.train_doc_classifier: bool = train_doc_classifier
        self.test_doc_classifier: bool = test_doc_classifier
        self.doc_type_model_file_name: str = doc_type_model_file_name
        # subdivisions passed in can be a list of subfolder names to be equally weighted or a dictionary of
        # subfolder_name:weight. Weights will be normalized
        self.split_fs_subdivisions = split_fs_subdivisions
        if split_fs_subdivisions and not subdivisions:
            subdivisions = kwargs.get('feature_set_subfolders', None)
        self.subdivision = Subdivisions(subdivisions)

    @property
    def features(self) -> Optional[Set[FeatureType]]:
        return self._features

    def subdivision_split_points(self) -> dict:
        output = dict()
        start_prob = 0
        for entry in self.subdivision.subdivision_probs:
            end_prob = start_prob+self.subdivision.subdivision_probs[entry]
            output[entry] = (start_prob, end_prob)
            start_prob = end_prob
        return output

    @features.setter
    def features(self, value):
        if value:
            enum_values = set()
            for feature in value:
                if type(feature) is FeatureType:
                    enum_values.add(feature)
                elif type(feature) is str:
                    enum_values.add(FeatureType[feature.split('.')[-1]])
                elif type(feature) is int:
                    enum_values.add(FeatureType(feature))
            self._features = enum_values
        else:
            self._features = value

    def to_json(self):
        result = {'job_id': self.job_id,
                  'feature_set_annotate': self.feature_set_annotate,
                  'update_annotation': self.update_annotation,
                  'features': self.features,
                  'annotator_disagreement': self.annotator_disagreement,
                  'api_disagreement': self.api_disagreement, 'annotator_categories': self.annotator_categories,
                  'train_doc_classifier': self.train_doc_classifier,
                  'test_doc_classifier': self.test_doc_classifier,
                  'doc_type_model_file_name': self.doc_type_model_file_name,
                  'split_fs_subdivisions': self.split_fs_subdivisions,
                  'subdivisions': self.subdivision.subdivision_probs}

        return result

    def save(self):
        path = os.path.join(FeatureServiceEnv.DATA_ROOT.value, self.job_id, 'job_metadata.json')
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        return common.write_json(self.to_json(), path)

    def to_escaped_string(self):
        converted_string = json.dumps(self.to_json()).replace('"', r'\"')
        converted_string = f'"{converted_string}"'
        return converted_string


class Subdivisions:
    def __init__(self, value):
        self._subdivision_probs = None
        self.subdivision_doc_count =None
        self.subdivision_probs=value
        self.default_subdivision_probs = self._subdivision_probs

    @property
    def subdivision_split_points(self):
        output = dict()
        start_prob = 0
        for entry in self.subdivision_probs:
            end_prob = start_prob + max(0, self.subdivision_probs[entry])
            output[entry] = (start_prob, end_prob)
            start_prob = end_prob
        return output

    @property
    def subdivision_probs(self) -> dict:
        return self._subdivision_probs


    @subdivision_probs.setter
    def subdivision_probs(self, value):
        output = dict()
        if isinstance(value, list):
            for entry in value:
                output[entry] = 1 / len(value)
        elif isinstance(value, dict):
            total_sum = sum([i for i in value.values() if i > 0])
            if total_sum == 0:
                operations_logger.warning('subdivision probabilities sum to 0 this should be the last entry')

            elif total_sum != 1:
                multiplier = 1 / total_sum
                for entry in value:
                    output[entry] = value[entry] * multiplier
            else:
                output = value
        self._subdivision_probs = output

    def create_subdivision_expect_doc_count(self, doc_count):
        output = dict()
        for entry in self.default_subdivision_probs:
            output[entry] = round(self.default_subdivision_probs[entry] * doc_count, ndigits=5)
        self.subdivision_doc_count = output

    def reduce_exp_doc_count(self, entry):
        if entry not in self.subdivision_doc_count:
            raise ValueError(f'{entry} not found within subdivision doc_count dictionary')
        elif self.subdivision_doc_count[entry] > 0:
            self.subdivision_doc_count[entry] -= 1
            self.subdivision_probs = self.subdivision_doc_count
        else:
            operations_logger.warning('Trying to reduce expected remaining doc count below zero')

