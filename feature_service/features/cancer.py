from collections import defaultdict

from feature_service.features.clinical import (
    Clinical,
    ClinicalBinary,
    ClinicalSemType,
    ClinicalTty,
    ClinicalTui,
    ClinicalVocab,
)
from feature_service.features.feature import FeatureConfigName
from feature_service.features.regex import RegExBase
from feature_service.nlp import nlp_cache
from feature_service.nlp.nlp_reader import ClinicalReader
from text2phenotype.constants.features import FeatureType


class MorphologyDetails:
    """
    Structured representation a morphology code.
    ICD-O morphology codes consist of histology, behavior, and can optionally contain grade.
    """
    def __init__(self, mcode: str):
        """
        Ctor.
        :param mcode: The raw morphology code text.
        """
        self.__histology = None
        self.__behavior = None
        self.__grade = None

        self.__process_code(mcode)

    @property
    def histology(self) -> str:
        return self.__histology

    @property
    def behavior(self) -> str:
        return self.__behavior

    @property
    def grade(self) -> str:
        return self.__grade

    def __process_code(self, mcode: str):
        """
        Decompose the input code into its individual pieces.
        :param mcode: The raw morphology code text.
        """
        delim = '/'

        if not mcode or delim not in mcode:
            return

        tokens = mcode.replace(' ', '').split(delim)
        if len(tokens) > 2 or len(tokens[0]) != 4 or len(tokens[1]) > 2:
            return

        self.__histology = tokens[0]
        self.__behavior = tokens[1][0]
        if len(tokens[1]) == 2:
            self.__grade = tokens[1][1]


class Topography(Clinical):
    vector_length = Clinical.vector_length + 1
    feature_type = FeatureType.topography
    config_name = FeatureConfigName.cancer_topography

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.topography))

    def vectorize_token(self, token: dict, **kwargs):
        vector = super().vectorize_token(token, **kwargs)

        if vector:
            vector.append(0)

            top_keys = {'DiseaseDisorder', 'AnatomicalSite', 'Entity'}
            if self.feature_type.name in token:
                for topo_key in top_keys:
                    if topo_key in token[self.feature_type.name][0]:
                        break

                for topo_result in token[self.feature_type.name][0][topo_key]:
                    if not topo_result['preferredText'].endswith('.9'):  # NOS
                        token[-1] = 1
                        break

        return vector


class TopographyBinary(ClinicalBinary):
    feature_type = FeatureType.topography_binary
    annotated_feature = FeatureType.topography

class TopographyVocab(ClinicalVocab):
    feature_type = FeatureType.topography_vocab
    annotated_feature = FeatureType.topography


class TopographySemType(ClinicalSemType):
    feature_type = FeatureType.topography_sem_type
    annotated_feature = FeatureType.topography


class TopographyTTY(ClinicalTty):
    feature_type = FeatureType.topography_tty
    annotated_feature = FeatureType.topography


class TopographyTui(ClinicalTui):
    feature_type = FeatureType.topography_tui
    annotated_feature = FeatureType.topography


class TopographyCode(Clinical):
    feature_type = FeatureType.topography_code
    config_name = FeatureConfigName.cancer_topography_code

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.topography_code))


class TopographyCodeBinary(ClinicalBinary):
    feature_type = FeatureType.topography_code_binary
    annotated_feature = FeatureType.topography_code


class TopographyCodeRegex(RegExBase):
    feature_type = FeatureType.topography_code_regex
    rules = RegExBase.Feature_Cache.regex_topography_rules()
    vector_length = len(rules)

    def annotate(self, text: str, **kwargs):
        annotations = super().annotate(text, **kwargs)

        cleaned = defaultdict(list)
        for location, loc_annotations in annotations:
            for annotation in loc_annotations:
                matched_text = annotation.get('$OCR_ERRORS2', None)
                if matched_text and matched_text[1] == '(':
                    # match to OCR error where C became (.  need to see if the preceding character to the code
                    # was also matched and need to be trimmed.
                    annotation['$OCR_ERRORS2'] = matched_text[1:]

                    cleaned[(location[0] + 1, location[1])].append(annotation)
                else:
                    cleaned[location].append(annotation)

        return cleaned.items()


class Morphology(Clinical):
    feature_type = FeatureType.morphology
    vector_length = Clinical.vector_length + 1
    config_name = FeatureConfigName.cancer_morphology

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.morphology))

    def vectorize_token(self, token: dict, **kwargs):
        vector = super().vectorize_token(token, **kwargs)

        if vector:
            vector.append(0)

            top_keys = {'DiseaseDisorder', 'AnatomicalSite', 'Entity'}
            if self.feature_type.name in token:
                for topo_key in top_keys:
                    if topo_key in token[self.feature_type.name][0]:
                        break

                for topo_result in token[self.feature_type.name][0][topo_key]:
                    if not topo_result['preferredText'].endswith('.9'):  # NOS
                        token[-1] = 1
                        break

        return vector


class MorphologyBinary(ClinicalBinary):
    feature_type = FeatureType.morphology_binary
    annotated_feature = FeatureType.morphology


class MorphologyVocab(ClinicalVocab):
    feature_type = FeatureType.morphology_vocab
    annotated_feature = FeatureType.morphology


class MorphologySemType(ClinicalSemType):
    feature_type = FeatureType.morphology_sem_type
    annotated_feature = FeatureType.morphology


class MorphologyTTY(ClinicalTty):
    feature_type = FeatureType.morphology_tty
    annotated_feature = FeatureType.morphology


class MorphologyTui(ClinicalTui):
    feature_type = FeatureType.morphology_tui
    annotated_feature = FeatureType.morphology


class MorphologyCode(Clinical):
    feature_type = FeatureType.morphology_code
    config_name = FeatureConfigName.cancer_morphology_code

    def __init__(self):
        super().__init__(ClinicalReader(autocoder=nlp_cache.morphology_code))


class MorphologyCodeBinary(ClinicalBinary):
    feature_type = FeatureType.morphology_code_binary
    annotated_feature = FeatureType.morphology_code


class MorphologyCodeRegex(RegExBase):
    feature_type = FeatureType.morphology_code_regex
    rules = RegExBase.Feature_Cache.regex_morphology_rules()
    vector_length = len(rules)


class TumorGradeCode(RegExBase):
    feature_type = FeatureType.tumor_grade_code
    rules = RegExBase.Feature_Cache.regex_grade_code_rules()
    re_flags = 0
    vector_length = len(rules)


class TumorGradeTerms(RegExBase):
    feature_type = FeatureType.tumor_grade_terms
    rules = RegExBase.Feature_Cache.regex_grade_term_rules()
    re_flags = 0
    vector_length = len(rules)


class TNMStaging(RegExBase):
    """
    NOTE: this is the complete specification, but we are currently only concerned with TNM.

    - T describes the size of the original (primary) tumor and whether it has invaded nearby tissue
        - Tx: tumor cannot be assessed
        - Tis: carcinoma in situ
        - T0: no evidence of tumor
        - T1, T2, T3, T4: size and/or extension of the primary tumor
    - N describes nearby (regional) lymph nodes that are involved
        - Nx: lymph nodes cannot be assessed
        - N0: no regional lymph nodes metastasis
        - N1: regional lymph node metastasis present; at some sites, tumor spread to closest or small number of
              regional lymph nodes
        - N2: tumor spread to an extent between N1 and N3 (N2 is not used at all sites)
        - N3: tumor spread to more distant or numerous regional lymph nodes (N3 is not used at all sites)
    - M describes distant metastasis
        - M0: no distant metastasis
        - M1: metastasis to distant organs (beyond regional lymph nodes)

    Other parameters
        - G (1–4): the grade of the cancer cells (i.e. they are "low grade" if they appear similar to normal cells,
                   and "high grade" if they appear poorly differentiated)
        - S (0–3): elevation of serum tumor markers
        - R (0–2): the completeness of the operation (resection-boundaries free of cancer cells or not)
        - L (0–1): invasion into lymphatic vessels
        - V (0–2): invasion into vein (no, microscopic, macroscopic)
        - C (1–5): a modifier of the certainty (quality) of the last mentioned parameter (has been removed in the TNM
                   8th edition)

    Prefix modifiers
        - c: stage is determined from evidence acquired before treatment (including clinical examination, imaging,
             endoscopy, biopsy, surgical exploration). The c-prefix is implicit in absence of the p-prefix.
        - p: stage given by histopathologic examination of a surgical specimen
        - y: stage assessed after chemotherapy and/or radiation therapy; in other words, the individual had
             neoadjuvant therapy.
        - r: stage for a recurrent tumor in an individual that had some period of time free from the disease.
        - a: stage determined at autopsy.
        - u: stage determined by ultrasonography or endosonography. Clinicians often use this modifier although it is
             not an officially defined one

    - For the T, N and M parameters exist subclassifications for some cancer-types (e.g. T1a, Tis, N1i)

    Examples
        - pT1 pN0 M0 R0 G1
        - pT4 pN2 M1 R1 G3
    """
    feature_type = FeatureType.tnm_code
    rules = RegExBase.Feature_Cache.regex_tnm_stage_rules()
    re_flags = 0
    vector_length = len(rules)
