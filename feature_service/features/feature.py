import enum
import re
from collections import defaultdict
from threading import Lock
from typing import (
    Dict,
    List,
    Tuple,
)

from text2phenotype.common.featureset_annotations import (
    MachineAnnotation,
    Vectorization,
)
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.feature_set.feature_set_worker import (
    FeatureSetAnnotationWorker,
    FeatureSetVectorizationWorker,
)
from feature_service.nlp.autocode import _expand_ctakes_response


class FeatureConfigName(enum.Enum):
    cancer_morphology = 'cancer-morphology'
    cancer_morphology_code = 'cancer-morphology-code'
    cancer_topography = 'cancer-topography'
    cancer_topography_code = 'cancer-topography-code'
    icd9 = 'icd9'
    icd9_code = 'icd9-code'
    icd10 = 'icd10'
    icd10_code = 'icd10-code'
    icd_syn = 'icd-syn'
    loinc_section = 'loinc-section'
    loinc_title = 'loinc-title'
    loinc_lab = 'loinc-lab'
    medgen = 'medgen'
    original = 'original'
    problem_master = 'problem-master'
    snomedct = 'snomedct'
    general = 'general'
    hepc = 'hepc'
    sectionizer = 'sectionizer'
    rxnorm = 'rxnorm'
    smoking = 'smoking'
    covid = 'covid'
    gene = 'gene'


class Feature:
    Feature_Cache = FeatureCache()
    feature_type: FeatureType = None
    vector_length: int = 0
    requires_annotation: bool = True
    config_name: FeatureConfigName = None
    annotated_feature = None

    def __init__(self):
        self._default_vector = [0] * self.vector_length
        self._zero_vector = [0] * self.vector_length

    @property
    def default_vector(self) -> List[int]:
        return self._default_vector

    @default_vector.setter
    def default_vector(self, value: list):
        if len(value) != self.vector_length:
            raise ValueError(f'New default vector must be of length {self.vector_length}')
        self._default_vector = value


    @property
    def zero_vector(self) -> List[int]:
        return self._zero_vector

    def initialize_vectors(self, token_len, width=None) -> list:
        if width is not None:
            self.default_vector(width)
        return [self.default_vector for _ in range(token_len)]

    def annotate(self, text: str, **kwargs):
        if self.requires_annotation:
            raise NotImplementedError(f'annotate method not implemented for {self.feature_type.name}.')

    @staticmethod
    def _update_data(data: dict) -> dict:
        """ Some magic from autocode for parsing FDL results """
        def __expand_umls_concepts(concepts):
            expanded = []

            for concept in concepts:
                tuis = concept.pop('tui') if concept.get('tui') else list()
                sab_concepts = concept.pop('sabConcepts') if concept.get('sabConcepts') else list()

                for sab_concept in sab_concepts:
                    vocab_concepts = sab_concept.pop('vocabConcepts') if concept.get('vocabConcepts') else dict()

                    for vocab_concept in vocab_concepts:
                        ttys = vocab_concept.pop('tty') if vocab_concept.get('tty') else list()
                        expanded_concept = vocab_concept.copy()
                        expanded_concept.update(concept)
                        expanded_concept.update(sab_concept)
                        # ensure tuis and ttys will be a list
                        if not isinstance(ttys,  list):
                            ttys = []
                        if not isinstance(tuis,  list):
                            tuis = []
                        expanded_concept['tty'] = ttys
                        expanded_concept['tui'] = tuis

                        expanded.append(expanded_concept)

            return expanded
        if 'docId' in data:
            data['docid'] = data.pop('docId')

        if 'content' in data:
            for item in data['content']:
                if 'attributes' in item:
                    if 'polarity' in item['attributes']:
                        item['attributes'].update({'relTime': ''})
            data['result'] = data.pop('content')

        for k in list(data.keys()):
            v = data[k]

            if k == 'umlsConcepts':
                data['umlsConcepts'] = __expand_umls_concepts(v)
            elif isinstance(v, dict):
                _expand_ctakes_response(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        _expand_ctakes_response(item)

        return data

    def annotated_feature_name(self) -> str:
        if self.annotated_feature is None or self.requires_annotation:
            feature_name = self.feature_type.name
        elif isinstance(self.annotated_feature, str):
            feature_name = self.annotated_feature
        elif isinstance(self.annotated_feature, FeatureType):
            feature_name = self.annotated_feature.name
        else:
            raise ValueError("No annotated feature name found")
        return feature_name

    def vectorize(self, annotated_tokens: MachineAnnotation, **kwargs):
        feature_name = self.annotated_feature_name()
        result = dict()
        feature_annotation = annotated_tokens[feature_name]
        if feature_annotation is None:
            operations_logger.warning(f'There is no annotation for feature name {feature_name}')
        elif annotated_tokens.list_feature(feature_name):
            list_annotations = annotated_tokens[feature_name]
            for i in range(len(list_annotations)):
                vector = self.vectorize_token(list_annotations[i], **kwargs)
                if vector is not None:
                    result[i] = vector
        else:
            for annotation_index, annotation in annotated_tokens[feature_name].items():
                vector = self.vectorize_token(annotation, **kwargs)
                if vector is not None:
                    result[int(annotation_index)] = vector

        return result

    def vectorize_token(self, token, **kwargs):
        raise NotImplementedError()

    def aggregate(self, annotations: list, num_tokens: int, token_ranges: List[set] = None):
        if not self.requires_annotation:
            return

        return self.aggregate_matches_direct_set(annotations, num_tokens, token_ranges)

    def get_annotation_workers(self,
                               text: str,
                               annotations: MachineAnnotation,
                               tid: str = None) -> List[FeatureSetAnnotationWorker]:
        if not self.requires_annotation:
            return []
        return [FeatureSetAnnotationWorker(self.feature_type,
                                           self.annotate,
                                           self.aggregate,
                                           text,
                                           annotations,
                                           tid=tid)]

    def get_vectorization_workers(self, tokens: MachineAnnotation, vectors: Vectorization, vectors_lock: Lock,
                                  tid: str = None) -> List[FeatureSetVectorizationWorker]:
        return [FeatureSetVectorizationWorker(self.feature_type, self.vectorize,
                                              vectors_lock=vectors_lock,
                                              vectors=vectors,
                                              tokens=tokens,
                                              tid=tid)]

    @staticmethod
    def aggregate_matches_direct_set(matches: dict, num_tokens: int = 0, token_ranges: list = None):
        output = {}
        if matches:
            for pair in matches:
                token_range = pair[0]
                annotation = pair[1]
                if token_range and token_range[1] > token_range[0]:
                    first_index = token_ranges[token_range[0]]
                    second_index = token_ranges[token_range[1] - 1]
                    if isinstance(first_index, tuple):
                        first_index = first_index[1]
                    if isinstance(second_index, tuple):
                        second_index = second_index[0]
                    if first_index <= second_index:
                        for token_index in range(first_index, second_index + 1):
                            if token_index < num_tokens:
                                if isinstance(annotation, dict):
                                    output[token_index] = annotation
                                else:
                                    if token_index not in output:
                                        output[token_index] = list()
                                    output[token_index].extend(annotation)
                else:
                    operations_logger.debug(f'Annotation range is not valid')
        return output

    def match_hints(self, text: str, curated: list, feature_name=None) -> List[Tuple]:
        """
        :param text:
        :param curated: str list of expert curated (and possibly LVG) utterances
        :param feature_name: str (optional) name of the feature
        :return:
        """
        if not feature_name:
            feature_name = self.feature_type.name
        matches = defaultdict(list)
        for candidate in curated:
            # pattern must use word boundary
            pattern = re.compile(fr'\b{candidate}\b', flags=re.MULTILINE | re.IGNORECASE)
            # headers are Uppercase
            for match in pattern.finditer(text):
                index = (match.start(), match.end())

                matches[index].append(feature_name)
        return matches.items()

    @staticmethod
    def feature_dict(sorted_keys) -> dict:
        """
        :param sorted_keys: collection of sorted(keys)
        :return: dict, entry['key'] = int(ordinal)
        """
        res = {}
        for i in range(len(sorted_keys)):
            res[sorted_keys[i]] = i
        return res

    @staticmethod
    def feature_zero(size: int) -> list:
        """
        :param size: length of vector
        :return: list vector initialized to value 0
        """
        return [0] * size
