from feature_service.nlp import nlp_cache
from feature_service.nlp.nlp_reader import ClinicalReader
from text2phenotype.constants.features import FeatureType
from text2phenotype.constants.umls import (
    PROBLEM_TTY,
    PROBLEM_TUI,
    PROBLEM_VOCAB,
)
from .clinical import (
    Clinical,
    ClinicalSemType,
    ClinicalTty,
    ClinicalTui,
    ClinicalVocab,
)
from .feature import FeatureConfigName


class Problem(Clinical):
    feature_type = FeatureType.problem
    vocab = PROBLEM_VOCAB
    feat_tui = PROBLEM_TUI
    feat_tty = PROBLEM_TTY
    vector_length = (Clinical.non_vocab_vect_len + len(vocab) + len(Clinical.semantic_type) + len(feat_tty) +
                     len(feat_tui))
    config_name = FeatureConfigName.problem_master

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.problem))


class ProblemVocab(ClinicalVocab):
    feature_type = FeatureType.problem_vocab
    annotated_feature = FeatureType.problem


class ProblemSemType(ClinicalSemType):
    feature_type = FeatureType.problem_sem_type
    annotated_feature = FeatureType.problem


class ProblemTTY(ClinicalTty):
    feature_type = FeatureType.problem_tty
    annotated_feature = FeatureType.problem


class ProblemTUI(ClinicalTui):
    feature_type = FeatureType.problem_tui
    annotated_feature = FeatureType.problem
