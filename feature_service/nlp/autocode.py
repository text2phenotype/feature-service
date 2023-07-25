import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from urllib3.util.retry import Retry

from text2phenotype.common.log import operations_logger

from feature_service.feature_service_env import FeatureServiceEnv

"""
##########################################################################################
#
# ENVIRONMENT VARIABLES - MUST DEFINE IN feature_service.feature_service_env.FeatureServiceEnv class
#
# UMLS_HOST     optional    explicitly define requests for UMLS based lookups
#
# NPI_HOST      optional    NPI (National Provider Identifiers)       default = UMLS_HOST
#
# ADDRESS_HOST  optional    https://openaddresses.io                  default = UMLS_HOST
#
##########################################################################################
"""
UMLS_HOST = FeatureServiceEnv.UMLS_HOST.value
NPI_HOST = FeatureServiceEnv.NPI_HOST.value or UMLS_HOST
ADDRESS_HOST = FeatureServiceEnv.ADDRESS_HOST.value or UMLS_HOST
# basic auth is NOT required at the time this was coded,
# but passing any username/password strings when the server is not
# protected with basic auth does not cause issues
# ==> leaving support for basic auth username/password
NLP_USERNAME = FeatureServiceEnv.NLP_USERNAME.value
NLP_PASSWORD = FeatureServiceEnv.NLP_PASSWORD.value

CONTENT_TYPE = 'application/x-www-form-urlencoded; charset=utf-8'


def get_session(max_retries: int = FeatureServiceEnv.NLP_MAX_RETRIES.value,
                backoff_factor: int = 1,
                session: requests.Session = None) -> requests.Session:

    # code from https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
        backoff_factor=backoff_factor
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = session if session else requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class Vocab(Enum):  # TODO: merge definition with text2phenotype/ccda/vocab
    original = 'original'  # ctakes original SNOMEDCT+RXNORM
    general = 'general'  # ctakes (supports pos_tagger smoking_status lab_value)
    snomedct = 'snomedct'  # Clinical Terms (many Aspect types)
    problem = 'problem-master'
    diagnosis = 'icd-syn'
    covid = 'covid'     # TODO: remove once new UMLS is in the wild (2020-09-23)
    hepc = 'hepc'  # Hepatitis-C
    icd9 = 'icd9'  # Aspect.diagnosis
    icd10 = 'icd10'  # Aspect.diagnosis
    rxnorm = 'rxnorm'  # Aspect.medication
    rxnorm_syn = 'rxnorm-syn'  # Aspect.medication
    loinc = 'loinc'  # Aspect.Lab
    loinc_common = 'loinc-common'
    loinc_mimic = 'loinc-mimic'
    loinc_title = 'loinc-title'
    loinc_section ='loinc-section'
    loinc2hpo = 'loinc2hpo'
    shrine_icd9 = 'shrine-icd9'  # Aspect.diagnosis (subset, Harvard shrine)
    shrine_icd10 = 'shrine-icd10'  # Aspect.diagnosis (subset, Harvard shrine)
    shrine_loinc = 'shrine-loinc'  # Aspect.lab (subset, Harvard shrine)
    shrine_rxnorm = 'rxnorm-shrine'  # Aspect.drug (subset, Harvard shrine)
    npi = 'npi'
    healthcare = 'healthcare'
    medgen = 'medgen'  # Medical Genetics
    topography = 'cancer-topography'
    morphology = 'cancer-morphology'
    gene = 'gene'


class Pipeline(Enum):
    pos_tagger = 'pos_tagger'
    temporal_module = 'temporal_module'
    default_clinical = 'default_clinical'
    smoking_status = 'smoking_status'
    drug_ner = 'drug_ner'
    lab_value = 'lab_value'
    npi = 'npi_recognition'
    address = 'address'


def dest(vocabulary=Vocab.original, pipeline=Pipeline.default_clinical, host_url=UMLS_HOST) -> str:
    """
    Build a destination URL to the NLP service pipeline.
    vocabulary (source) and pipeline (function) may be custom
    :param vocabulary: see Vocab
    :param pipeline: see Autocoder
    :return:
    """
    if isinstance(vocabulary, Enum):
        vocabulary = str(vocabulary.value)
    if isinstance(pipeline, Enum):
        pipeline = str(pipeline.value)

    return f"{host_url}/{vocabulary}/{pipeline}"


class PipelineURL(Enum):
    # Aspect.multiple
    original = dest(Vocab.original)
    general = dest(Vocab.general)
    snomedct = dest(Vocab.snomedct)
    hepc = dest(Vocab.hepc)
    medgen = dest(Vocab.medgen)

    # Aspect.medication
    rxnorm = dest(Vocab.rxnorm, Pipeline.drug_ner)
    rxnorm_syn = dest(Vocab.rxnorm_syn, Pipeline.drug_ner)
    rxnorm_shrine = dest(Vocab.shrine_rxnorm, Pipeline.drug_ner)

    # Aspect.lab
    loinc = dest(Vocab.loinc, Pipeline.lab_value)
    loinc_common = dest(Vocab.loinc_common, Pipeline.lab_value)
    loinc_mimic = dest(Vocab.loinc_mimic, Pipeline.lab_value)
    loinc_shrine = dest(Vocab.shrine_loinc, Pipeline.lab_value)
    loinc2hpo = dest(Vocab.loinc2hpo, Pipeline.lab_value)
    lab_master = dest(Vocab.loinc, Pipeline.lab_value)
    general_lab_value = dest(Vocab.general, Pipeline.lab_value)

    # Aspect.diagnosis (only)
    icd9 = dest(Vocab.icd9)
    icd10 = dest(Vocab.icd10)

    # Expert curated subsets
    icd10_shrine = dest(Vocab.shrine_icd10)
    icd9_shrine = dest(Vocab.shrine_icd9)
    hepc_drug_ner = dest(Vocab.hepc, Pipeline.drug_ner)
    hepc_lab_value = dest(Vocab.hepc, Pipeline.lab_value)

    # Defaults
    pos_tagger = dest(Vocab.general, Pipeline.pos_tagger)
    temporal_module = dest(Vocab.general, Pipeline.temporal_module)
    smoking_status = dest(Vocab.snomedct, Pipeline.smoking_status)
    default_clinical = dest(Vocab.snomedct, Pipeline.default_clinical)

    # Aspect.encounter
    healthcare = dest(Vocab.healthcare)
    npi = dest(Vocab.npi, Pipeline.npi, NPI_HOST)
    address = dest(Vocab.general, Pipeline.address, ADDRESS_HOST)

    # sectionizer header
    loinc_section = dest(Vocab.loinc_section, Pipeline.default_clinical)
    loinc_title = dest(Vocab.loinc_title, Pipeline.default_clinical)


class LookupMode(Enum):
    """Possible cTAKES query modes."""
    STR = 'str'
    CODE = 'code'


def autocode(input_text: str, url=dest(), lookup_mode=LookupMode.STR, async_mode: bool = None) -> dict:
    """
    autocode text
    :param input_text:
    :param url: url of Pipeline (default is default_clinical)
    :param lookup_mode: The type of cTAKES lookup to perform (STR [default] or CODE).
    :param async_mode: Call cTAKES asynchronously.
    :return: dict JSON
    """
    if async_mode is None:
        async_mode = FeatureServiceEnv.UMLS_REQUEST_MODE.value

    if isinstance(url, Enum):
        url = str(url.value)

    data = {'inputText': input_text, 'datatype': 'plain_text', 'lookup_mode': lookup_mode.value}

    operations_logger.debug('Making autocode request to %s...', url)

    timeout = 125
    with get_session() as session:
        response = _autocode_async_mode(data, url, timeout, session=session) if async_mode \
            else _autocode_sync_mode(data, url, timeout, session=session)

    return _expand_ctakes_response(response)


def _expand_ctakes_response(ctakes_res: Dict):
    if not isinstance(ctakes_res, dict):
        return

    for k in list(ctakes_res.keys()):
        v = ctakes_res[k]

        if k == 'umlsConcepts':
            ctakes_res['umlsConcept'] = __expand_umls_concepts(v)
            del ctakes_res[k]
        elif isinstance(v, dict):
            _expand_ctakes_response(v)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    _expand_ctakes_response(item)

    return ctakes_res


# TODO: test cases for missing TUIs/TTYs
def __expand_umls_concepts(concepts):
    expanded = []

    for concept in concepts:
        tuis = concept.pop('tui')
        sab_concepts = concept.pop('sabConcepts')

        for sab_concept in sab_concepts:
            vocab_concepts = sab_concept.pop('vocabConcepts')

            for vocab_concept in vocab_concepts:
                ttys = vocab_concept.pop('tty')
                __add_new_concept(concept, sab_concept,  vocab_concept, ttys, tuis, expanded)

    return expanded


def __add_new_concept(concept, sab_concept, vocab_concept, ttys: list, tuis: list, expanded):
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


def _autocode_async_mode(data: Dict, url: str, timeout: int, session: requests.Session = None) -> dict:
    """
    Make an asynchronous autocode request.
    :param data: The request data.
    :param url: url of Pipeline (default is default_clinical).
    :param timeout: The request timeout (seconds).
    :return: dict JSON
    """
    start_time = datetime.now()

    data["async"] = "True"
    session = session if session else get_session()

    with session.post(url,
                      data=data,
                      headers={'Content-type': CONTENT_TYPE},
                      auth=(NLP_USERNAME, NLP_PASSWORD), timeout=timeout) as res:
        if res.status_code != requests.codes.ok:
            res.raise_for_status()

        response_url = f'{url}/{json.loads(res.text)["id"]}'

    while (datetime.now() - start_time).total_seconds() < timeout:
        with session.get(response_url, auth=(NLP_USERNAME, NLP_PASSWORD), timeout=timeout) as res:
            res.raise_for_status()

            response_json = json.loads(res.text)
            if 'status' not in response_json.keys() or response_json['status'] != 102:
                return ensure_compatible_response(response_json)

        time.sleep(1)

    raise HTTPError(f"Response timeout for {response_url}")


def _autocode_sync_mode(data: Dict, url: str, timeout: int, session: requests.Session = None) -> dict:
    """
    Make a synchronous autocode request.
    :param data: The request data.
    :param url: url of Pipeline (default is default_clinical).
    :param timeout: The request timeout (seconds).
    :return: dict JSON
    """
    session = session if session else get_session()
    with session.post(url,
                      data=data,
                      headers={'Content-type': CONTENT_TYPE},
                      auth=(NLP_USERNAME, NLP_PASSWORD), timeout=timeout) as res:

        res.raise_for_status()
        return ensure_compatible_response(json.loads(res.text))


def autocode_dest(input_text: str, vocab=Vocab.original, pipeline=Pipeline.default_clinical) -> dict:
    """
    :param input_text: str of clinical text
    :param vocab: (default) use ctakes "original" vocab
    :param pipeline: (default) use "default_clinical" pipeline
    :return: dict of JSON
    """
    return autocode(input_text, dest(vocab, pipeline))


def autocode_icd9_code(input_text: str) -> dict:
    return autocode(input_text, dest(Vocab.icd9, Pipeline.default_clinical), lookup_mode=LookupMode.CODE)


def autocode_icd10_code(input_text: str) -> dict:
    return autocode(input_text, dest(Vocab.icd10, Pipeline.default_clinical), lookup_mode=LookupMode.CODE)


def ensure_compatible_response(autocode_response):
    """
    JIRA/BIOMED-103
    JIRA/SANDS-156
    :param autocode_response: response from autocode_text(...)
    :return: response dict with 'content' renamed to 'results' and 'docId' renamed to 'docid'
    """

    if 'docId' in autocode_response.keys():
        autocode_response['docid'] = autocode_response.pop('docId')

    if 'content' in autocode_response.keys():
        for item in autocode_response['content']:
            if 'attributes' in item:
                if 'polarity' in item['attributes']:
                    item['attributes'].update({'relTime': ''})

        autocode_response['result'] = autocode_response.pop('content')

    return autocode_response


# Functions for API endpoints
def clinical(text):
    return autocode(text, PipelineURL.default_clinical.value)


def snomed_clinical(text):
    return autocode(text, dest(Vocab.snomedct, Pipeline.default_clinical))


def medgen_clinical(text):
    return autocode(text, dest(Vocab.medgen, Pipeline.default_clinical))


def general_clinical(text):
    return autocode(text, dest(Vocab.general, Pipeline.default_clinical))


def covid_clinical(text):
    return autocode(text, dest(Vocab.covid, Pipeline.default_clinical))

def loinc_common(text):
    return autocode(text, dest(Vocab.loinc_common, Pipeline.lab_value))

def loinc_mimic(text):
    return autocode(text, dest(Vocab.loinc_mimic, Pipeline.default_clinical))

def loinc2hpo(text):
    return autocode(text, dest(Vocab.loinc2hpo, Pipeline.default_clinical))

def lab_value(text):
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

def lab_master(text):
    return autocode(text, url=PipelineURL.lab_master.value)

def drug_ner(text, vocabulary=Vocab.rxnorm):
    """
    BIOMED-1402 drug_ner default is 'rxnorm' NOT 'rxnorm-syn'
    """
    return autocode(text, dest(vocabulary, Pipeline.drug_ner))

def drug_ner_syn(text, vocabulary=Vocab.rxnorm_syn):
    return autocode(text, dest(vocabulary, Pipeline.drug_ner))

def temporal(text):
    return autocode(text, dest(Vocab.general, Pipeline.temporal_module))


def smoking(text):
    return autocode(text, dest(Vocab.snomedct, Pipeline.smoking_status))


def speech_tags(text):
    return autocode(text, dest(Vocab.general, Pipeline.pos_tagger))


def hepc_clinical(text):
    return autocode(text, dest(Vocab.hepc, Pipeline.default_clinical))


def hepc_lab_value(text):
    return autocode(text, dest(Vocab.hepc, Pipeline.lab_value))


def loinc_lab_value(text):
    return autocode(text, dest(Vocab.loinc, Pipeline.lab_value))


def hepc_drug_ner(text):
    return autocode(text, dest(Vocab.hepc, Pipeline.drug_ner))


def problem(text: str) -> Dict:
    return autocode(text, dest(Vocab.problem, Pipeline.default_clinical))


def diagnosis(text: str) -> Dict:
    return autocode(text, dest(Vocab.diagnosis, Pipeline.default_clinical))


def topography(text: str) -> Dict:
    """
    Call the topography endpoint in text processing mode.
    :param text: The text to process.
    :return: The autocoded response.
    """
    return _topography(text)


def topography_code(text: str) -> Dict:
    """
    Call the topography endpoint in code processing mode.
    :param text: The text to process.
    :return: The autocoded response.
    """
    return _topography(text, LookupMode.CODE)


def _topography(text: str, lookup_mode=LookupMode.STR) -> Dict:
    """
    Call the topography endpoint.
    :param text: The text to process.
    :param lookup_mode: The cTAKES processing mode.
    :return: The autocoded response.
    """
    return autocode(text, dest(Vocab.topography, Pipeline.default_clinical), lookup_mode=lookup_mode)


def morphology(text: str) -> Dict:
    return _morphology(text)


def morphology_code(text: str) -> Dict:
    return _morphology(text, LookupMode.CODE)


def _morphology(text: str, lookup_mode=LookupMode.STR) -> Dict:
    """
    Call the morphology endpoint.
    :param text: The text to process.
    :param lookup_mode: The cTAKES processing mode.
    :return: The autocoded response.
    """
    return autocode(text, dest(Vocab.morphology, Pipeline.default_clinical), lookup_mode=lookup_mode)


def npi(text: str) -> Dict:
    return autocode(text, PipelineURL.npi.value)


def address(text):
    return autocode(text, PipelineURL.address.value)


def loinc_section(text: str) -> Dict:
    return autocode(text, PipelineURL.loinc_section)


def loinc_title(text: str) -> Dict:
    return autocode(text, PipelineURL.loinc_title)

# TODO: remove once new UMLS is in the wild (2020-09-23)
def covid_repr(text: str) -> Dict:
    return autocode(text, dest(Vocab.covid, Pipeline.default_clinical))


def gene(text: str) -> Dict:
    return autocode(text, dest(Vocab.gene, Pipeline.default_clinical))
