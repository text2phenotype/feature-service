import json
import os
import pickle
from typing import List, Dict
from zipfile import ZipFile

import joblib
from sklearn.feature_extraction.text import CountVectorizer

from text2phenotype.common.log import operations_logger
from text2phenotype.common import common
from text2phenotype.common.singleton import singleton, SingletonCache

from feature_service.common import bsv
from feature_service.aspect.tokenizer import Tokenizer
from feature_service.hep_c.answers import QuestionAnswers
from feature_service.resources import (PERSON_NAMES, ZIP_CODES, REGEX_DATE, TF_CCDA, TF_I2B2, REGEX_ICD, REGEX_BP,
                                       TF_MRCONSO, TF_MTSAMPLE, TF_NPI_ADDRESS, TF_NPI_CITY, TF_NPI_FIRST_NAME,
                                       TF_NPI_LAST_NAME, TF_NPI_PHONE, TF_PATIENTS_FIRST_NAME, TF_PATIENTS_LAST_NAME,
                                       TF_SNOMED_CORE_DISORDER, TF_SNOMED_CORE_FINDING, TF_SNOMED_CORE_PROCEDURE,
                                       TF_USA_CITIES, TF_USA_STATES, EXPERT_SECTIONIZER, ASPECT_VOCAB_MODEL,
                                       ASPECT_CLASSIFIER_MODEL, STOP_WORDS, HCV_GRAMMAR_JSON, REGEX_URL,
                                       WORD2VEC_MIMIC, REGEX_TOPOGRAPHY, REGEX_MORPHOLOGY, REGEX_TNM,
                                       LATIN_RESOURCES, UNITS_OF_MEASURE, DOCUMENT_TYPE_VOCAB_MODEL, REGEX_GRADE_TERMS,
                                       REGEX_GRADE_CODE, REGEX_SMOKING, REGEX_CONTACT_INFO, REGEX_HOSPITAL_PERSONNEL,
                                       REGEX_PATIENT, REGEX_GENDER, REGEX_AGE, REGEX_ADDRESS, REGEX_HOSPITAL,
                                       REGEX_GRAMMAR, REGEX_ANALYTE, REGEX_COVID, REGEX_COVID_DEVICE, REGEX_IMAGING,
                                       REGEX_FINDING, LOINC_SECTIONS, LOINC_DOC_SECTIONS,
                                       REGEX_COVID_MANUFACTURERS)
from feature_service.common.latin import LatinTypes


@singleton
class FeatureCache(SingletonCache):
    def __init__(self, preload: bool = False):
        super().__init__()
        if preload:
            self.preload()

    def aspect_map(self) -> Dict:
        """
        :return: dict having entry[header]=Aspect
        """
        key = 'aspect|ASPECT_MAP'
        if not self.exists(key):
            _sections = self.expert_sectionizer()
            _aspects = dict()

            for _header, _detail in _sections.items():
                _aspects[_header] = _detail['aspect']

            self.put(key, _aspects)

        return self.get(key)

    def aspect_vectorizer(self):
        key = 'aspect|vectorizer'
        return self.__get_vectorizer(key, self.aspect_vocabulary())

    def document_vectorizer(self, train: bool = False, model_file_name: str = DOCUMENT_TYPE_VOCAB_MODEL):
        if train:
            vocabulary = None
        else:
            vocabulary = self.document_classifier_vocab_word_index(model_file_name)
        return self.__get_vectorizer(model_file_name, vocabulary)

    def __get_vectorizer(self, key: str, vocabulary):
        key += '_vectorizer'
        if not self.exists(key):
            value = CountVectorizer(binary=False,
                                    lowercase=True,
                                    decode_error='replace',
                                    tokenizer=Tokenizer(self.aspect_stop_words()),
                                    vocabulary=vocabulary)
            self.put(key, value)

        return self.get(key)

    def aspect_vocabulary(self):
        key = 'aspect|vocabulary'

        if not self.exists(key):
            self.put(key, joblib.load(ASPECT_VOCAB_MODEL))

        return self.get(key)

    def document_classifier_vocab_word_index(self, model_file_name: str = None):
        document_type_vocab_file_name = f'{model_file_name}_vocabulary.sav'
        if not self.exists(document_type_vocab_file_name):
            operations_logger.info(f'Caching document vocab model: {document_type_vocab_file_name}')
            self.put(document_type_vocab_file_name, pickle.load(open(document_type_vocab_file_name, 'rb'),
                                                                encoding='utf8'))

        return self.get(document_type_vocab_file_name)

    def document_classifier_vocab_model(self, model_file_name):

        if not self.exists(model_file_name):
            operations_logger.info(f'Caching document vocab index: {model_file_name}')
            self.put(model_file_name, joblib.load(model_file_name))

        return self.get(model_file_name)

    def aspect_classifier(self, model_file_path: str = None):
        """
        Load and cache the aspect classifier

        :param model_file_path: str, full path to a target model estimator to load
        """
        key = 'aspect|classifier'

        if not self.exists(key):
            if not model_file_path:
                model_file_path = ASPECT_CLASSIFIER_MODEL
            # value = common.read_pkl(model_file_path)
            value = joblib.load(model_file_path)
            self.put(key, value)

        return self.get(key)

    def aspect_stop_words(self):
        key = 'aspect|stop_words'
        if not self.exists(key):
            stop_words = []
            with open(STOP_WORDS) as stop_words_file:
                for line in stop_words_file:
                    stop_words.append(line.strip())
            self.put(key, stop_words)
        return self.get(key)

    def regex_covid_rules(self) -> Dict:
        return self.__regex_rules('regex_covid', REGEX_COVID)

    def regex_covid_device_rules(self) -> Dict:
        return self.__regex_rules('regex_covid_device', REGEX_COVID_DEVICE)

    def regex_date_rules(self) -> Dict:
        """
        :return: dict, entry[REGEX_NAME]=pattern
        """
        return self.__regex_rules('regex_dates', REGEX_DATE)

    def regex_finding_rules(self):
        return self.__regex_rules('regex_finding', REGEX_FINDING)

    def regex_covid_manufacturers(self):
        return self.__regex_rules('regex_finding', REGEX_COVID_MANUFACTURERS)

    def regex_topography_rules(self):
        return self.__regex_rules('regex_topography', REGEX_TOPOGRAPHY)

    def regex_morphology_rules(self):
        return self.__regex_rules('regex_morphology', REGEX_MORPHOLOGY)

    def regex_grade_code_rules(self):
        return self.__regex_rules('regex_grade', REGEX_GRADE_CODE)

    def regex_grade_term_rules(self):
        return self.__regex_rules('regex_grade_terms', REGEX_GRADE_TERMS)

    def regex_tnm_stage_rules(self):
        return self.__regex_rules('regex_TNM_stage', REGEX_TNM)

    def regex_imaging_rules(self):
        return self.__regex_rules('regex_imaging', REGEX_IMAGING)

    def regex_smoking(self):
        return self.__regex_rules('regex_smoking', REGEX_SMOKING)

    def regex_contact_info(self):
        return self.__regex_rules('regex_contact_info', REGEX_CONTACT_INFO)

    def regex_hospital_personnel(self):
        return self.__regex_rules('regex_hospital_personnel', REGEX_HOSPITAL_PERSONNEL)

    def regex_patient(self):
        return self.__regex_rules('regex_patient', REGEX_PATIENT)

    def regex_gender(self):
        return self.__regex_rules('regex_gender', REGEX_GENDER)

    def regex_age(self):
        return self.__regex_rules('regex_age', REGEX_AGE)

    def regex_address(self):
        return self.__regex_rules('regex_address', REGEX_ADDRESS)

    def regex_hospital(self):
        return self.__regex_rules('regex_address', REGEX_HOSPITAL)

    def regex_grammar(self):
        return self.__regex_rules('regex_grammar', REGEX_GRAMMAR)

    def regex_url(self):
        return self.__regex_rules('regex_url', REGEX_URL)

    def regex_icd(self):
        return self.__regex_rules('regex_icd', REGEX_ICD)

    def regex_bp(self):
        return self.__regex_rules('regex_bp', REGEX_BP)

    def regex_analyte(self):
        return self.__regex_rules('regex_analyte', REGEX_ANALYTE)

    def __regex_rules(self, package: str, re_file: str) -> Dict:
        """
        :param package: The cache package.
        :param re_file: File containing regular expressions.
        :return: dict, entry[REGEX_NAME]=pattern
        """
        key = f'{package}|{re_file}'

        if not self.exists(key):
            self.put(key, self.parse_regex_file(re_file))

        return self.get(key)

    def person_names(self) -> List:
        """
        :return: list of person names from US census
        """
        key = 'person|NAMES_FILE'

        if not self.exists(key):
            self.put(key, common.read_text(PERSON_NAMES).splitlines())
        return self.get(key)

    def zip_codes_dict(self) -> Dict:
        """
        :return: dict having entry[ZipCode]= {city/state/...}
        """
        return self.__get_json('locations|ZIPCODES_FILE', ZIP_CODES)

    def zip_codes_list(self) -> List:
        """
        :return: list of zipcodes
        """
        return list(self.zip_codes_dict().keys())

    def zip_codes_city(self) -> List:
        """
        :return: list of cities from ZIPCODES_FILE
        """
        key = 'locations|ZIPCODES_CITY'

        if not self.exists(key):
            cities = [zip5['city'] for zip5 in self.zip_codes_dict().values()]
            self.put(key, cities)

        return self.get(key)

    def tf_file(self, file_path: str) -> Dict:
        """
        :return: dict where entry['term'] = int(frequency)
        """
        return self.__get_json(f'tf|{file_path}', file_path)

    def tf_i2b2(self):
        """
        I2B2 corpus term frequency TODO: DOCTNOTE: which challenge? DEID?
        :return: dict where entry[term] = int(frequency)
        """
        return self.tf_file(TF_I2B2)

    def tf_ccda(self):
        """
        C-CCDA standard formatted data term frequencies from CCDA parser
        :return: dict where entry[term] = int(frequency)
        """
        return self.tf_file(TF_CCDA)

    def tf_mtsamples(self):
        """
        mtsamples.com medical transcription samples
        :return: dict where entry[term] = int(frequency)
        """
        return self.tf_file(TF_MTSAMPLE)

    def tf_mrconso(self):
        """
        UMLS Concept Strings (more than 2 million )
        :return: dict where entry[term] = int(frequency)
        """
        return self.tf_file(TF_MRCONSO)

    def tf_npi_address(self):
        """
        NPI National Provider ID ( Address )
        :return: dict where entry[addressToken] = int(frequency)
        """
        return self.tf_file(TF_NPI_ADDRESS)

    def tf_npi_first_name(self):
        """
        NPI National Provider ID ( First Name )
        :return: dict where entry[firstName] = int(frequency)
        """
        return self.tf_file(TF_NPI_FIRST_NAME)

    def tf_npi_last_name(self):
        """
        NPI National Provider ID ( Last Name )
        :return: dict where entry[lastName] = int(frequency)
        """
        return self.tf_file(TF_NPI_LAST_NAME)

    def tf_npi_phone(self):
        """
        NPI National Provider ID ( Phone )
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_NPI_PHONE)

    def tf_npi_city(self):
        """
        NPI National Provider ID ( City Location )
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_NPI_CITY)

    def tf_patients_first_name(self):
        """
        Patients First Name TODO: DOCNOTE andy DEID original source?
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_PATIENTS_FIRST_NAME)

    def tf_patients_last_name(self):
        """
        Patients Last Name TODO: DOCNOTE andy DEID original source?
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_PATIENTS_LAST_NAME)

    def tf_usa_cities(self):
        """
        USA Cities TODO: DOCNOTE original source zipcodes?
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_USA_CITIES)

    def tf_usa_states(self):
        """
        USA Cities TODO: DOCNOTE original source zipcodes?
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_USA_STATES)

    def tf_snomed_vocab_disorder(self):
        """
        disorder vocab from snomed core list
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_SNOMED_CORE_DISORDER)

    def tf_snomed_vocab_finding(self):
        """
        finding vocab from snomed core list
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_SNOMED_CORE_FINDING)

    def tf_snomed_vocab_procedure(self):
        """
        procedure vocab from snomed core list
        :return: dict where entry['term'] = int(frequency)
        """
        return self.tf_file(TF_SNOMED_CORE_PROCEDURE)

    def expert_sectionizer(self):
        return self.__get_json('expert|sectionizer', EXPERT_SECTIONIZER)

    def hcv_grammar(self):
        return self.__get_json('hcv_grammar_json', HCV_GRAMMAR_JSON)

    def hep_c_answers(self):
        key = 'hep_c_answers'
        if not self.exists(key):
            self.put(key, QuestionAnswers())
        return self.get(key)

    @staticmethod
    def parse_regex_file(file_regex: str) -> Dict[str, str]:
        """
        https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-6-12

        Parse file with regex patterns and create cache
        :param file_regex: Path to the file with RegEx patterns
        :return: Dictionary: (replace_token) => (pattern)
        """
        result = {}
        if os.path.exists(file_regex):

            with open(file_regex) as fp:

                for line in fp:
                    if len(line) > 0 and line[0] == '#':
                        pattern_line = fp.readline()
                        result['$' + line[1:].strip('\n')] = pattern_line.strip('\n')
        else:
            operations_logger.error(f'The file with RegEx patterns does NOT exist!: {file_regex}')

        return result

    def word2vec_mimic(self):
        """
        load a pre-trained word embedding (word2vec tuned on mimic)
        :return:
        """
        key = 'word2vec_mimic'

        if not self.exists(key):
            val = WORD2VEC_MIMIC
            with ZipFile(val, 'r') as zipObj:
                for filename in zipObj.namelist():
                    with zipObj.open(filename) as f:
                        data = f.read()
                        d = json.loads(data)
            operations_logger.info(f"{key}|{val}")

            self.put(key, d)

        return self.get(key)

    def load_latin_resource(self, resource_name, resource_path):
        key = f'latin_{resource_name}|{resource_path}'
        if not self.exists(key):
            operations_logger.info(f'cache_bsv {key}')
            self.put(key, bsv.parse_bsv_latin_resource(resource_path))
        return self.get(key)

    def latin_resources(self):
        key = 'latin|cache_all'
        merged = list()
        if not self.exists(key):
            for lt in LatinTypes.__members__:
                merged = merged + self.load_latin_resource(lt, os.path.join(LATIN_RESOURCES, f'BIOMED-848.{lt}.bsv'))
            self.put(key, merged)
        return self.get(key)

    def units_of_measure_resource(self) -> List:
        """
        :return: list of units
        """
        key = 'units|UNITS_FILE'

        if not self.exists(key):
            units_list = [unit['UNIT'][0].lower() for unit in bsv.parse_bsv_list(UNITS_OF_MEASURE, 'ID|UNIT')]
            self.put(key, units_list)
        return self.get(key)

    def loinc_sections(self) -> dict:
        return self.__get_json('loinc_sections', LOINC_SECTIONS)

    def loinc_doc_sections(self) -> dict:
        return self.__get_json('loinc_doc_sections', LOINC_DOC_SECTIONS)

    def __get_json(self, key: str, json_file: str) -> dict:
        if not self.exists(key):
            self.put(key, common.read_json(json_file))

        return self.get(key)

    def preload(self):
        self.aspect_classifier()
        self.aspect_map()
        self.aspect_vectorizer()
        self.aspect_vocabulary()
        self.aspect_stop_words()
        self.person_names()
        self.tf_ccda()
        self.tf_i2b2()
        self.tf_mrconso()
        self.tf_mtsamples()
        self.tf_npi_address()
        self.tf_npi_city()
        self.tf_npi_first_name()
        self.tf_npi_last_name()
        self.tf_npi_phone()
        self.tf_usa_cities()
        self.tf_usa_states()
        self.tf_patients_first_name()
        self.tf_patients_last_name()
        self.zip_codes_dict()
        self.regex_rules()
        self.tf_snomed_vocab_disorder()
        self.tf_snomed_vocab_finding()
        self.tf_snomed_vocab_procedure()
        self.hcv_grammar()
        self.hep_c_answers()
        self.regex_topography_rules()
        self.regex_morphology_rules()
        self.regex_tnm_stage_rules()
        self.latin_resources()
        self.units_of_measure_resource()
