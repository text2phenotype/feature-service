from typing import Dict
from enum import Enum
from collections import OrderedDict
import unittest

from feature_service.features import history
from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.tests.files import *

from text2phenotype.common import common
from text2phenotype.ccda.section import Template as CCDATemplate, Aspect, Section as CCDASection, Person, RelTime
from text2phenotype.ccda.document import DocumentType
from text2phenotype.common.log import operations_logger

# TODO: from biomed.db import sql as db

ASPECT_TO_FILES = {
    Aspect.allergy: [BIOMED_407_ALLERGY_JSON, BIOMED_407_ALLERGY_BSV],
    'ccda': [BIOMED_407_CCDA_JSON, BIOMED_407_CCDA_BSV],
    Aspect.demographics: [BIOMED_407_DEMOGRAPHICS_JSON, BIOMED_407_DEMOGRAPHICS_BSV],
    Aspect.diagnosis: [BIOMED_407_DIAGNOSIS_JSON, BIOMED_407_DIAGNOSIS_BSV],
    Aspect.encounter: [BIOMED_407_ENCOUNTER_JSON, BIOMED_407_ENCOUNTER_BSV],
    Aspect.immunization: [BIOMED_407_IMMUNIZATION_JSON, BIOMED_407_IMMUNIZATION_BSV],
    Aspect.lab: [BIOMED_407_LAB_JSON, BIOMED_407_LAB_BSV],
    Aspect.medication: [BIOMED_407_MEDICATION_JSON, BIOMED_407_MEDICATION_BSV],
    Aspect.other: [BIOMED_407_OTHER_JSON, BIOMED_407_OTHER_BSV],
    Aspect.physical_exam: [BIOMED_407_PHYSICAL_EXAM_JSON, BIOMED_407_PHYSICAL_EXAM_BSV],
    Aspect.problem: [BIOMED_407_PROBLEM_JSON, BIOMED_407_PROBLEM_BSV],
    Aspect.procedure: [BIOMED_407_PROCEDURE_JSON, BIOMED_407_PROCEDURE_BSV],
    Aspect.social: [BIOMED_407_SOCIAL_JSON, BIOMED_407_SOCIAL_BSV],
    Aspect.treatment: [BIOMED_407_TREATMENT_JSON, BIOMED_407_TREATMENT_BSV]
}


def expert_save_dict(context_map: dict, aspect_type: Aspect):
    f = ASPECT_TO_FILES.get(aspect_type)[0]
    common.write_json(to_json(context_map), f)


def to_json(res: dict) -> Dict:
    o = OrderedDict()
    for key in sorted(res.keys()):
        o[key] = res[key].__dict__
    return o


def to_str(obj):
    if obj is None:
        return '?'

    if isinstance(obj, Enum):
        return str(obj.name)

    if isinstance(obj, list):
        obj = list(filter(None, obj))

        if len(obj) == 0:
            return '?'
        else:
            return ','.join(obj)

    return str(obj)


######################################################################################################
#
# PROCESS
#
######################################################################################################
def process_aspect(aspect_type: Aspect, suggest=None):
    expert_dict = dict()
    expert_bsv = list()

    if not suggest:
        suggest = Suggest()

    for header in list_headers(aspect_type):
        person = suggest.get_person(header)
        reltime = suggest.get_reltime(header)
        style = suggest.get_style(header)

        section = SectionContext(header, aspect_type, style, person, reltime)
        section.umls = list()  # TODO: list_umls_child(header)
        section.loinc = list()  # TODO:  list_loinc_from_text(header)

        expert_dict[header] = section
        expert_bsv.append(section.bsv())

    expert_bsv.append('\n')

    expert_save_dict(expert_dict, aspect_type)
    common.write_text('\n'.join(expert_bsv), ASPECT_TO_FILES.get(aspect_type)[1])

    return expert_dict


def list_headers(aspect_type: Aspect):
    match = list()
    for header, label in FeatureCache().aspect_map().items():
        if str(label) == str(aspect_type):
            match.append(header)
    return match


######################################################################################################
#
# TYPES
#
######################################################################################################
class StyleType(Enum):
    narrative = 'narrative'
    subheading = 'sub'
    lists = 'list'
    keyval = 'keyval'
    unique = 'unique'
    legal = 'legal'  # signature, attestation, consent


class SectionContext:
    def __init__(self, header, aspect=None, style=None, person=None, reltime=None, doctype=None):
        self.header = header
        self.aspect = aspect
        self.style = style
        self.person = person
        self.reltime = reltime
        self.doctype = [doctype]
        self.umls = None
        self.loinc = None

    def json(self):
        return {'header': str(self.header),
                'aspect': str(self.aspect),
                'style': str(self.style),
                'person': str(self.person) if self.person else None,
                'reltime': str(self.reltime) if self.reltime else None,
                'doctype': self.doctype if self.doctype else list(),
                'loinc': self.loinc,
                'umls': self.umls if self.umls else list()}

    def tsv(self):
        return self.bsv('\t')

    def bsv(self, sep='|'):
        return f"{self.header}{sep}{to_str(self.aspect)}{sep}{to_str(self.style)}{sep}{to_str(self.person)}{sep}{to_str(self.reltime)}{sep}{to_str(self.loinc)}{sep}{to_str(self.doctype)}"


######################################################################################################
#
# TYPE SUGGESTION
#
######################################################################################################

class Suggest:
    # RelTime
    HISTORY = ['HISTORY', 'PAST', 'COMPLETED', 'RECEIVED', 'PREVIOUS', 'PRIOR', 'ADMINISTERED', 'PERFORMED', 'RENDERED',
               'DEAD', 'DEATH']
    PRESENT = ['PRESENT', 'CURRENT', 'INDICATION', 'ACTIVE']
    PLAN = ['PLAN', 'AS NEEDED', 'RECOMMEND']
    ADMIT = ['ADMIT', 'ADMISSION']
    DISCHARGE = ['DISCHARGE']
    TRANSFER = ['TRANSFER', 'CONSULT']

    # Style
    LEGAL = ['SIGNED', 'SIGNATURE', 'CONSENT', 'DISCLOSURE', 'DISCLOSED', 'ALERT', 'OVERRIDE']
    REPORT = ['REPORT', 'DOCUMENT', 'NOTE', 'TITLE', 'DESCRIPTION', 'CONSULT', 'INTERPRET']
    NARRATIVE = REPORT + ['NARRATIVE', 'PLAN', 'INFORMATION']
    LIST = ['LIST']
    DOB = ['BIRTH', 'DOB', 'AGE']
    DATE = ['DATE'] + DOB
    PLACE = ['CITY', 'ZIP', 'ADDRESS']
    CONTACT = ['EMAIL', 'PHONE', 'FAX', 'NAME', 'CONTACT BY']
    UNIQUE = ['EXTERNAL ID', 'ADDRESS'] + DOB + CONTACT
    KEYVAL = PLACE + UNIQUE
    SUBHEAD = []

    # Person
    PATIENT = ['PATIENT', 'PERSONAL', 'ASSESSMENT', 'PLAN'] + UNIQUE + history.History.PERSONAL_HISTORY
    FAMILY = ['FAMILY', 'FHX'] + history.History.RELATIVES
    PROVIDER = ['PROVIDER', 'PCP', 'CARE TEAM', 'COMPLETED BY', 'CONSULT', 'REFERRED BY', 'SIGNED BY', 'FAX']

    DEFAULTS = SectionContext('?')

    def is_like(self, header: str, phrases: list):
        for utterance in phrases:
            if utterance.upper() in header.upper():
                return True
        return False

    # STYLE
    def get_style(self, header):
        if self.is_legal(header):
            return StyleType.legal
        if self.is_narrative(header):
            return StyleType.narrative
        if self.is_subhead(header):
            return StyleType.subheading
        if self.is_unique(header):
            return StyleType.unique
        if self.is_contact(header):
            return StyleType.unique
        if self.is_date(header):
            return StyleType.keyval
        if self.is_keyval(header):
            return StyleType.keyval
        if self.is_list(header):
            return StyleType.lists

        return self.DEFAULTS.style

    def is_narrative(self, header):
        return self.is_like(header, self.NARRATIVE)

    def is_subhead(self, header):
        return self.is_like(header, self.SUBHEAD)

    def is_legal(self, header):
        return self.is_like(header, self.LEGAL)

    def is_list(self, header):
        return self.is_like(header, self.LIST)

    def is_contact(self, header):
        return self.is_like(header, self.CONTACT)

    def is_unique(self, header):
        return self.is_like(header, self.UNIQUE)

    def is_keyval(self, header):
        return self.is_like(header, self.KEYVAL)

    def is_date(self, header):
        return self.is_like(header, self.DATE)

    # RELTIME
    def get_reltime(self, header):
        if self.is_admit(header):
            return RelTime.admit
        if self.is_discharge(header):
            return RelTime.discharge
        if self.is_transfer(header):
            return RelTime.transfer
        if self.is_history(header):
            return RelTime.history
        if self.is_plan(header):
            return RelTime.plan
        if self.is_present(header):
            return RelTime.present

        return self.DEFAULTS.reltime

    def is_history(self, header):
        return self.is_like(header, self.HISTORY)

    def is_present(self, header):
        return self.is_like(header, self.PRESENT)

    def is_plan(self, header):
        return self.is_like(header, self.PLAN)

    def is_admit(self, header):
        return self.is_like(header, self.ADMIT)

    def is_discharge(self, header):
        return self.is_like(header, self.DISCHARGE)

    def is_transfer(self, header):
        return self.is_like(header, self.TRANSFER)

    # PERSON
    def get_person(self, header):
        if self.is_family(header):
            return Person.family
        if self.is_provider(header):
            return Person.provider
        if self.is_patient(header):
            return Person.patient

        return self.DEFAULTS.person

    def is_patient(self, header):
        return self.is_like(header, self.PATIENT)

    def is_provider(self, header):
        return self.is_like(header, self.PROVIDER)

    def is_family(self, header):
        return self.is_like(header, self.FAMILY)


######################################################################################################
#
# UMLS
#
######################################################################################################
def tic(text: str) -> str:
    return text.replace('\'', '')


def list_sql_column(query: str, column: str) -> list:
    query = query + f' order by {column} ASC'
    return list(set([row[column] for row in db.query(query).all()]))


def list_sql_dict(query: str) -> list:
    return [row.as_dict() for row in db.query(query).all()]


def str_from_list(list_text: list) -> str:
    list_text = [f"'{text}'" for text in list_text]
    list_text = ','.join(list_text)
    list_text = f"({list_text})"
    return list_text


def list_umls_cui(text: str, min_text_len=2) -> list:
    if len(text) <= min_text_len:
        return list()
    return list_sql_column(f"select distinct CUI from umls.MRCONSO where STR='{tic(text)}'", 'CUI')


def list_umls_text(cui: str) -> list:
    return list_sql_column(f"select distinct STR as TEXT from umls.MRCONSO where CUI='{cui}'", 'TEXT')


def list_umls_cui2(cui: str, rel=None) -> list:
    if not rel:
        rel = ['SY']
    q = f"select CUI2 as CUI from umls.MRREL where REL in {str_from_list(rel)} and CUI1='{cui}'"
    return list_sql_column(q, 'CUI')


def list_umls_child(header: str):
    umls = list()
    for cui in list_umls_cui(header):
        for child in list_umls_cui2(cui):
            for text in list_umls_text(child):
                umls.append(text)
    return umls


def list_loinc_from_code(code: str, select='CUI') -> list:
    q = f"select distinct {select} from umls.MRCONSO where CODE='{code}' and SAB='LNC'"
    return list_sql_column(q, select)


def list_loinc_from_text(text: str, select='CODE') -> list:
    q = f"select distinct {select} from umls.MRCONSO where STR='{tic(text)}' and SAB='LNC'"
    return list_sql_column(q, select)


def list_loinc_concepts(code: str):
    res = dict()
    for cui in list_loinc_from_code(code):
        res[cui] = list()
        q = f"SELECT distinct SAB, CODE, STT, ISPREF, STR as TEXT from umls.MRCONSO where CUI='{cui}'"
        for match in db.query(q).all():
            res[cui].append(match.as_dict())
    return res


######################################################################################################
#
# CCDA
#
######################################################################################################
def ccda_section_context(t: CCDATemplate, title: str):
    loinc = t.section
    umls = list()  # TODO: list_loinc_from_code(loinc, 'STR')
    header = ccda.get_section_title_pretty(title)

    style = None
    if t.narrative:
        style = StyleType.narrative
    else:
        if 'list' in header.lower():
            style = StyleType.lists
    if t.person is None:
        operations_logger.error(t.__dict__)
        raise Exception('which person?')

    context = SectionContext(header, t.aspect, style, t.person, t.rel_time, doctype='CCDA')
    context.loinc = loinc
    context.umls = umls

    context.bsv()

    return context


def ccda_document_context(doc_enum, doctype):
    res = dict()

    for section_enum in doc_enum:
        loinc = section_enum.value
        umls = list()  # TODO: list_loinc_from_code(loinc, 'STR')
        header = ccda.get_section_title_pretty(section_enum.name)

        t = ccda.section_template_map[section_enum.value]

        style = None
        if t.narrative:
            style = StyleType.narrative
        else:
            if 'list' in header.lower():
                style = StyleType.lists

        if t.person is None:
            t.person = Person.patient

        context = SectionContext(header, t.aspect, style, t.person, t.rel_time, doctype)
        context.loinc = loinc
        context.umls = umls

        res[header] = context
    return res


def ccda_loinc_context():
    # History and physical note
    # mysql> select * from MRREL_lnc_doc_concept where CODE='34117-2';
    #
    # mysql> select distinct CODE from MRREL_lnc_doc_concept where RELA= 'class_of';
    pass


######################################################################################################
#
# Unit Test
#
######################################################################################################

class TestBiomed407(unittest.TestCase):

    ######################################################################################################
    #
    # MERGE
    #
    ######################################################################################################
    def test_merge_everything(self):
        mu2 = common.read_json(ASPECT_TO_FILES.get('ccda')[0])
        merged = dict()

        for a in Aspect.get_active_aspects():
            aspect_json = ASPECT_TO_FILES.get(a)[0]
            for header, attrs in common.read_json(aspect_json).items():
                merged[header] = attrs

                if header in mu2:
                    merged[header]['doctype'] = list(set(['CCDA'] + mu2[header]['doctype']))
                    merged[header]['loinc'] = mu2[header]['loinc']

                    merged[header]['umls'] += mu2[header]['umls']
                    merged[header]['umls'] = list(set(merged[header]['umls']))

                    # TODO: which test validations should be here?
                    # self.assertEqual(mu2[header]['aspect'], merged[header]['aspect'], f"mismatch {header} @ {attrs}")

        operations_logger.info(
            f'Merged standard (MU2) with physician styles of writing: headings = {len(merged.keys())}')
        common.write_json(merged, 'code/feature-service/feature_service/resources/files/BIOMED-407.merged.json')

    ######################################################################################################
    #
    # C-CDA / CCD
    #
    ######################################################################################################
    def test_ccda(self):
        merged = dict()

        for ccda_section in CCDASection:
            context = ccda_section_context(ccda_section.value, ccda_section.name)
            merged[context.header] = context

        for doc_type in DocumentType:
            doc_class = ccda.get_document_class(doc_type)

            for header, context in ccda_document_context(doc_class, doc_type.name).items():
                if header not in merged.keys():
                    merged[header] = context
                else:
                    merged[header].doctype.append(doc_type.name)

        out_bsv = list()
        map_bsv = OrderedDict()

        for header in sorted(merged.keys()):
            out_bsv.append(merged[header].bsv())
            map_bsv[header] = merged[header].__dict__
        file_ccda = ASPECT_TO_FILES.get('ccda')[0]
        common.write_json(map_bsv, file_ccda)
        common.write_text('\n'.join(out_bsv), file_ccda.replace('.json', '.bsv'))

    ######################################################################################################
    #
    # OTHER
    #
    ######################################################################################################
    def test_other(self):
        suggest = Suggest()
        suggest.NARRATIVE += ['SOAP', 'COURSE', 'HISTORY', 'OBJECTIVE', 'NOTE']
        suggest.SUBHEAD += ['SYMPTOMS']
        suggest.KEYVAL += ['DD', 'TD']

        suggest.PROVIDER += ['QUESTION']
        suggest.PATIENT += ['ANSWER', 'CLINICAL', 'NOTE', 'HISTORY', 'SYMPTOMS', 'DISPOSITION', 'OBJECTIVE',
                            'SUBJECTIVE', 'PSYCHIATRIC']

        suggest.PRESENT += ['SYMPTOMS']
        suggest.PLAN += ['SERVICES DUE']

        process_aspect(Aspect.other)

    ######################################################################################################
    #
    # SOCIAL
    #
    ######################################################################################################
    def test_social(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = None
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = None

        habbits = ['HABIT', 'DIET', 'EAT', 'TOBACCO', 'SMOK', 'DRINK', 'ALCOHOL']

        suggest.NARRATIVE += ['COMMENT']
        suggest.HISTORY += ['PSH', 'SHX']

        suggest.SUBHEAD += habbits
        suggest.PRESENT += habbits

        process_aspect(Aspect.social, suggest)

    ######################################################################################################
    #
    # TREATMENT
    #
    ######################################################################################################
    def test_treatment(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = None
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = None

        instructions = ['FOLLOW', 'RECOMMNED', 'INSTRUCTION', 'DIET', 'REMINDER', 'PLAN']

        suggest.NARRATIVE += ['TREATMENT']
        suggest.PLAN += instructions
        suggest.NARRATIVE += instructions

        process_aspect(Aspect.treatment, suggest)

    ######################################################################################################
    #
    # PROCEDURE
    #
    ######################################################################################################
    def test_procedure(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = None
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = None

        suggest.SUBHEAD += ['ECG', 'EKG', 'ECHO', 'CXR', 'MRI', 'XRAY', 'X-RAY']
        suggest.NARRATIVE += ['FINDINGS']

        process_aspect(Aspect.procedure, suggest)

    ######################################################################################################
    #
    # LAB
    #
    ######################################################################################################
    def test_lab(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = StyleType.lists
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = None

        suggest.PRESENT += ['BMI', 'PREOPERATIVE', 'NOTABLE', 'PERTINENT']
        suggest.PLAN += ['LABS TO FU']
        suggest.LIST += ['INFORMATION', 'NOTE']
        suggest.NARRATIVE += ['PATHOLOGY']

        process_aspect(Aspect.lab, suggest)

    ######################################################################################################
    #
    # IMMUNIZATION
    #
    ######################################################################################################
    def test_immunization(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = StyleType.lists
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = RelTime.history

        process_aspect(Aspect.immunization, suggest)

    ######################################################################################################
    #
    # ALLERGY
    #
    ######################################################################################################
    def test_allergy(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = None
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = RelTime.present

        suggest.KEYVAL += ['NKDA']

        process_aspect(Aspect.allergy, suggest)

    ######################################################################################################
    #
    # MEDICATION
    #
    ######################################################################################################
    def test_medication(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = StyleType.lists
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = RelTime.present

        suggest.PLAN += ['ORDER']

        process_aspect(Aspect.medication, suggest)

    ######################################################################################################
    #
    # PROBLEM
    #
    ######################################################################################################
    def test_problem(self):

        suggest = Suggest()
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.style = StyleType.narrative

        suggest.NARRATIVE += ['COURSE']

        suggest.ADMIT += ['CC', 'CHIEF', 'COMPLAINT', 'REASON FOR VISIT']
        suggest.DISCHARGE += ['HOSPITALIZATION']
        suggest.TRANSFER += ['INDICATION', 'COURSE', 'REFER']

        soap_now = ['SUBJECTIVE', 'OBJECTIVE', 'OBSERVATIONS', 'FINDINGS', 'ASSESSMENT', 'IMPRESSION', 'CONCLUSIONS']

        suggest.PRESENT += ['SIGNIFICANT', 'LIST', 'PRINCIPAL', 'CARDIOVASCULAR', 'ASSOCIATED', 'SUMMARY',
                            'RISK'] + soap_now
        suggest.HISTORY += ['PMH', 'FHX']

        suggest.FAMILY += ['FHX']

        process_aspect(Aspect.problem, suggest)

    ######################################################################################################
    #
    # DIAGNOSIS
    #
    ######################################################################################################
    def test_diagnosis(self):
        suggest = Suggest()
        suggest.DEFAULTS.style = StyleType.narrative
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = RelTime.present

        suggest.HISTORY = history.History().HISTORY

        process_aspect(Aspect.diagnosis, suggest)

    ######################################################################################################
    #
    # PHYSICAL EXAM
    #
    ######################################################################################################
    def test_physical_exam(self):

        suggest = Suggest()
        suggest.DEFAULTS.style = StyleType.narrative
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = RelTime.present

        suggest.NARRATIVE += ['PHYSICAL', 'FINDINGS']

        suggest.KEYVAL = ['HEIGHT', 'WEIGHT', 'REFLEX', 'PULSE', 'BLOOD PRESSURE', 'BP']

        suggest.SUBHEAD = ['GENERAL', 'GEN',
                           'VITALS', 'VITAL SIGN',
                           'MENTAL', 'COGNIT',
                           'OPHTHALMOLOGY',
                           'SENSORY', 'COORDINATION', 'GAIT',
                           'MUSCULOSKELETAL', 'SKIN',
                           'ENDOCRINE', 'ENDO',
                           'HEENT',
                           'HEAD', 'CRANIAL', 'NEURO', 'CEREBELLAR', 'CNS',
                           'EARS',
                           'EYE EXAM', 'EYES',
                           'NOSE',
                           'THROAT',
                           'NECK',
                           'CARDIOVASCULAR', 'HEART', 'CARDIAC', 'CV', 'VS',
                           'LUNG', 'LUNGS', 'RESP', 'PULMONARY', 'PLUM',
                           'CHEST', 'BREAST',
                           'ABDOMEN', 'ABD',
                           'BACK',
                           'RENAL',
                           'PELVIC', 'GENITOURINARY',
                           'GASTRO', 'GI', 'RECTAL',
                           'EXTREMITIES', 'EXT',
                           'FOOT']

        process_aspect(Aspect.physical_exam, suggest)

    ######################################################################################################
    #
    # DEMOGRAPHICS
    #
    ######################################################################################################
    def test_demographics(self):

        suggest = Suggest()
        suggest.DEFAULTS.style = StyleType.keyval
        suggest.DEFAULTS.person = Person.patient
        suggest.DEFAULTS.reltime = RelTime.present

        suggest.LIST = ['DOCUMENT', 'DEMOGRAPHICS', 'INFO', 'INFORMATION', 'DATA', 'IDENTIFICATION', 'IDENTIFYING']
        suggest.SUBHEAD = ['INSURANCE', 'INS', 'PAYMENT', 'PAYER', 'BENEFITS', 'COMPLETED', 'STATUS', 'CONTACT']
        suggest.LEGAL = ['CONSENT', 'DISCLOSURE']
        suggest.UNIQUE = ['SSN', 'S.S.', 'SOCIAL', 'SECURITY', 'NUMBER', 'SOC SEC', 'PHONE', 'MOBILE', 'EMAIL',
                          'ADDRESS'] + ['ID', 'MRN', 'IDENTIF', 'RECORD']
        suggest.DATE = ['DOB', 'DATE', 'BIRTH', 'AGE']
        suggest.KEYVAL = ['GENDER', 'SEX', 'CITY', 'LANG', 'RACE', 'ETHNICITY', 'PAYMENT', 'JOB', 'WORK', 'OCCUPATION',
                          'HOMELESS']

        process_aspect(Aspect.demographics, suggest)

    ######################################################################################################
    #
    # ENCOUNTER
    #
    ######################################################################################################
    def test_encounter(self):

        suggest = Suggest()

        suggest.ADMIT += ['ARRIV', 'REGISTRATION', 'HOSPITALIZ']
        suggest.TRANSFER += ['REFER', 'CONSULT']

        facility = ['FACILITY', 'DEPARTMENT', 'ROOM', 'BUILDING', 'CAMPUS']

        suggest.PLACE = ['STATE', 'ZIP', 'POSTAL'] + facility

        suggest.LEGAL += ['COMPLETED', 'DICTATATED', 'CONSENT', 'SIGNED']

        suggest.UNIQUE += ['NPI', 'PROVIDER ID', 'FAX']

        suggest.PROVIDER += suggest.UNIQUE + facility + ['FAX', 'SIGN', 'CONSULT', 'ATTEND', 'REFER', 'SEEN', 'ENTERED',
                                                         'DICTAT',
                                                         'STAFF', 'NOTIF', 'CARE TEAM']

        suggest.FAMILY += ['DELIVERY DATE']

        suggest.PATIENT = suggest.ADMIT + suggest.DISCHARGE
        suggest.PATIENT += ['CONSENT', 'CODE', 'STATE', 'ZIP', 'POSTAL'] + ['PAYER', 'INSURANCE']

        suggest.PRESENT += suggest.LEGAL + suggest.UNIQUE + suggest.PATIENT

        suggest.SUBHEAD += ['ENCOUNTER', 'VISIT']
        suggest.KEYVAL += ['CODE', 'TIME'] + suggest.PROVIDER + suggest.PATIENT
        suggest.UNIQUE += suggest.PROVIDER + suggest.PATIENT

        process_aspect(Aspect.encounter, suggest)

    ###############################################################################
    #
    # Match RELAXED (section aspect headers)
    #
    ###############################################################################
    @staticmethod
    def match_relaxed_deprecated(text: str, min_char_length=3):
        """
        :param text:
        :param min_char_length:
        :return:
        """
        matches = dict()
        length = 0

        for line in text.splitlines(keepends=True):

            index = range(length, length + len(line))

            if len(line) >= min_char_length:
                if ':' in line:
                    matches[index] = line.split(':')

                if line.isupper():
                    matches[index] = [line]

            length += len(line)

        return matches
