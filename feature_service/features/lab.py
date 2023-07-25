from abc import (ABC, abstractmethod)
from collections import defaultdict
from typing import List

from feature_service.features.feature import (
    Feature,
    FeatureConfigName,
)
from text2phenotype.constants.features import FeatureType

from text2phenotype.constants.umls import (
    LAB_TTY,
    LAB_VOCAB,
    Vocab)
from feature_service.features import Clinical, ClinicalBinary, ClinicalTty, ClinicalVocab
from feature_service.nlp import nlp_cache


class Lab(Clinical, ABC):
    non_vocab_len = 4
    feat_tui = []
    semantic_type = []
    feat_tty = LAB_TTY
    vocab = LAB_VOCAB
    vector_length = non_vocab_len + len(LAB_TTY) + len(LAB_VOCAB)
    pref_vocab = [Vocab.LNC.name]

    # @chunk_annotations()
    def annotate(self, text: str, fdl_data: dict = None, **kwargs):
        """
        JIRA/BIOMED-270
        """
        if fdl_data:
            data = fdl_data
            k = 'result'
        else:
            data = self._autocode(text)
            k = 'labValues'

        matches = defaultdict(list)
        for hit in data[k]:
            _text = hit['text']
            lab_index = (_text[1], _text[2])
            if text[_text[1]: _text[2]].lower() != _text[0].lower():
                # Wrong range for the text
                continue
            if len(matches[lab_index]) < 3:
                matches[lab_index].append({
                    'Lab': self.sort_concepts(hit['umlsConcept'])[0:self.MAX_CONCEPTS_TO_INCLUDE],
                    'polarity': hit['attributes'].get('polarity'),
                    'attributes': {
                        'labValue': hit['attributes'].get('labValue'),
                        'labUnit': hit['attributes'].get('labValueUnit'),
                    },
                })

            lab_value_list = hit['attributes'].get('labValue')
            if isinstance(lab_value_list, list) and len(lab_value_list) > 0:
                lab_value = lab_value_list[0]
                value_index = (lab_value_list[1], lab_value_list[2])
                if value_index not in matches:
                    matches[value_index] = [{'labValue': lab_value}]
                else:
                    matches[value_index][0]['labValue'] = lab_value
            lab_unit_list = hit['attributes'].get('labValueUnit')
            if isinstance(lab_unit_list, list) and len(lab_unit_list) > 0:
                lab_unit = lab_unit_list[0]
                unit_index = (lab_unit_list[1], lab_unit_list[2])
                if unit_index not in matches:
                    matches[unit_index] = [{'labUnit': lab_unit}]
                else:
                    matches[unit_index][0]['labUnit'] = lab_unit
        return matches.items()

    def vectorize_token(self, token, **kwargs) -> List[int]:
        """
        create feature vector for lab pipeline
        * polarity
        * lab type (CONST_UMLS)
        * lab value
        * lab value units (@anton)
        :param **kwargs:
        """

        vector = self.default_vector.copy()

        vector[0] = self._encode_polarity(token)
        tty_vect = self.vectorize_tty(token)
        vocab_vect = self.vectorize_vocab(token)

        for hit in token:
            semtype = list(hit.keys())[0]
            if 'Lab' in hit:
                vector[1] = 1
            if 'labValue' in hit:
                vector[2] = 1
            if 'labUnit' in hit:
                vector[3] = 1

        vector[self.non_vocab_len:len(LAB_VOCAB) + self.non_vocab_len] = vocab_vect
        vector[len(LAB_VOCAB) + self.non_vocab_len:] = tty_vect

        return vector

    @abstractmethod
    def _autocode(self, text: str):
        pass


class LabBinary(ClinicalBinary, ABC):
    def vectorize_token(self, token, **kwargs) -> List[int]:
        if token:
            vector = self.default_vector.copy()
            vector[1] = self._encode_polarity(token)

            for hit in token:
                if 'Lab' in hit:
                    vector[0] = 1
                    break

            return vector


class LabHepc(Lab):
    feature_type = FeatureType.lab_hepc
    config_name = FeatureConfigName.hepc

    def _autocode(self, text: str):
        return nlp_cache.hepc_lab_value(text)


class LabHepcBinary(LabBinary):
    feature_type = FeatureType.lab_hepc_binary
    annotated_feature = FeatureType.lab_hepc


class LabLoinc(Lab):
    feature_type = FeatureType.lab_loinc
    config_name = FeatureConfigName.loinc_lab

    def _autocode(self, text: str):
        return nlp_cache.loinc_lab_value(text)


class LabLoincBinary(LabBinary):
    feature_type = FeatureType.lab_loinc_binary
    annotated_feature = FeatureType.lab_loinc


class LabHepCLabWithAtttibutes(Feature):
    feature_type = FeatureType.lab_hepc_attributes
    vector_length = 2
    annotated_feature = FeatureType.lab_hepc
    requires_annotation = False

    def vectorize_token(self, token, **kwargs):
        vector = self.default_vector.copy()
        for hit in token:
            if 'Lab' in hit and 'attributes' in hit:
                if hit['attributes'].get('labValue'):
                    vector[0] = 1
                if hit['attributes'].get('labUnit'):
                    vector[1] = 1

        if sum(vector) != 0:
            return vector


class LabLoincTTY(ClinicalTty):
    feat_tty = LAB_TTY
    feature_type = FeatureType.lab_loinc_tty
    annotated_feature = FeatureType.lab_loinc
    vector_length = len(feat_tty)


class LabLoincVocab(ClinicalVocab):
    vocab = LAB_VOCAB
    feature_type = FeatureType.lab_loinc_vocab
    annotated_feature = FeatureType.lab_loinc
    vector_length = len(vocab)

class LabHepcTTY(ClinicalTty):
    feat_tty = LAB_TTY
    feature_type = FeatureType.lab_hepc_tty
    annotated_feature = FeatureType.lab_hepc
    vector_length = len(feat_tty)


class LabHepcVocab(ClinicalVocab):
    vocab = LAB_VOCAB
    feature_type = FeatureType.lab_hepc_vocab
    annotated_feature = FeatureType.lab_hepc
    vector_length = len(vocab)
