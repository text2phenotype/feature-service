from feature_service.features.clinical import (
    Clinical,
    ClinicalSemType,
    ClinicalTty,
    ClinicalTui,
    ClinicalVocab,
)
from feature_service.features.feature import FeatureConfigName
from feature_service.nlp import nlp_cache
from feature_service.nlp.nlp_reader import ClinicalReader
from text2phenotype.constants.features import FeatureType
from text2phenotype.constants.umls import (
    DIAGNOSIS_TTY,
    PROBLEM_TUI,
    Vocab)


class Diagnosis(Clinical):
    feature_type = FeatureType.diagnosis
    vocab = []
    feat_tui = PROBLEM_TUI
    feat_tty = DIAGNOSIS_TTY
    vector_length = (Clinical.non_vocab_vect_len + len(Clinical.semantic_type) + len(feat_tty) + len(feat_tui))
    config_name = FeatureConfigName.icd_syn

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.diagnosis))


class DiagnosisVocab(ClinicalVocab):
    feature_type = FeatureType.diagnosis_vocab
    annotated_feature = FeatureType.diagnosis


class DiagnosisSemType(ClinicalSemType):
    feature_type = FeatureType.diagnosis_sem_type
    annotated_feature = FeatureType.diagnosis


class DiagnosisTTY(ClinicalTty):
    feature_type = FeatureType.diagnosis_tty
    annotated_feature = FeatureType.diagnosis


class DiagnosisTui(ClinicalTui):
    feature_type = FeatureType.diagnosis_tui
    annotated_feature = FeatureType.diagnosis

class DiagnosisICD10(Diagnosis):
    feature_type = FeatureType.icd10_diagnosis
    pref_vocab = [Vocab.ICD10CM.name, Vocab.ICD10.name, Vocab.ICD10AE.name, Vocab.ICD10.name]
