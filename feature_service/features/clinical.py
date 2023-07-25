from abc import ABC
from collections import defaultdict
from typing import List

from feature_service.feature_set import umls
from feature_service.features.binary_feature import BinaryFeature
from feature_service.features.feature import (
    Feature,
    FeatureConfigName,
)
from feature_service.nlp import nlp_cache
from feature_service.nlp.nlp_reader import ClinicalReader
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType
from text2phenotype.constants.umls import (
    DIAGNOSIS_TTY,
    PROBLEM_TTY,
    PROBLEM_TUI,
    SemTypeCtakesAsserted,
    TTY,
    TUI,
    Vocab,
)


class Clinical(Feature, ABC):
    non_vocab_vect_len = 3
    vocab = Vocab
    feat_tui = TUI
    feat_tty = TTY
    feature_type = FeatureType.clinical
    semantic_type = SemTypeCtakesAsserted
    vector_length = (non_vocab_vect_len + len(semantic_type) + len(vocab) + len(feat_tty) + len(feat_tui))
    pref_vocab = [Vocab.SNOMEDCT_US.name]
    pref_tty: set = {PROBLEM_TTY.PT.name, PROBLEM_TTY.FN.name, None}
    MAX_CONCEPTS_TO_INCLUDE = 4
    SNOMED_ALTS = {'snomedct', 'SNOMEDCT'}
    config_name = FeatureConfigName.original

    def __init__(self, reader: ClinicalReader = None):
        super().__init__()
        self.reader = reader if reader else ClinicalReader()

    # @chunk_annotations()
    def annotate(self, text: str, fdl_data: dict = None, **kwargs):
        if fdl_data:
            operations_logger.debug(f'Using FDL results for the '
                                    f'feature - {self.feature_type.value}, '
                                    f'config - {self.config_name.value}')
            self.reader.from_json(fdl_data)
        else:
            self.reader.autocode(text)

        matches = defaultdict(list)
        for hit in self.reader.list_results():
            if text[hit.match.start:hit.match.stop].lower() != hit.match.text.lower():
                # Wrong range for the text
                continue
            matches[(hit.match.start, hit.match.stop)].append({
                hit.semantic_type: hit.concepts.to_json(),
                'polarity': hit.attributes.polarity,
            })
        for key, value in matches.items():
            for r in range(len(value)):
                for sem_type in value[r]:
                    if sem_type != 'polarity':
                        matches[key][r][sem_type] = self.sort_concepts(value[r][sem_type])[0:2]

        return list(matches.items())

    def sort_concepts(self, concept_list):
        # there are 4 groups a concept can be in, both from the preferred vocab and preferred term type,
        # pref vocab only, tty only or neither. We will rank them in the order above
        both_pref, vocab_pref, tty_pref, no_pref = [], [], [], []
        for concept in concept_list:
            pref_vocab = concept.get('codingScheme') in self.pref_vocab
            pref_tty = set(concept.get('tty', [])).intersection(self.pref_tty)
            if pref_vocab and pref_tty:
                both_pref.append(concept)
            elif pref_vocab:
                vocab_pref.append(concept)
            elif pref_tty:
                tty_pref.append(concept)
            else:
                no_pref.append(concept)
        ordered_concept_list = both_pref + vocab_pref + tty_pref + no_pref
        return ordered_concept_list

    def vectorize_sab_vocab(self, vocab_iter: list) -> list:
        """
        :param vocab_iter: list of vocab names like ['NCI','NDFRT','RXNORM','SNOMEDCT']
        :return: [0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 0, 0, 0 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0,0]
        """
        return umls.vectorize(umls.match_vocab(self.vocab, vocab_iter))

    def vectorize_tui_semtype(self, tui_iter: list) -> list:
        """
        :param tui_iter: list of 'tui' matches like ['T019','T203']
        :return: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        """
        return umls.vectorize(umls.match_tui(self.feat_tui, tui_iter))

    def vectorize_tty_termtype(self, tty_iter: list) -> list:
        """
        :param tty_iter: list of 'tty' matches like ['PT','SY'] for Preferred Term and Synonym
        :return: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        """
        return umls.vectorize(umls.match_termtype(self.feat_tty, tty_iter))

    @staticmethod
    def _encode_polarity(token) -> int:
        return 1 if token[0].get('polarity') == 'positive' else 0

    @staticmethod
    def _is_acceptable_hit(hit) -> bool:
        keys = list(hit.keys())
        semtype = keys[0]

        is_acceptable = semtype in SemTypeCtakesAsserted.__members__
        if not is_acceptable:
            operations_logger.debug(f'Invalid semtype {semtype}; ({keys})')

        return is_acceptable

    def vectorize_vocab(self, token: list):
        vocab_set = set()

        if isinstance(token, list):
            for hit in token:
                if not self._is_acceptable_hit(hit):
                    continue
                semtype = list(hit.keys())[0]

                for concept in hit[semtype]:
                    vocab = concept.get('codingScheme', None)

                    if vocab in self.SNOMED_ALTS:
                        vocab = 'SNOMEDCT_US'

                    if vocab:
                        vocab_set.add(vocab.upper())
        return self.vectorize_sab_vocab(list(vocab_set))

    def vectorize_tui(self, token: list):
        tui_set = set()
        if isinstance(token, list):
            for hit in token:
                if not self._is_acceptable_hit(hit):
                    continue
                semtype = list(hit.keys())[0]

                for concept in hit[semtype]:
                    tui = concept.get('tui', None)
                    if tui:
                        tui_set.update(set(tui))
        return self.vectorize_tui_semtype(list(tui_set))

    def vectorize_tty(self, token: list):
        tty_set = set()
        if isinstance(token, list):
            for hit in token:
                if not self._is_acceptable_hit(hit):
                    continue
                semtype = list(hit.keys())[0]

                for concept in hit[semtype]:
                    tty = concept.get('tty', None)
                    if tty:
                        tty_set.update(set(tty))
        return self.vectorize_tty_termtype(list(tty_set))

    def vectorize_sem_types(self, token: list):
        vector = [0] * len(SemTypeCtakesAsserted)
        if isinstance(token, list):
            for hit in token:
                if not self._is_acceptable_hit(hit):
                    continue
                semtype = list(hit.keys())[0]
                vector[SemTypeCtakesAsserted[semtype].value] = 1
        return vector

    def vectorize_token(self, token: list, **kwargs) -> List[int]:
        """
        JIRA/BIOMED-199
        create feature vector for the clinical pipeline output
        * polarity
        * count vocabs (?)
        * count concepts (?)
        * umls type (CONST_UMLS)
        * dictionary vector
        ["CPT”,“ICD10”,“ICD9",“ICD9CM”,“LNC”,“MSH”,“MTH”,“MTHICD9”,“NCI”,“NDFRT”,“RXNORM”,“SNOMEDCT”]
        * name (like MedicationMention, also a vector)
        :param **kwargs:
        """

        vector = self.default_vector.copy()
        vector[0] = self._encode_polarity(token)

        count_concepts = 0

        for hit in token:
            if not self._is_acceptable_hit(hit):
                continue
            semtype = list(hit.keys())[0]
            count_concepts += len(hit[semtype])

        vocab_vect = self.vectorize_vocab(token)
        tui_vect = self.vectorize_tui(token)
        tty_vect = self.vectorize_tty(token)
        sem_type_vect = self.vectorize_sem_types(token)
        # TODO: maybe instead of add the count, bin the count to make the feature vector one hot encoder
        if sum(vocab_vect) > 1:
            vector[1] = 1
        if count_concepts > 2:
            vector[2] = 1
        vector[self.non_vocab_vect_len: self.non_vocab_vect_len + len(SemTypeCtakesAsserted)] = sem_type_vect

        # potential normalization issue here
        vector[self.non_vocab_vect_len + len(SemTypeCtakesAsserted): len(self.vocab) + self.non_vocab_vect_len +
                                                                     len(SemTypeCtakesAsserted)] = vocab_vect
        vector[len(self.vocab) + self.non_vocab_vect_len + len(SemTypeCtakesAsserted):
               len(self.feat_tui) + len(self.vocab) + self.non_vocab_vect_len + len(SemTypeCtakesAsserted)] = tui_vect
        vector[len(self.feat_tui) + len(self.vocab) + self.non_vocab_vect_len + len(SemTypeCtakesAsserted):] = tty_vect

        return vector


class ClinicalBinary(Clinical, BinaryFeature, ABC):
    feature_type = FeatureType.clinical_binary
    vector_length = BinaryFeature.vector_length
    annotated_feature = FeatureType.clinical

    def __init__(self):
        Clinical.__init__(self)
        BinaryFeature.__init__(self, has_polarity=True)

    @property
    def default_vector(self) -> List[int]:
        return BinaryFeature.default_vector.fget(self)

    def vectorize_token(self, token, **kwargs) -> List[int]:
        if token:
            vector = self.default_vector.copy()

            vector[1] = self._encode_polarity(token)

            for hit in token:
                if not self._is_acceptable_hit(hit):
                    continue

                vector[0] = 1

                return vector


class ClinicalVocab(Clinical):
    annotated_feature = FeatureType.clinical
    vector_length = len(Clinical.vocab)
    feature_type = FeatureType.clinical_vocab
    requires_annotation = False

    def vectorize_token(self, token, **kwargs) -> List[int]:
        return super().vectorize_vocab(token)


class ClinicalTui(Clinical):
    annotated_feature = FeatureType.clinical
    vector_length = len(Clinical.feat_tui)
    feature_type = FeatureType.clinical_tui
    requires_annotation = False

    def vectorize_token(self, token, **kwargs) -> List[int]:
        return super().vectorize_tui(token)


class ClinicalTty(Clinical):
    annotated_feature = FeatureType.clinical
    vector_length = len(Clinical.feat_tty)
    feature_type = FeatureType.clinical_tty
    requires_annotation = False

    def vectorize_token(self, token, **kwargs) -> List[int]:
        return super().vectorize_tty(token)


class ClinicalSemType(Clinical):
    annotated_feature = FeatureType.clinical
    vector_length = len(SemTypeCtakesAsserted)
    feature_type = FeatureType.clinical_sem_type
    requires_annotation = False

    def vectorize_token(self, token, **kwargs) -> List[int]:
        return super().vectorize_sem_types(token)


class ClinicalSnomed(Clinical):
    feature_type = FeatureType.clinical_snomed
    vocab = []
    vector_length = (Clinical.non_vocab_vect_len + len(Clinical.semantic_type) + len(Clinical.feat_tty) + len(
        Clinical.feat_tui))
    config_name = FeatureConfigName.snomedct

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.clinical_snomed))


class ClinicalSnomedBinary(ClinicalBinary):
    feature_type = FeatureType.clinical_snomed_binary
    annotated_feature = FeatureType.clinical_snomed


class ClinicalSnomedVocab(ClinicalVocab):
    feature_type = FeatureType.clinical_snomed_vocab
    annotated_feature = FeatureType.clinical_snomed


class ClinicalSnomedSemType(ClinicalSemType):
    feature_type = FeatureType.clinical_snomed_sem_type
    annotated_feature = FeatureType.clinical_snomed


class ClinicalSnomedTTY(ClinicalTty):
    feature_type = FeatureType.clinical_snomed_tty
    annotated_feature = FeatureType.clinical_snomed


class ClinicalSnomedTui(ClinicalTui):
    feature_type = FeatureType.clinical_snomed_tui
    annotated_feature = FeatureType.clinical_snomed


class ClinicalGeneral(Clinical):
    feature_type = FeatureType.clinical_general
    config_name = FeatureConfigName.general

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.clinical_general))


class ClinicalGeneralVocab(ClinicalVocab):
    feature_type = FeatureType.clinical_general_vocab
    annotated_feature = FeatureType.clinical_general


class ClinicalGeneralSemType(ClinicalSemType):
    feature_type = FeatureType.clinical_general_sem_type
    annotated_feature = FeatureType.clinical_general


class ClinicalGeneralTTY(ClinicalTty):
    feature_type = FeatureType.clinical_general_tty
    annotated_feature = FeatureType.clinical_general


class ClinicalGeneralTui(ClinicalTui):
    feature_type = FeatureType.clinical_general_tui
    annotated_feature = FeatureType.clinical_general


class ClinicalGeneralBinary(ClinicalBinary):
    feature_type = FeatureType.clinical_general_binary
    annotated_feature = FeatureType.clinical_general


class ICD9ClinicalCode(Clinical):
    feature_type = FeatureType.clinical_code_icd9
    vocab = []
    feat_tui = PROBLEM_TUI
    feat_tty = DIAGNOSIS_TTY
    vector_length = (Clinical.non_vocab_vect_len + len(Clinical.semantic_type) + len(feat_tty) + len(feat_tui))
    config_name = FeatureConfigName.icd9_code

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.clinical_code_icd9))


class ICD9ClinicalCodeBinary(ClinicalBinary):
    feature_type = FeatureType.clinical_code_icd9_binary
    annotated_feature = FeatureType.clinical_code_icd9


class ICD10ClinicalCode(Clinical):
    feature_type = FeatureType.clinical_code_icd10
    vocab = []
    feat_tui = PROBLEM_TUI
    feat_tty = DIAGNOSIS_TTY
    vector_length = (Clinical.non_vocab_vect_len + len(Clinical.semantic_type) + len(feat_tty) + len(feat_tui))
    config_name = FeatureConfigName.icd10_code

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.clinical_code_icd10))


class ICD10ClinicalCodeBinary(ClinicalBinary):
    feature_type = FeatureType.clinical_code_icd10_binary
    annotated_feature = FeatureType.clinical_code_icd10


class ClinicalMedgen(Clinical):
    feature_type = FeatureType.clinical_medgen
    vocab = []
    vector_length = (Clinical.non_vocab_vect_len + len(Clinical.semantic_type) + len(Clinical.feat_tty) + len(
        Clinical.feat_tui))
    config_name = FeatureConfigName.medgen

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.clinical_medgen))


class ClinicalMedgenBinary(ClinicalBinary):
    feature_type = FeatureType.clinical_medgen_binary
    annotated_feature = FeatureType.clinical_medgen


class ClinicalMedGenVocab(ClinicalVocab):
    feature_type = FeatureType.clinical_medgen_vocab
    annotated_feature = FeatureType.clinical_medgen


class ClinicalMedGenSemType(ClinicalSemType):
    feature_type = FeatureType.clinical_medgen_sem_type
    annotated_feature = FeatureType.clinical_medgen


class ClinicalMedGenTTY(ClinicalTty):
    feature_type = FeatureType.clinical_medgen_tty
    annotated_feature = FeatureType.clinical_medgen


class ClinicalMedGenTui(ClinicalTui):
    feature_type = FeatureType.clinical_medgen_tui
    annotated_feature = FeatureType.clinical_medgen
