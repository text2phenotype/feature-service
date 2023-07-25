import csv
import datetime
import os
import random
import re
import unittest
from typing import Dict, List
from collections import defaultdict

from text2phenotype.annotations.file_helpers import Annotation
from text2phenotype.common import common
from text2phenotype.common.log import operations_logger

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.tests.experiment.i2b2.surrogates import (PatientSurrogates, PATIENT_FIELDS, DOCTOR_REQ_FIELDS,
                                                              read_names, PersonFields, get_random_hospital,
                                                              HospitalFields, flipcoin, abbreviate, get_random_person,
                                                              DoctorSurrogates, HospitalSurrogates)


class _Patient(object):
    def __init__(self):
        self.dob = None
        self.gender = None
        self.age_at_first_admin = None
        self.age_at_last_discharge = None
        self.admissions = list()


class TestBiomed647(unittest.TestCase):
    """Test class for performing surrogate injection on MIMIC-III patient records."""
    _PHI_PATTERN = re.compile('\[\*{2}.+?\*{2}\]')
    __SHORT_DATE_PATTERN = re.compile('\d{1,2}-\d{1,2}$')
    __DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    __ROOT_OUT_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'mimic', 'biomed_674_records')
    __PATIENTS = PatientSurrogates()
    __DOCTORS = DoctorSurrogates()
    __HOSPITALS = HospitalSurrogates()

    def __init__(self, *args, **kwargs):
        super(TestBiomed647, self).__init__(*args, **kwargs)

        self._hospitals = dict()
        self._doctor_cache = defaultdict(list)
        self._year_offsets = dict()
        self._patients = dict()
        self._names_by_gender = None
        self._patient_surrogates = dict()
        self._demo_type_counts = defaultdict(int)
        self._phi_type_counts = defaultdict(int)
        self._patient_surrogates = dict()
        self.__last_doc = None
        self.__last_doc_name_field = None

        self._CCUs = ('CCU', 'CSRU', 'MICU', 'SICU', 'TSICU')
        self._STATES = ('Alabama', 'AL', 'Alaska', 'AK', 'Arizona', 'AZ', 'Arkansas', 'AR', 'California', 'CA',
                        'Colorado', 'CO', 'Connecticut', 'CT', 'Delaware', 'DE', 'Florida', 'FL', 'Georgia', 'GA',
                        'Hawaii', 'HI', 'Idaho', 'ID', 'Illinois', 'IL', 'Indiana', 'IN', 'Iowa', 'IA', 'Kansas',
                        'KS', 'Kentucky', 'KY', 'Louisiana', 'LA', 'Maine', 'ME', 'Maryland', 'MD', 'Massachusetts',
                        'MA', 'Michigan', 'MI', 'Minnesota', 'MN', 'Mississippi', 'MS', 'Missouri', 'MO', 'Montana',
                        'MT', 'Nebraska', 'NE', 'Nevada', 'NV', 'New Hampshire', 'NH', 'New Jersey', 'NJ',
                        'New Mexico', 'NM', 'New York', 'NY', 'North Carolina', 'NC', 'North Dakota', 'ND', 'Ohio',
                        'OH', 'Oklahoma', 'OK', 'Oregon', 'OR', 'Pennsylvania', 'PA', 'Rhode Island', 'RI',
                        'South Carolina', 'SC', 'South Dakota', 'SD', 'Tennessee', 'TN', 'Texas', 'TX', 'Utah', 'UT',
                        'Vermont', 'VT', 'Virginia', 'VA', 'Washington', 'WA', 'West Virginia', 'WV', 'Wisconsin',
                        'WI', 'Wyoming', 'WY')
        self._OLD_AGES = tuple(str(age) for age in range(90, 106))
        self._UNIVERSITIES = ('Boston University', 'Boston College', 'Harvard', 'MIT', 'Northeastern', 'Tufts')
        self._HOLIDAYS = ('Chrismas', 'New Years', 'Memorial Day', '4th of July', 'Labor Day', 'Thanksgiving')
        self._WARDS = ('AMU', 'AEC', 'Coronary Care', 'HDU', 'ICU', 'Geriatrics')
        self._COMPANIES = ('Barnes Group', 'Headwaters Inc.', 'Knowles Corporation',
                           'Zoetis Inc.', 'Ventas Inc.', 'PartnerRe Ltd.')
        self._COUNTRIES = ('Mexico', 'Canada')
        self._DOMAINS = (
            'text2phenotype.com', 'gmail.com', 'yahoo.com', 'hotmail.com', 'protonmail.com', 'bwh.org', 'harvard.edu')

    @unittest.skip
    def test_inject_surrogates(self):
        """Perform the injection."""
        operations_logger.info("Getting valid surrogates...")
        self._get_valid_surrogates()

        self._names_by_gender = read_names(os.path.join(os.path.dirname(__file__), '..',
                                                        'us-likelihood-of-gender-by-name-in-2014.csv'))

        self._read_patient_dates()
        self._filter_neonates()
        self._get_year_adj()
        self.__process_patient_notes()

        operations_logger.info(f'Demographics counts: {self._demo_type_counts}')
        operations_logger.info(f'PHI counts: {self._phi_type_counts}')

    def _get_valid_surrogates(self):
        """Pre-filter surrogates that are missing required information."""
        for i in range(len(self.__PATIENTS.first_name())):
            person = dict()
            person[PersonFields.FIRST_NAME] = self.__PATIENTS.first_name()[i].strip()
            person[PersonFields.LAST_NAME] = self.__PATIENTS.last_name()[i].strip()
            person[PersonFields.MIDDLE_NAME] = self.__PATIENTS.middle_name()[i].strip()
            person[PersonFields.STREET] = self.__PATIENTS.address()[i].strip()
            person[PersonFields.CITY] = self.__PATIENTS.city()[i].strip()
            person[PersonFields.STATE] = self.__PATIENTS.state()[i].strip()
            person[PersonFields.ZIPCODE] = self.__PATIENTS.zipcode()[i].strip()

            for field in PATIENT_FIELDS:
                if not person[field]:
                    break
            else:
                self._patient_surrogates[i] = person

        operations_logger.info(f'Kept {len(self._patient_surrogates)} patient surrogates with required information.')

    def __process_patient_notes(self):
        """Process patient notes, surrogating PHI, adjusting dates, and writing new outputs."""
        note_file = os.path.join(os.path.dirname(__file__), 'NOTEEVENTS.csv')

        note_count = 0
        # type -> patient -> admission -> note
        notes_by_type = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        with open(note_file, 'r') as note_fh:
            for note in csv.reader(note_fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL):
                subject_id = int(note[0])
                if subject_id not in self._patients:
                    continue

                # HADM_ID will be NULL ('N') if patient was either outpatient, or inpatient but did not visit ICU
                hadm_id = note[1]
                if hadm_id != 'N':
                    hadm_id = int(note[1])

                note_id = note[2]
                category = note[3]

                notes_by_type[category][subject_id][hadm_id].append((note_id, note[4]))

                note_count += 1
                if not note_count % 5000:
                    operations_logger.info(f'Read {note_count} note events...')

        operations_logger.info(f'Read {note_count} total note events.')

        self.__surrogate_notes(notes_by_type)

    def _get_patient(self, subject_id, patient_cache, person_cache):
        if subject_id not in patient_cache:
            gender = self._patients[subject_id].gender
            if len(person_cache[gender]):
                patient_cache[subject_id] = person_cache[gender].pop()
            else:
                while True:
                    pat_keys = list(self._patient_surrogates)
                    pat_key = random.choice(pat_keys)
                    person = self._patient_surrogates[pat_key]
                    surrogate_gender = self._names_by_gender.get(person[PersonFields.FIRST_NAME].upper(),
                                                                 self._names_by_gender.get(
                                                                     person[PersonFields.MIDDLE_NAME].upper()))

                    if gender != surrogate_gender:
                        if surrogate_gender:
                            person_cache[surrogate_gender].append(person)
                        del self._patient_surrogates[pat_key]
                    else:
                        patient_cache[subject_id] = person
                        del self._patient_surrogates[pat_key]
                        break

        return patient_cache[subject_id]

    def __surrogate_notes(self, notes_by_type):
        person_cache = defaultdict(list)
        note_count = 0
        patient_cache = dict()
        for category, patients in notes_by_type.items():
            for subject_id, admissions in patients.items():
                self.__last_doc = None
                self.__last_doc_name_field = None

                patient = self._get_patient(subject_id, patient_cache, person_cache)

                substitutions = dict()
                for hadm_id, notes in admissions.items():
                    for note in notes:
                        demo_annotations = []
                        phi_annotations = []

                        note_text = self.__surrogate_note(note[1], substitutions,
                                                          subject_id, patient, demo_annotations, phi_annotations)
                        self.__annotate_gender(note_text, gender, demo_annotations)
                        self.__write_note(category, subject_id, hadm_id, note[0], note_text,
                                          demo_annotations, phi_annotations)

                        note_count += 1
                        if not note_count % 5000:
                            operations_logger.info(f'Processed {note_count} notes...')

    def __annotate_gender(self, note_text: str, gender: str, annotations: List):
        """Add annotations for patient gender if found.
        @param note_text: The note to annotate.
        @param gender: The patient gender.
        @param reader: The BRAT reader to add the annotation to.
        """
        gender_re = ' (male|man) ' if gender == 'M' else ' (female|woman) '
        for match in re.finditer(gender_re, note_text, re.IGNORECASE):
            self.__add_annotation('sex', (match.start(), match.end()), match[0], annotations, self._demo_type_counts)

        for match in re.finditer(f'Sex:\s+[{gender}]', note_text, re.IGNORECASE):
            self.__add_annotation('sex', (match.end() - 1, match.end()), match[0][-1], annotations, self._demo_type_counts)

    def __surrogate_note(self, note: str, substitutions: dict, patient_id: int, patient, demo_reader,
                         phi_reader) -> str:
        """Inject surrogate data into a note.
        @param note: The note to process.
        @param substitutions: The aggregate mapping of PHI indicator to previously used substitution string.
        @param patient_id: The patient id.
        @return: The surrogated note.
        """
        while True:
            phi_match = self._PHI_PATTERN.search(note)
            if not phi_match:
                break

            phi_text = phi_match[0]
            if phi_match not in substitutions:
                substitutions[phi_text] = self._get_phi_sub(phi_match, patient_id, patient)

            substitution, demo_type, phi_type = substitutions[phi_text]
            sub_text = ' '.join(substitution)
            note = note.replace(phi_text, sub_text, 1)

            if demo_type:
                self.__process_annotation(demo_type, phi_match.start(), sub_text, substitution,
                                          demo_reader, self._demo_type_counts)

            if phi_type:
                self.__process_annotation(phi_type, phi_match.start(), sub_text, substitution,
                                          phi_reader, self._phi_type_counts)

        return note

    def __process_annotation(self, annot_type, phi_start, sub_text, substitution, reader, counts):
        if len(annot_type) == 1:
            self.__add_annotation(annot_type[0], (phi_start, phi_start + len(sub_text)), sub_text, reader, counts)
        else:
            for i in range(len(annot_type)):
                token_end = phi_start + len(substitution[i])
                self.__add_annotation(annot_type[i], (phi_start, token_end),
                                      substitution[i], reader, counts)
                phi_start = token_end + 1

    @staticmethod
    def __add_annotation(aspect: str, span: tuple, text: str, annotations: List, counts: Dict[str, int]):
        annotation = Annotation()
        annotation.label = aspect
        annotation.text_range = span
        annotation.text = text

        annotations.append(annotation)

        counts[aspect] += 1

    def _get_phi_sub(self, match, subject_id: int, patient):
        """Get the substitution for a PHI text blob.
        @param phi_text: The PHI match.
        @param subject_id: The patient id.
        @return: The text to substitute, demographics type, and PHI type.
        """
        phi_text = match[0].replace('[**', '').replace('**]', '')

        if phi_text.startswith('Country'):
            return (random.choice(self._COUNTRIES),), (), ('COUNTRY',)

        if phi_text.startswith('Age over 90'):
            return (random.choice(self._OLD_AGES),), ('pat_age',), ('AGE',)

        if phi_text.startswith('University'):
            return (random.choice(self._UNIVERSITIES),), (), ()

        if phi_text.startswith('PO') or (phi_text.strip().isnumeric() and len(phi_text) < 4):
            demo_type, phi_type = ('pat_street', 'STREET') if phi_text.startswith('PO') else ('pat_age', 'AGE')

            return (phi_text,), (demo_type,), (phi_type,)

        if phi_text.startswith('URL'):
            return (f'https://www.{random.choice(self._DOMAINS)}',), (), ('URL',)

        if phi_text.startswith('Holiday'):
            return (random.choice(self._HOLIDAYS),), ('date',), ('DATE',)

        if phi_text.startswith('Wardname') or phi_text.startswith('Hospital Ward Name'):
            return (random.choice(self._WARDS),), ('facility_name',), ('HOSPITAL',)

        if phi_text.startswith('Location') or phi_text.startswith('Numeric Identifier'):
            demo_type = ()
            phi_type = ()
            if phi_text.startswith('Numeric Identifier'):
                demo_type = ('dr_id',)
                phi_type = ('IDNUM',)

            return (f'Room {random.choice(range(1, 501))}',), demo_type, phi_type

        if phi_text.startswith('Company'):
            return (random.choice(self._COMPANIES),), random.choice([(), ('dr_org',)]), ('ORGANIZATION',)

        if phi_text.startswith('Known lastname'):
            return (patient[PersonFields.LAST_NAME],), ('pat_last',), ('PATIENT',)

        if phi_text.startswith('Known firstname'):
            return (patient[PersonFields.FIRST_NAME],), ('pat_first',), ('PATIENT',)

        if phi_text.startswith('State'):
            return (random.choice(self._STATES),), ('pat_state',), ('STATE',)

        if phi_text.startswith('Hospital Unit Name'):
            return (random.choice(self._CCUs),), (), ()

        if phi_text.startswith('Hospital'):
            if subject_id not in self._hospitals:
                self._hospitals[subject_id] = get_random_hospital(self.__HOSPITALS)

            return (self.__get_hospital_name_or_abbr(
                self._hospitals[subject_id][HospitalFields.NAME].title()),), ('facility_name',), ('HOSPITAL',)

        if phi_text.startswith('Pager'):
            return (''.join(str(i) for i in self.__get_random_digits(5)),), ('dr_phone',), ('PHONE',)

        if phi_text.startswith('Telephone'):
            area = str(random.choice(range(2, 10))) + ''.join(str(i) for i in self.__get_random_digits(2))
            prefix = ''.join(str(i) for i in self.__get_random_digits(3))
            line = ''.join(str(i) for i in self.__get_random_digits(4))

            demo_type = random.choice(['pat_phone', 'dr_phone', 'dr_fax'])
            return (f'{area}-{prefix}-{line}',), (demo_type,), ('FAX' if demo_type == 'dr_fax' else 'PHONE',)

        if phi_text.startswith('Dictator') or phi_text.startswith('CC Contact') or phi_text.startswith('Attending'):
            if phi_text not in self._doctor_cache:
                self._doctor_cache[phi_text].append(get_random_person(self.__DOCTORS, DOCTOR_REQ_FIELDS))

            person = self._doctor_cache[phi_text][0]

            return (person[PersonFields.FIRST_NAME], person[PersonFields.LAST_NAME]), \
                   ('dr_first', 'dr_last'), ('DOCTOR',)

        if phi_text.startswith('E-mail'):
            domain = random.choice(self._DOMAINS)

            if flipcoin():
                first_name = patient[PersonFields.FIRST_NAME]
                middle_init = patient[PersonFields.MIDDLE_NAME][0]
                last_name = patient[PersonFields.LAST_NAME]

                if flipcoin():
                    if flipcoin():
                        return (f'{first_name[0]}{last_name}@{domain}',), ('pat_email',), ('EMAIL',)

                    return (f'{first_name[0]}{middle_init}{last_name}@{domain}',), ('pat_email',), ('EMAIL',)
                return (f'{first_name}.{last_name}@{domain}',), ('pat_email',), ('EMAIL',)

            doctor = self.__get_doctor(subject_id)
            return (f'{doctor[PersonFields.FIRST_NAME]}.{doctor[PersonFields.LAST_NAME]}@{domain}',), \
                   ('dr_email',), ('EMAIL',)

        if phi_text.startswith('Doctor'):
            if 'First' in phi_text:
                return (self.__get_dr_name(PersonFields.FIRST_NAME, subject_id),), ('dr_first',), ('DOCTOR',)

            return (self.__get_dr_name(PersonFields.LAST_NAME, subject_id),), ('dr_last',), ('DOCTOR',)

        if phi_text.startswith('Last Name'):
            return (self.__get_dr_name(PersonFields.LAST_NAME, subject_id),), ('dr_last',), ('DOCTOR',)

        if 'First Name' in phi_text:
            return (self.__get_dr_name(PersonFields.FIRST_NAME, subject_id),), ('dr_first',), ('DOCTOR',)

        if phi_text.startswith('Initial'):
            person = self.__get_doctor(subject_id)

            if phi_text.startswith('Initial '):
                return (f'{person[PersonFields.FIRST_NAME][0]}.',), ('dr_first',), ('DOCTOR',)

            return (f'{person[PersonFields.FIRST_NAME][0]}.{person[PersonFields.MIDDLE_NAME][0]}.',), \
                   ('dr_initials',), ('DOCTOR',)

        if phi_text.startswith('Name'):
            person = self.__get_doctor(subject_id)

            if phi_text.startswith('Name Initial') or phi_text.startswith('Name (NI)'):
                return (f'{person[PersonFields.FIRST_NAME][0]}.', person[PersonFields.LAST_NAME]), \
                       ('dr_first', 'dr_last'), ('DOCTOR',)

            return (person[PersonFields.FIRST_NAME], person[PersonFields.LAST_NAME]), \
                   ('dr_first', 'dr_last'), ('DOCTOR',)

        if 'Address' in phi_text:
            if phi_text.startswith('Street Address'):
                if subject_id not in self._hospitals:
                    self._hospitals[subject_id] = get_random_hospital(self.__HOSPITALS)

                hospital = self._hospitals[subject_id]

                return (hospital[HospitalFields.STREET], hospital[HospitalFields.CITY], hospital[HospitalFields.STATE],
                        hospital[HospitalFields.ZIPCODE]), \
                       ('dr_street', 'dr_city', 'dr_state', 'dr_zip'), ('STREET', 'CITY', 'STATE', 'ZIP')

            return (patient[PersonFields.STREET], patient[PersonFields.CITY], patient[PersonFields.STATE],
                    patient[PersonFields.ZIPCODE]), \
                   ('pat_street', 'pat_city', 'pat_state', 'pat_zip'), ('STREET', 'CITY', 'STATE', 'ZIP')

        if 'Number' in phi_text:
            if phi_text.startswith('Social Security Number'):
                ssn1 = ''.join(str(i) for i in self.__get_random_digits(3))
                ssn2 = ''.join(str(i) for i in self.__get_random_digits(2))
                ssn3 = ''.join(str(i) for i in self.__get_random_digits(4))
                return ('-'.join([ssn1, ssn2, ssn3]),), ('SSN',), ('IDNUM',)

            demo_type = ()
            phi_type = ()
            if phi_text.startswith('MD Number'):
                demo_type = ('dr_id',)
                phi_type = ('IDNUM',)
            elif phi_text.startswith('Medical Record Number'):
                demo_type = ('MRN',)
                phi_type = ('MEDICALRECORD',)
            elif phi_text.startswith('Clip Number'):
                phi_type = ('BIOID',)
            elif phi_text.startswith('Serial Number'):
                phi_type = ('DEVICE',)
            elif phi_text.startswith('Provider Number'):
                demo_type = ('insurance',)
                phi_type = ('HEALTHPLAN',)

            return (''.join(str(i) for i in self.__get_random_digits(10)),), demo_type, phi_type

        date_sub, is_dob = self.__get_date_sub(phi_text, subject_id)
        if date_sub:
            return (date_sub,), ('DOB' if is_dob else 'date',), ('DATE',)

        return (phi_text,), (), ()

    def __get_doctor(self, subject_id: int) -> Dict[PersonFields, str]:
        """Get a doctor for a patient record.
        @param subject_id: The patient id.
        """
        N_DOCS = 5
        if subject_id not in self._doctor_cache:
            self._doctor_cache[subject_id].append(get_random_person(self.__DOCTORS, DOCTOR_REQ_FIELDS))
        elif len(self._doctor_cache[subject_id]) != N_DOCS:
            for _ in range(N_DOCS - 1):
                self._doctor_cache[subject_id].append(get_random_person(self.__DOCTORS, DOCTOR_REQ_FIELDS))

        return random.choice(self._doctor_cache[subject_id])

    def __get_dr_name(self, name_field: PersonFields, subject_id: int) -> str:
        """Get a formatted doctor name.
        @param name_field: The name part to retrieve.
        @param subject_id: The patient id.
        @return: The doctor name.
        """
        if not self.__last_doc or not self.__last_doc_name_field or self.__last_doc_name_field == name_field:
            self.__last_doc = self.__get_doctor(subject_id)

        if self.__last_doc_name_field:
            self.__last_doc_name_field = None
        else:
            self.__last_doc_name_field = name_field

        return self.__last_doc[name_field]

    def __get_random_digits(self, N: int) -> List[int]:
        """Get N random integers between 0 and 9 (inclusive).
        @param N: The number of integers to generate.
        @return: List of N integers.
        """
        return [random.choice(range(10)) for _ in range(N)]

    def __get_hospital_name_or_abbr(self, hospital_name: str) -> str:
        """Get the hospital name either in full or abbreviated.
        @param hospital_name: The original hospital name.
        @return: The formatted name.
        """
        return abbreviate(hospital_name.split()) if flipcoin() else hospital_name

    def __get_date_sub(self, phi_text: str, subject_id: int) -> str:
        """Try to process a PHI field as a date.
        @param phi_text: The PHI field to process.
        @param subject_id: The patient id.
        @return: The text to substitute, if the PHI is a date.
        """
        DATE_FORMATS = ['%Y-%m-%d', '%m/%Y', '%Y', '%B %Y', ', %Y']
        YEARS = [str(y) for y in range(2000, 2013)]
        MONTHS = [f'0{m}'[-2:] for m in range(1, 13)]
        MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                       'October', 'November', 'December']
        DAYS = [f'0{m}'[-2:] for m in range(1, 28)]

        if phi_text.lower().startswith('date range'):
            r_year = random.choice(YEARS)
            rindex = random.choice(range(1, len(MONTHS)))

            return f'{MONTHS[random.choice(range(rindex))]}/{r_year} - {MONTHS[rindex]}/{r_year}', False

        if phi_text.startswith('Year'):
            if phi_text.startswith('Year (4 digits)'):
                return random.choice(YEARS), False

            if phi_text.startswith('Year/Month/Day'):
                return f'{random.choice(YEARS)}/{random.choice(MONTHS)}/{random.choice(DAYS)}', False

            if phi_text.startswith('Year (2 digits)'):
                return random.choice(YEARS[-2:]), False

            if phi_text.startswith('Year/Month'):
                return f'{random.choice(YEARS)}/{random.choice(MONTHS)}', False

        if phi_text == 'Day Month':
            return f'{random.choice(DAYS)} {random.choice(MONTH_NAMES)}', False

        if phi_text.startswith('Month'):
            if phi_text.startswith('Month (only) '):
                return f'{random.choice(MONTH_NAMES)}', False

            if phi_text.startswith('Month/Day/Year '):
                return f'{random.choice(MONTHS)}/{random.choice(DAYS)}/{random.choice(YEARS)}', False

            if phi_text.startswith('Month/Day '):
                return f'{random.choice(MONTHS)}/{random.choice(DAYS)}', False

            if phi_text.startswith('Month/Year '):
                return f'{random.choice(MONTHS)}/{random.choice(YEARS)}', False

            if phi_text.startswith('Month Day '):
                return f'{random.choice(MONTH_NAMES)} {random.choice(DAYS)}', False

            if phi_text.startswith('Month Year '):
                return f'{random.choice(MONTH_NAMES)} {random.choice(YEARS)}', False

        if self.__SHORT_DATE_PATTERN.match(phi_text):
            return phi_text, False

        for df in DATE_FORMATS:
            try:
                phi_date = datetime.datetime.strptime(phi_text, df)

                if phi_date.month == 2 and phi_date.day == 29:
                    phi_date = phi_date.replace(day=28)

                return phi_date.replace(year=phi_date.year - self._year_offsets[subject_id]).strftime(df), \
                       phi_date == self._patients[subject_id].dob
            except:
                pass

        return None, None

    def __write_note(self, category, pid, hadm_id, note_id, note_text, demo_reader, phi_reader):
        """Write the admission note(s) to file."""
        out_root = os.path.join(self.__ROOT_OUT_DIR, category)
        dir_id = f'{pid}{hadm_id}'.zfill(3)
        hash_dir = os.sep.join([out_root, dir_id[:2], dir_id[2]])

        text_root_dir = os.path.join(hash_dir, 'txt')
        demo_root_dir = os.path.join(hash_dir, 'demographics')
        phi_root_dir = os.path.join(hash_dir, 'phi')
        for d in [text_root_dir, demo_root_dir, phi_root_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

        file_root = f'{pid}_{hadm_id}_{note_id}'
        common.write_text(note_text, os.path.join(text_root_dir, f'{file_root}.txt'))

        self.__validate_annotations(note_text, demo_reader.annotations)
        common.write_text(demo_reader.to_brat(), os.path.join(demo_root_dir, f"{file_root}.ann"))

        self.__validate_annotations(note_text, phi_reader.annotations)
        common.write_text(phi_reader.to_brat(), os.path.join(phi_root_dir, f"{file_root}.ann"))

    def __validate_annotations(self, text: str, annotations: List[Annotation]):
        """Make sure things line up properly."""
        for annotation in annotations.values():
            span = annotation.spans[0]

            if text[span[0]:span[1]] != annotation.text:
                raise Exception(f'\n{span[0]}:{span[1]}\nExpected: {annotation.text}\nActual: {text[span[0]:span[1]]}')

    def _get_year_adj(self):
        """Compute the year adjustments to get records back to original date range."""
        for pid, patient in self._patients.items():
            min_year = patient.admissions[0][1].year
            max_year = patient.admissions[-1][2].year

            # 1/6/2001 and 10/10/2012 for adults
            self._year_offsets[pid] = random.choice(range(max_year - 2012, min_year - 2000))

    def _filter_neonates(self):
        """Remove patient info for neonates."""
        filter_ids = set()
        for pid, patient in self._patients.items():
            if patient.age_at_first_admin == 0:
                filter_ids.add(pid)

        for pid in filter_ids:
            del self._patients[pid]

        operations_logger.info(f'Filtered {len(filter_ids)} patients.')

    def _read_patient_dates(self):
        """Read the patient date file."""
        # file needs to be synched down from s3://biomed-raw-data/resources/mimic
        with open('PATIENT_DATES.csv', 'r') as date_fh:
            for cols in csv.reader(date_fh):
                subject_id = int(cols[0])
                hadm_id = int(cols[1])
                admit_time = datetime.datetime.strptime(cols[2], self.__DATE_TIME_FORMAT)
                discharge_time = datetime.datetime.strptime(cols[3], self.__DATE_TIME_FORMAT)

                if subject_id not in self._patients:
                    patient = _Patient()
                    patient.dob = datetime.datetime.strptime(cols[4], self.__DATE_TIME_FORMAT)
                    patient.gender = cols[5]
                    self._patients[subject_id] = patient

                patient = self._patients[subject_id]
                patient.admissions.append((hadm_id, admit_time, discharge_time))
                self._patients[subject_id] = patient

        for patient in self._patients.values():
            patient.admissions.sort(key=lambda x: x[1])
            patient.age_at_first_admin = self.__get_age(patient.dob, patient.admissions[0][1])
            patient.age_at_last_discharge = self.__get_age(patient.dob, patient.admissions[-1][2])

        operations_logger.info(f"Read data for {len(self._patients)} patients.")

    def __get_age(self, dob: datetime.datetime, event_date: datetime.datetime) -> int:
        """Get a person's age at the time of an event.
        @param dob: The person's date of birth.
        @param event_date: The event date.
        @return: The person's age.
        """
        return event_date.year - dob.year - ((event_date.month, event_date.day) < (dob.month, dob.day))


if __name__ == '__main__':
    unittest.main()
