import os
import unittest
from typing import List, Dict
import numpy

from text2phenotype.common import common
from text2phenotype.common.feature_data_parsing import from_bag_of_words

from feature_service.common.data_source import FeatureServiceDataSource
from feature_service.nlp.nlp_reader import ClinicalReader, DrugReader, LabReader
from feature_service.nlp import nlp_cache

#################################################################################
#
# TARGET entity types matching umls VOCABS
#
##################################################################################
TARGETS = ['Cancer', 'Lab', 'Allergy', 'Medication', 'SignSymptom', 'Findings', 'Device', 'DiseaseDisorder']

VOCABS = {
    0: 'problem',
    1: 'clinical_icd9',
    2: 'clinical_icd10',
    3: 'loinc2hpo',
    4: 'clinical_snomed',
    5: 'clinical_general',
    6: 'covid',
    7: 'hepc_clinical',
    8: 'clinical_medgen',
    9: 'topography',
    10: 'morphology',
    11: 'loinc_section',
    12: 'loinc_title',
    13: 'drug_ner',
    14: 'drug_ner_syn',
    15: 'hepc_drug_ner',
    16: 'lab_value',
    17: 'loinc_lab_value',
    18: 'loinc_common',
    19: 'lab_master'}

#################################################################################
#
# ANNOTATION FILES
#
##################################################################################
ANNOTATIONS_DIR = os.environ.get('ANNOTATION_DIR', '/Users/andy.mcmurry/s3copy/annotations-phi')


# ANNOTATIONS_DIR = os.environ.get('ANNOTATION_DIR', '/Users/andy.mcmurry/s3copy/annotations-merged')

def filepath(filename: str):
    folder = os.path.join(ANNOTATIONS_DIR, 'BIOMED-1826')
    if not os.path.exists(folder):
        os.mkdir(folder)

    f = os.path.join(ANNOTATIONS_DIR, 'BIOMED-1826', filename)
    print(f'file\t{f}')
    return f


def save(contents, filename: str):
    if filename.endswith('.json'):
        common.write_json(contents, filepath(filename))
    else:
        common.write_text(contents, filepath(filename))


def load(filename: str):
    if filename.endswith('.json'):
        return common.read_json(filepath(filename))
    else:
        return common.read_text(filepath(filename))


def aggregate_files(dir_path=ANNOTATIONS_DIR, endswith='.ann') -> List[str]:
    """
    Aggregate ANN files from $ANNOTATION_DIR

    :param dir_path: ANN annotations root folder
    :param endswith: .ann default annotations file from Text2phenotype human reviewers
    :return: list of ANN annotation files
    """
    res = list()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(endswith):
                file_path = os.path.join(root, file)
                res.append(file_path)
    return res


#################################################################################
#
# TEST
#
##################################################################################

class TestBiomed1826_UMLS_Update(unittest.TestCase):

    def test_Cancer(self):
        t = 'Cancer'
        CalculateTF().target(t)
        CalculateLongest().target(t)
        CalculateOutOfVocab().target_Cancer()

    def test_DiseaseDisorder(self):
        t = 'DiseaseDisorder'
        # CalculateTF().target(t)
        CalculateLongest().target(t)
        # CalculateOutOfVocab().target_DiseaseDisorder()

    def test_SignSymptom(self):
        t = 'SignSymptom'
        CalculateTF().target(t)
        CalculateLongest().target(t)
        CalculateOutOfVocab().target_SignSymptom()

    def test_Medication(self):
        t = 'Medication'
        CalculateTF().target(t)
        CalculateLongest().target(t)
        CalculateOutOfVocab().target_Medication()

    def test_Allergy(self):
        t = 'Allergy'
        CalculateTF().target(t)
        CalculateLongest().target(t)
        CalculateOutOfVocab().target_Allergy()

    def test_Lab(self):
        t = 'Lab'
        CalculateTF().target(t)
        CalculateLongest().target(t)
        CalculateOutOfVocab().target_Lab()

    def test_Findings(self):
        t = 'Findings'
        CalculateTF().target(t)
        CalculateLongest().target(t)
        CalculateOutOfVocab().target_Findings()

    def test(self):
        for t in TARGETS:
            CalculateTF().target(t)
            # CalculateLongest().target(t)


def deprecated__list_ann_highlights(ann_filename, filterBy=None) -> List[str]:
    """
    Highlight annotations from ANN file

    :param ann_filename: ANN annotation file
    :param filterBy: optionally filter by one of the include/exclude/legacy entity labels (losely speaking, aspects)
    :return: list of human expert labeled highlighted str
    """
    highlights = list()

    legacy = ['Disability', 'Cancer', 'medication', 'Device/Procedure', 'physical_exam']
    include = ['Medication', 'Allergy', 'Lab', 'DiseaseDisorder', 'SignSymptom', 'DiagnosticImaging', 'CovidLabs',
               'Device', 'Findings', 'DocumentType'] + legacy
    exclude = ['PHI', 'Demographic', 'Smoking', 'SocialRiskFactors', 'VitalSigns', 'EventDate', 'DuplicateDocument',
               'Temporal', 'None', 'Deviated septum']

    for line in common.read_text(ann_filename).splitlines():
        cols = line.split('\t')
        text = None
        aspect = None

        if len(cols) > 6:
            text = cols[3].strip()
            aspect = cols[4].strip()

        # unknown entity type
        if aspect:
            if aspect not in include and aspect not in exclude:
                raise Exception(f"{aspect}|{text}|{line}")

        if text and aspect in include:
            if filterBy is None:
                highlights.append(text.strip())
            elif filterBy == aspect:
                highlights.append(text.strip())

    return highlights


def list_highlights(ann_filename, filterBy=None) -> List[str]:
    highlighted = list()

    legacy = ['Disability', 'Cancer', 'medication', 'Device/Procedure', 'physical_exam']
    include = ['Medication', 'Allergy', 'Lab', 'DiseaseDisorder', 'SignSymptom', 'DiagnosticImaging',
               'CovidLabs', 'Device', 'Findings', 'DocumentType'] + legacy
    exclude = ['PHI', 'Demographic', 'Smoking', 'SocialRiskFactors', 'VitalSigns', 'EventDate',
               'DuplicateDocument', 'Temporal', 'None', 'Deviated septum']

    try:
        for annot in FeatureServiceDataSource.parse_brat_ann_with_link_info(ann_filename).values():

            # Filter
            if annot.category_label in include:
                if filterBy is None:
                    highlighted.append(annot.text)
                elif filterBy == annot.category_label:
                    highlighted.append(annot.text)
            elif annot.category_label in exclude:
                pass  # do nothing
            else:
                raise Exception(f"{annot.category_label}|{annot.text}|{annot.__dict__}")
    except:
        print(f'@@@Failed {ann_filename}')

    return highlighted


def tf_annotations(annotations_dir, annotation_type=None) -> Dict[int, str]:
    """
    :param annotations_dir: ANN human annotations
    :param annotation_type: (optional) filterBy annotation type, such as "Medication"
    :return: dict mapping Key:int 'term frequency'  to Value:str 'Highlighted String'
    """
    phrases = list()
    for f in aggregate_files(annotations_dir):
        for selected in list_highlights(f, annotation_type):
            if '|' in selected:
                print('skipping !!! highlight contains bad char=' + str(selected))
            else:
                phrases.append(selected.strip())

    return from_bag_of_words(phrases)


class CalculateTF:

    def test(self):
        for target in TARGETS:
            self.target(target)

    def target(self, aspect):
        """
        Term Frequency of annotations
        """
        print(f'TF @target= {aspect}')

        save(tf_annotations(ANNOTATIONS_DIR, aspect), f'tf.{aspect}.json')

        TF = load(f'tf.{aspect}.json')

        xyplot = list()

        for phrase, freq in TF.items():

            phrase = phrase.replace('|', '?')
            x_chars = len(phrase)
            y_freq = numpy.log(freq)

            attribute = ''
            if len(phrase) < 3:
                attribute = '@short'
            elif len(phrase) > 75:
                attribute = '@long'

            xyplot.append(f"{x_chars}\t{y_freq}\t{attribute}\t{phrase}")
        save('\n'.join(xyplot), f'plot.{aspect}.tsv')


#################################################################################
#
# CalculateLongest : UMLS match 20 UMLS sources
#
##################################################################################
def umls_drug() -> List:
    """
    :return:
    """
    return [nlp_cache.drug_ner,
            nlp_cache.drug_ner_syn,
            nlp_cache.hepc_drug_ner]


def umls_lab() -> List:
    """
    :return:
    """
    return [nlp_cache.lab_value,
            nlp_cache.loinc_lab_value,
            nlp_cache.loinc_common,
            nlp_cache.lab_master]


def umls_snomed() -> List:
    """
    :return:
    """
    return [nlp_cache.clinical_snomed,
            nlp_cache.clinical_general]


def umls_problem() -> List:
    """
    :return: ICD9/10 string names, and HPO phenotypes determined from measure.
    """
    return [nlp_cache.problem,
            nlp_cache.clinical_icd9, nlp_cache.clinical_icd10,
            nlp_cache.loinc2hpo]


def umls_problem_special() -> List:
    """
    :return: COVID, Hepc CRF Form clinical, NCBI MedGen, and ICDO Topography/Morpology
    """
    return [nlp_cache.covid,
            nlp_cache.hepc_clinical,
            nlp_cache.clinical_medgen, nlp_cache.topography, nlp_cache.morphology]


def umls_document() -> List:
    """
    :return:
    """
    return [nlp_cache.loinc_section, nlp_cache.loinc_title]


class CalculateLongest:
    def target(self, aspect):
        TF = load(f'tf.{aspect}.json')

        longest = list()

        last = None
        for phrase, freq in TF.items():

            print(f'{phrase}')

            targets = umls_problem() + umls_snomed() + umls_problem_special() + umls_document()
            targets = [ClinicalReader(phrase, autocoder=a) for a in targets]
            targets += [DrugReader(phrase, t) for t in umls_drug()]
            targets += [LabReader(phrase, t) for t in umls_lab()]

            results = '|'.join([str(len(t.longest())) for t in targets])  # LONGEST

            longest.append(f"{freq}|{phrase}|{results}")

            if last is None:
                last = freq
            elif last == freq:
                pass
            elif freq < last:
                save({'rows': longest}, f'longest.{aspect}.json')
                last = freq

    def test(self):
        for target in TARGETS:
            self.target(target)


class CalculateOutOfVocab:

    def target_Cancer(self):
        self.target('Cancer', [4, 9, 10])  # strict ICD-O names only in this strict test

    def target_DiseaseDisorder(self):
        self.target('DiseaseDisorder', list(range(0, 8)))

    def target_SignSymptom(self):
        self.target('SignSymptom', list(range(0, 8)))

    def target_Allergy(self):
        self.target('Allergy', [13, 14, 15])

    def target_Medication(self):
        self.target('Medication', [13, 14, 15])

    def target_Lab(self):
        self.target('Lab', [6, 7, 16, 17, 18, 19])

    def target_Findings(self):
        self.target('Findings', [0, 3, 4, 5, 6])

    def target(self, aspect, allow: List[int]):
        longest = load(f'longest.{aspect}.json')['rows']
        missing = list()

        for row in longest:
            cols = row.split('|')
            tf = cols[0]
            phrase = cols[1]
            matches = cols[2:]
            found = False

            for a in allow:
                if not found and int(str(matches[a])) > 0:
                    found = True

            if not found:
                missing.append(f'{tf}\t{phrase}')

        save('\n'.join(missing), f'oovocab.{aspect}.tsv')

    def test(self):
        self.target_Cancer()
        self.target_DiseaseDisorder()
        self.target_SignSymptom()
        self.target_Medication()
        self.target_Allergy()
        self.target_Lab()
        self.target_Findings()
