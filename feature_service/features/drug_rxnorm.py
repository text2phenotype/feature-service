from collections import defaultdict
from typing import List

from feature_service.features import (
    Clinical,
    ClinicalBinary,
    ClinicalTty,
    ClinicalTui,
    ClinicalVocab,
)
from feature_service.features.feature import FeatureConfigName
from feature_service.nlp import nlp_cache
from text2phenotype.constants.features import FeatureType
from text2phenotype.constants.umls import (
    DRUG_TTY,
    DRUG_TUI,
    DRUG_VOCAB,
    Vocab,
)


class DrugRXNorm(Clinical):
    feature_type = FeatureType.drug_rxnorm
    non_vocab_len = 6
    vocab = DRUG_VOCAB
    feat_tui = DRUG_TUI
    feat_tty = DRUG_TTY
    semantic_type = []
    vector_length = (non_vocab_len + len(vocab) + len(feat_tty) + len(feat_tui))
    config_name = FeatureConfigName.rxnorm

    medication = 'Medication'
    attributes = 'attributes'
    umlsConcept = 'umlsConcept'
    medStrengthNum = 'medStrengthNum'
    medStrengthUnit = 'medStrengthUnit'
    medFrequencyUnit = 'medFrequencyUnit'
    medFrequencyNum = 'medFrequencyNum'
    polarity = 'polarity'
    medDosage = 'medDosage'
    medUnit = 'medUnit'
    pref_vocab = [Vocab.RXNORM.name]

    # @chunk_annotations()
    def annotate(self, text: str, fdl_data: dict = None, **kwargs):
        """JIRA/BIOMED-270"""
        if fdl_data:
            data = fdl_data['result']
        else:
            data = nlp_cache.drug_ner(text)['drugEntities']

        matches = defaultdict(list)
        for hit in data:
            _text = hit['text']
            index = (_text[1], _text[2])

            if text[_text[1]: _text[2]].lower() != _text[0].lower():
                # Wrong range for the text
                continue

            matches[index].append({self.medication: hit[self.umlsConcept],
                                   self.attributes: hit[self.attributes]})

            dosage = hit[self.attributes].get(self.medStrengthNum)

            if isinstance(dosage, list) and len(dosage) > 2:
                med_dosage = dosage[0]
                dosage_index = (dosage[1], dosage[2])
                matches[dosage_index] = [{self.medDosage: med_dosage}]

            unit = hit[self.attributes].get(self.medStrengthUnit)

            if isinstance(unit, list) and len(unit) > 0:
                med_unit = unit[0]
                unit_index = (unit[1], unit[2])
                matches[unit_index] = [{self.medUnit: med_unit}]

        for key, value in matches.items():
            for r in range(len(value)):
                if self.medication in matches[key][r]:
                    matches[key][r][self.medication] = self.sort_concepts(value[r][self.medication])[0:self.MAX_CONCEPTS_TO_INCLUDE]
        return matches.items()

    @classmethod
    def encode_polarity(cls, token) -> int:
        polarity = token[0].get(cls.attributes, {}).get(cls.polarity)

        return 1 if polarity == 'positive' else 0

    def vectorize_token(self, token: dict, **kwargs) -> List[int]:
        vector = self.default_vector.copy()

        vector[0] = self.encode_polarity(token)
        if len(token[0].get(self.attributes, {}).get(self.medStrengthNum, [])) > 0:
            vector[2] = 1
        if len(token[0].get(self.attributes, {}).get(self.medStrengthUnit, [])) > 0:
            vector[3] = 1

        vocab_set = set()
        tui_set = set()
        tty_set = set()
        for hit in token:
            if self.medication in hit:
                vector[1] = 1
            if self.medDosage in hit:   # TODO: should be in "attributes" section?
                vector[4] = 1
            if self.medUnit in hit:   # TODO: should be in "attributes" section, and medStrengthUnit?
                vector[5] = 1
            semtype = list(hit.keys())[0]

            for concept in hit[semtype]:
                if isinstance(concept, dict):
                    vocab = concept.get('codingScheme', None)
                    tuis = set(concept.get('tui', []))
                    ttys = set(concept.get('tty', []))
                    if vocab:
                        vocab_set.add(vocab)
                    if tuis:
                        tui_set = tui_set.union(tuis)
                    if ttys:
                        tty_set = tty_set.union(ttys)

        vector[self.non_vocab_len:len(DRUG_VOCAB)+self.non_vocab_len] = self.vectorize_sab_vocab(list(vocab_set))
        vector[len(DRUG_VOCAB)+self.non_vocab_len: len(DRUG_TUI)+self.non_vocab_len+len(DRUG_VOCAB)] = self.vectorize_tui_semtype(list(tui_set))
        vector[len(DRUG_TUI)+self.non_vocab_len+len(DRUG_VOCAB):] = self.vectorize_tty_termtype(list(tty_set))
        return vector


class DrugRXNormBinary(ClinicalBinary):
    feature_type = FeatureType.drug_rxnorm_binary
    annotated_feature = FeatureType.drug_rxnorm

    def vectorize_token(self, token, **kwargs) -> List[int]:
        if not token:
            return

        vector = self.default_vector.copy()

        vector[1] = DrugRXNorm.encode_polarity(token)

        for hit in token:
            if DrugRXNorm.medication in hit:
                vector[0] = 1

        return vector


class DrugRxNormTTY(ClinicalTty):
    feat_tty = DRUG_TTY
    feature_type = FeatureType.drug_rxnorm_tty
    annotated_feature = FeatureType.drug_rxnorm
    vector_length = len(feat_tty)


class DrugRxNormTui(ClinicalTui):
    feat_tui = DRUG_TUI
    feature_type = FeatureType.drug_rxnorm_tui
    annotated_feature = FeatureType.drug_rxnorm
    vector_length = len(feat_tui)


class DrugRxNormVocab(ClinicalVocab):
    vocab = DRUG_VOCAB
    feature_type = FeatureType.drug_rxnorm_vocab
    annotated_feature = FeatureType.drug_rxnorm
    vector_length = len(vocab)
