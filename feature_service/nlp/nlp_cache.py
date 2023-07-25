import os
import hashlib
from typing import List, Dict

from text2phenotype.common import common
from text2phenotype.common.log import operations_logger

from feature_service.nlp import autocode
from feature_service.feature_service_env import FeatureServiceEnv


###############################################################################
#
# Functions to enable caching, nearly identical to text2phenotype.nlp.autocode
#
###############################################################################

def autocode_cache(text: str, autocoder, cache_filetype, dictionary=None) -> Dict:
    """
    Autocode and cache responses for a given text/autocoder.
    If results already exist in CACHE_DIR, return without calling autocoder.
    :param text: biomedical text
    :param autocoder: NLP autocoder function like text2phenotype.nlp.lab_value
    :param cache_filetype: name to save file as
    :param dictionary: which dictionary to use for this autocode pipeline
    :return: dict autocoded response
    """
    if not FeatureServiceEnv.NLP_CACHE_ENABLE.value:
        operations_logger.debug('cache is disabled, calling autocoder directly.')
        if dictionary:
            res = autocoder(text, dictionary)
        else:
            res = autocoder(text)
        res['umls_host'] = FeatureServiceEnv.UMLS_HOST.value
        return res
    else:
        f = hash_path(text, cache_filetype)
        if os.path.exists(f):
            return common.read_json(f)
        else:
            if dictionary:
                res = autocoder(text, dictionary)
            else:
                res = autocoder(text)

            if isinstance(res, dict):
                res['cache_file'] = f
                res['umls_host'] = FeatureServiceEnv.UMLS_HOST.value

            common.write_json(res, f)
            return res


def clinical(text: str) -> Dict:
    return autocode_cache(text, autocode.autocode_dest, 'clinical')


def clinical_snomed(text: str) -> Dict:
    return autocode_cache(text, autocode.snomed_clinical, 'clinical_snomed')


def clinical_general(text: str) -> Dict:
    return autocode_cache(text, autocode.general_clinical, 'clinical_general')


def clinical_icd9(text: str) -> Dict:
    return autocode_cache(text, autocode.autocode_icd9_code, 'clinical_icd9')


def clinical_icd10(text: str) -> Dict:
    return autocode_cache(text, autocode.autocode_icd9_code, 'clinical_icd10')


def clinical_code_icd9(text: str) -> Dict:
    return autocode_cache(text, autocode.autocode_icd9_code, 'clinical_code_icd9')


def clinical_code_icd10(text: str) -> Dict:
    return autocode_cache(text, autocode.autocode_icd10_code, 'clinical_code_icd10')


def clinical_medgen(text: str) -> Dict:
    return autocode_cache(text, autocode.medgen_clinical, 'clinical_medgen')


def lab_value(text: str) -> Dict:
    """
    BIOMED-1402 : default lab_value is *** HEPC lab value***
    see also: autocode.py
    see also: nlp_cache.py
    see also: LabReader(ClinicalReader)
    see also: HepcLabReader
    BIOMED-1402 : default lab_value is HEPC lab value.
    HEPC lab values are default because this is a clinical expert reviewed lab list with common lab tests
    """
    return hepc_lab_value(text)

def lab_master(text:str) -> Dict:
    return autocode_cache(text, autocode.lab_master, 'lab_master')

def drug_ner(text: str, dictionary=autocode.Vocab.rxnorm.name) -> Dict:
    """
    BIOMED-1402 drug_ner default is 'rxnorm' NOT 'rxnorm-syn'
    """
    return autocode_cache(text, autocode.drug_ner, f'drug_ner_{dictionary}', dictionary)

def drug_ner_syn(text: str, dictionary='rxnorm-syn') -> Dict:
    """
    """
    return autocode_cache(text, autocode.drug_ner_syn, f'drug_ner_{dictionary}', dictionary)

def smoking(text: str) -> Dict:
    return autocode_cache(text, autocode.smoking, 'smoking')


def temporal(text: str) -> Dict:
    return autocode_cache(text, autocode.temporal, 'temporal')


def hepc_clinical(text: str) -> Dict:
    return autocode_cache(text, autocode.hepc_clinical, 'hepc_clinical')


def hepc_drug_ner(text: str) -> Dict:
    return autocode_cache(text, autocode.hepc_drug_ner, 'hepc_drug_ner')


def hepc_lab_value(text: str) -> Dict:
    return autocode_cache(text, autocode.hepc_lab_value, 'hepc_lab_value')


def loinc_lab_value(text: str) -> Dict:
    return autocode_cache(text, autocode.loinc_lab_value, 'loinc_lab_value')


def problem(text: str) -> Dict:
    return autocode_cache(text, autocode.problem, 'problem')


def problem_master(text: str) -> Dict:
    return autocode_cache(text, autocode.problem_master, 'problem_master')



def diagnosis(text: str) -> Dict:
    return autocode_cache(text, autocode.diagnosis, 'diagnosis')


def covid(text: str) -> Dict:
    return autocode_cache(text, autocode.covid_clinical, 'covid_clinical')


def npi_recognition(text: str) -> Dict:
    return autocode_cache(text, autocode.npi, 'npi')


def topography(text: str) -> Dict:
    return autocode_cache(text, autocode.topography, 'topography')


def topography_code(text: str) -> Dict:
    return autocode_cache(text, autocode.topography_code, 'topography_code')


def morphology(text: str) -> Dict:
    return autocode_cache(text, autocode.morphology, 'morphology')


def morphology_code(text: str) -> Dict:
    return autocode_cache(text, autocode.morphology_code, 'morphology_code')

def loinc_common(text: str) -> Dict:
    return autocode_cache(text, autocode.loinc_common, 'loinc_common')

def loinc_mimic(text: str) -> Dict:
    return autocode_cache(text, autocode.loinc_mimic, 'loinc_mimic')

def loinc_section(text: str) -> Dict:
    return autocode_cache(text, autocode.loinc_section, 'loinc_section')


def loinc_title(text: str) -> Dict:
    return autocode_cache(text, autocode.loinc_title, 'loinc_title')

def loinc2hpo(text: str) -> Dict:
    return autocode_cache(text, autocode.loinc2hpo, 'loinc2hpo')

# TODO: remove once new UMLS is in the wild (2020-09-23)
def covid_repr(text: str) -> Dict:
    return autocode_cache(text, autocode.covid_repr, 'covid_repr')


def gene(text: str) -> Dict:
    return autocode_cache(text, autocode.gene, 'gene')

###############################################################################
#
# Cache environment variables and filesystem handlers
#
###############################################################################


def init_cache_dir() -> str:
    """
    Initialize (create) the NLP_CACHE folder
    """
    cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    return cache_dir


def get_cache_dir() -> str:
    """
    Get NLP_CACHE environment variable setting
    """
    return FeatureServiceEnv.NLP_CACHE.value


def hash_text(text: str) -> str:
    """
    Get hashkey for text
    :param text: biomedical text
    :return: unique key
    """
    return hashlib.md5(text.encode()).hexdigest()


def hash_filename(text: str, cache_method: str, file_type='json') -> str:
    """
    :param text: biomedical text
    :param cache_method: nlp autocoder
    :return: filename with format hash_text.cache_method.file_type
    """
    return f"{hash_text(text)}.{cache_method}.{file_type}"


def hash_dir(text: str, hash_len=4) -> List:
    """
    :param text: input text of any length
    :param hash_len: default 4 (15^4 = 50k, which is in recommended range of number of files per EXT4)
    :return: list of dirs
    """
    cache_dir = get_cache_dir()

    if not os.path.exists(cache_dir):
        operations_logger.info('creating NLP_CACHE %s ' % cache_dir)
        os.makedirs(cache_dir)

    hash = hash_text(text)  # 32

    dirs = [cache_dir, hash[0:hash_len], hash[hash_len:]]
    dirs = os.sep.join(dirs)

    if not os.path.exists(dirs):
        os.makedirs(dirs)

    return dirs


def hash_path(text: str, cache_type: str, file_type='json') -> str:
    return hash_dir(text) + os.sep + hash_filename(text, cache_type, file_type)


def save_text(text: str, cache_method='save_text') -> str:
    """
    Writes text using text2phenotype.common.write_text(...)
    :param text: raw clinical text
    :return: path to saved file
    """
    _file = hash_path(text, cache_method, 'txt')
    if os.path.exists(_file):
        pass
    else:
        return common.write_text(text, _file)


def list_contents(file_type: str, cache_dir=get_cache_dir()) -> List:
    """
    Get a list of files in an NLP cache directory matching file_type
    :param file_type: like '.txt' or '.json' or '.clinical.json'
    :param cache_dir: default NLP_CACHE
    :return: list of paths to cache contents
    """
    contents = list()
    if os.path.isdir(cache_dir):
        for index in os.listdir(cache_dir):
            if os.path.isdir(os.path.join(cache_dir, index)):
                for entry in os.listdir(os.path.join(cache_dir, index)):
                    cache_entry = os.path.join(cache_dir, index, entry)
                    if os.path.isdir(cache_entry):
                        for f in os.listdir(cache_entry):
                            if f.endswith(file_type):
                                contents.append(os.path.join(cache_entry, f))
    return contents