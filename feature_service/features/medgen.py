from feature_service.features.clinical import Clinical, ClinicalBinary
from feature_service.features.feature import FeatureConfigName
from feature_service.nlp import nlp_cache
from feature_service.nlp.nlp_reader import ClinicalReader

from text2phenotype.constants.features import FeatureType


class ClinicalMedgen(Clinical):
    feature_type = FeatureType.clinical_medgen
    vocab = []
    vector_length = (Clinical.non_vocab_vect_len + len(Clinical.semantic_type) + len(Clinical.feat_tty) +
                     len(Clinical.feat_tui))
    config_name = FeatureConfigName.medgen

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.clinical_medgen))


class ClinicalMedgenBinary(ClinicalBinary):
    feature_type = FeatureType.clinical_medgen_binary
    annotated_feature = FeatureType.clinical_medgen


class MedgenGene(Clinical):
    feature_type = FeatureType.gene
    config_name = FeatureConfigName.gene
    vocab = []
    vector_length = (Clinical.non_vocab_vect_len + len(Clinical.semantic_type) + len(Clinical.feat_tty) +
                     len(Clinical.feat_tui))

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.gene))


class MedgenGeneBinary(ClinicalMedgenBinary):
    feature_type = FeatureType.gene_binary
    annotated_feature = FeatureType.gene
