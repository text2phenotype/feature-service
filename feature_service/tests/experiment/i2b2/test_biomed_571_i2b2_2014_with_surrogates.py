#!/usr/bin/python
import unittest
import os
import re
from collections import defaultdict
from typing import Dict, List

from text2phenotype.annotations.file_helpers import Annotation
from text2phenotype.common import common
from text2phenotype.common.log import operations_logger

from feature_service.tests.experiment.i2b2 import i2b2_2014
from feature_service.tests.experiment.i2b2.surrogates import (PatientSurrogates, HospitalSurrogates, DoctorSurrogates,
                                                              PersonFields, HospitalFields, read_names, abbreviate,
                                                              get_random_person, get_random_hospital, num_tokens,
                                                              make_surrogate_dates, guess_patient_gender,
                                                              phi_person_text, phi_hospital_name)
from text2phenotype.entity.brat import BratReader


@unittest.skip('JIRA/BIOMED-571')
class TestI2b2Surrogates2014(unittest.TestCase):
    __HOSPITALS = HospitalSurrogates()
    __PATIENTS = PatientSurrogates()
    __DOCTORS = DoctorSurrogates()

    def test_biomed_571(self):
        """
        prepare i2b2 2014 training corpus files
        """
        names = read_names(os.path.join(os.path.dirname(__file__), '..', 'us-likelihood-of-gender-by-name-in-2014.csv'))

        SOURCE_DIR = 'gold_raw_text'
        self.rewrite_surrogates(i2b2_2014.get_training_files(
            [os.path.join(SOURCE_DIR, 'training-PHI-Gold-Set1'),
             os.path.join(SOURCE_DIR, 'training-PHI-Gold-Set2')]), names)
        self.rewrite_surrogates(
            i2b2_2014.get_testing_files([os.path.join(SOURCE_DIR, 'testing-PHI-Gold-fixed')]), names)

    ###############################################################################
    #
    # Rewrite Surrogates for i2b2 2014
    #
    ###############################################################################
    def rewrite_surrogates(self, sample_files: List[str], names: Dict[str, str]):
        """
        Rewrite i2b2 files, writes output files into 'surrogates' subdirectory

        * record_id.txt  text with replacement text from surrogates
        * record_id.json PHI  with replacement PHI  from surrogates

        :param sample_files: The I2B2 files to process.
        :param names: Mapping of name to most likely gender.
        """
        FILE_COUNT = len(sample_files)
        DOCTOR_REQ_FIELDS = frozenset([PersonFields.FIRST_NAME, PersonFields.LAST_NAME, PersonFields.MIDDLE_NAME])
        PATIENT_FIELDS = frozenset([pf for pf in PersonFields])

        ssn_pattern = re.compile(fr'\d{3}-?\d{2}-?\d{4}')
        reader = BratReader()
        changes = defaultdict(list)
        surrogates_versions = dict()
        surrogate_version_dirs = dict()
        person_cache = defaultdict(list)
        record_count = 0
        for sample_file in sample_files:
            id = os.path.splitext(os.path.basename(sample_file))[0]
            operations_logger.info(f"Processing {id}...")

            src_dir = os.path.dirname(sample_file)
            if src_dir not in surrogates_versions:
                surrogates_versions[src_dir] = common.version_text('surrogates')
            surrogates_ver = surrogates_versions[src_dir]

            surrogates_ver_dir = os.path.join(src_dir, surrogates_ver)
            if not os.path.exists(surrogates_ver_dir):
                os.mkdir(surrogates_ver_dir)
                surrogate_version_dirs[surrogates_ver] = surrogates_ver_dir

            record_text = i2b2_2014.get_text(sample_file)
            record_tags = i2b2_2014.get_tags(sample_file)

            date_map = make_surrogate_dates([tag for tag in record_tags if tag['TYPE'] == 'DATE'])

            gender = guess_patient_gender(record_text,
                                          [tag for tag in record_tags if tag['TYPE'] == 'PATIENT'], names)
            patient_info = get_random_person(self.__PATIENTS, PATIENT_FIELDS, names, gender, person_cache)

            text_start = 0
            use_hospital_addr = False
            last_hospital_end = 0
            doctors = dict()
            hospitals = dict()
            text2phenotype_type = None
            real_text_fields = list()
            real_phi = list()
            patient_fnames = dict()
            doctor_fnames = dict()
            for tag in record_tags:
                phi_start = int(tag['start'])
                phi_end = int(tag['end'])
                phi_type = tag['TYPE']
                phi_i2b2 = tag['text']

                # arbitrarily checking if PHI starts more than 10 characters from a hospital name
                if use_hospital_addr and phi_type != 'HOSPITAL' and phi_start - last_hospital_end > 25:
                    use_hospital_addr = False

                phi_sub = None
                phi_fields = None
                if phi_type == 'DOCTOR':
                    if phi_i2b2 not in doctors:
                        doctor_info = get_random_person(self.__DOCTORS, DOCTOR_REQ_FIELDS)

                        doctors[phi_i2b2] = doctor_info
                        # simple matching on doctor first/last names
                        for doc_name in re.findall(r"[\w\-]+", phi_i2b2):
                            if len(doc_name) == 1:
                                continue

                            doctors[doc_name] = doctor_info

                    if phi_i2b2 not in doctor_fnames:
                        doctor_fnames[phi_i2b2] = phi_person_text(phi_i2b2, doctors[phi_i2b2], 'dr',
                                                                  record_text[(phi_start - 10):phi_start])

                    phi_sub, phi_fields = doctor_fnames[phi_i2b2]
                elif phi_type == 'PATIENT':
                    if phi_i2b2 not in patient_fnames:
                        patient_fnames[phi_i2b2] = phi_person_text(phi_i2b2, patient_info, 'pat',
                                                                   record_text[(phi_start - 10):phi_start])

                    phi_sub, phi_fields = patient_fnames[phi_i2b2]
                elif phi_type == 'HOSPITAL':
                    hospital_key = phi_i2b2
                    # simple match hospital full name and abbreviation
                    if phi_i2b2 not in hospitals:
                        hospital_abbr = abbreviate(phi_i2b2.split())
                        if hospital_abbr not in hospitals:
                            hospital_info = get_random_hospital(self.__HOSPITALS)

                            hospitals[phi_i2b2] = hospital_info
                            if num_tokens(phi_i2b2) > 1:
                                hospitals[hospital_abbr] = hospital_info
                        else:
                            hospital_key = hospital_abbr

                    # need to set the current hospital_info to grab address info if needed
                    hospital_info = hospitals[hospital_key]
                    phi_sub = phi_hospital_name(phi_i2b2, hospital_info[HospitalFields.NAME])
                    text2phenotype_type = 'facility_name'

                    use_hospital_addr = True
                    last_hospital_end = phi_end
                elif phi_type == 'CITY':
                    if use_hospital_addr:
                        phi_sub = hospital_info[HospitalFields.CITY]
                        last_hospital_end = phi_end
                        text2phenotype_type = 'dr_city'
                    else:
                        phi_sub = patient_info[PersonFields.CITY]
                        text2phenotype_type = 'pat_city'
                elif phi_type == 'STREET':
                    if use_hospital_addr:
                        phi_sub = hospital_info[HospitalFields.STREET]
                        last_hospital_end = phi_end
                        text2phenotype_type = 'dr_street'
                    else:
                        phi_sub = patient_info[PersonFields.STREET]
                        text2phenotype_type = 'pat_street'

                    if not phi_i2b2[0].isnumeric():
                        phi_sub = ' '.join(phi_sub.split()[1:])
                elif phi_type == 'STATE':
                    if use_hospital_addr:
                        phi_sub = hospital_info[HospitalFields.STATE]
                        last_hospital_end = phi_end
                        text2phenotype_type = 'dr_state'
                    else:
                        phi_sub = patient_info[PersonFields.STATE]
                        text2phenotype_type = 'pat_state'
                elif phi_type == 'ZIP':
                    if use_hospital_addr:
                        phi_sub = hospital_info[HospitalFields.ZIPCODE]
                        last_hospital_end = phi_end
                        text2phenotype_type = 'dr_zip'
                    else:
                        phi_sub = patient_info[PersonFields.ZIPCODE]
                        text2phenotype_type = 'pat_zip'
                elif phi_type == 'DATE':
                    text2phenotype_type = phi_type

                    if phi_i2b2 in date_map:
                        phi_sub = date_map[phi_i2b2]
                    else:
                        phi_sub = phi_i2b2
                else:
                    phi_sub = phi_i2b2
                    if phi_type == 'MEDICALRECORD':
                        text2phenotype_type = 'MRN'
                    elif phi_type == 'AGE':
                        text2phenotype_type = 'pat_age'
                    elif phi_type == 'PHONE':
                        if len(phi_i2b2) == 5:  # pager #
                            text2phenotype_type = 'dr_phone'
                        else:
                            text2phenotype_type = 'pat_phone'
                    elif phi_type == 'ORGANIZATION':
                        text2phenotype_type = 'dr_org'
                    elif phi_type == 'FAX':
                        text2phenotype_type = 'dr_fax'
                    elif phi_type == 'EMAIL':
                        text2phenotype_type = 'dr_email' if phi_i2b2.lower().endswith('.org') else 'pat_email'
                    elif phi_type == 'HEALTHPLAN':
                        text2phenotype_type = 'insurance'
                    else:
                        text2phenotype_type = phi_type

                real_text_fields.append(record_text[text_start:phi_start])
                text_start = phi_end
                real_text_fields.append(phi_sub)

                real_phi_start = sum([len(t) for t in real_text_fields[:-1]])
                if phi_fields is None:
                    phi_fields = [(text2phenotype_type, phi_sub)]

                for type, value in phi_fields:
                    name_len = len(value)

                    if type != 'COMMA':
                        phi_range = (real_phi_start, real_phi_start + name_len)
                        phi_map = {'i2b2_type': phi_type, 'text2phenotype_type': type, 'i2b2_value': phi_i2b2,
                                   'text2phenotype_value': value, 'range': phi_range}
                        real_phi.append(phi_map)

                        changes_map = phi_map.copy()
                        changes_map['id'] = id
                        changes[surrogates_ver].append(changes_map)

                        real_phi_start += name_len

                    real_phi_start += 1

            real_text_fields.append(record_text[text_start:])
            modified_text = ''.join(real_text_fields)

            common.write_text(modified_text, os.path.join(surrogates_ver_dir, f"{id}.txt"))

            reader.annotations.clear()
            for phi in real_phi:
                annotation = Annotation()

                annotation.label = phi['text2phenotype_type']
                annotation.text_range = phi['range']
                annotation.text = phi['text2phenotype_value']

                span = annotation.text_range[0]
                if modified_text[span[0]:span[1]] != annotation.text:
                    print(modified_text[span[0]:span[1]], annotation.text)
                    raise Exception()

                reader.add_annotation(annotation)

            common.write_text(reader.to_brat(), os.path.join(surrogates_ver_dir, f"{id}.ann"))

            record_count += 1
            operations_logger.info(f"# complete:{record_count} of {FILE_COUNT}")

        for vers, subs in changes.items():
            common.write_json(subs, os.path.join(surrogate_version_dirs[vers], f"{vers}.json"))


if __name__ == '__main__':
    unittest.main()
