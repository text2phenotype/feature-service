import os
import random
import unittest

from feature_service.tests.experiment.i2b2 import i2b2_2006
from feature_service.tests.experiment.i2b2.surrogates import Surrogates

from text2phenotype.apiclients.feature_service import FeatureServiceClient
from text2phenotype.common import common
from text2phenotype.common.log import operations_logger


@unittest.skip('JIRA/BIOMED-216')
class TestI2b2Surrogates2006(unittest.TestCase):

    def test_biomed_216(self):
        """
        prepare i2b2 2006 training corpus files
        """
        self.rewrite_surrogates(i2b2_2006.TRAIN_DIR, i2b2_2006.TRAIN_XML)
        self.rewrite_surrogates(i2b2_2006.TEST_DIR, i2b2_2006.TEST_XML)

    ###############################################################################
    #
    # Rewrite Surrogates for i2b2 2006
    #
    ###############################################################################
    def rewrite_surrogates(self, xml_dir, xml_file, do_surrogates=True):
        """
        Rewrite i2b2 files, writes output files into 'surrogates' subdirectory

        * record_id.txt  text with replacement text from surrogates
        * record_id.json PHI  with replacement PHI  from surrogates

        :param xml_dir:  TRAIN_DIR or TEST_DIR
        :param xml_file: TRAIN_XML or TEST_XML
        :param do_surrogates: true/false use surrogate files to replace PHI with new data
        """
        operations_logger.info(f'{xml_dir}')
        operations_logger.info(f'{xml_file}')

        surrogates = Surrogates()
        surrogates_ver_dir = os.path.join(xml_dir, common.version_text('surrogates'))

        changes = list()
        progress = list()

        feature_service_client = FeatureServiceClient()

        for record in i2b2_2006.get_records(xml_file):
            id = record.attrib['ID']
            text = list()
            phi = list()

            operations_logger.info(f"ID: {id}, #complete:{len(progress)}")
            progress.append(id)

            for content in record.getchildren():
                for utterance in content.getchildren():

                    if utterance.tag != 'PHI':
                        text.append(utterance.text)
                    else:
                        phi_2006 = utterance.attrib['TYPE']
                        phi_2014 = phi_2006
                        phi_i2b2 = utterance.text
                        phi_real = phi_i2b2

                        # original i2b2 DATES and PHONES and AGE
                        if phi_2006 in ['DATE', 'PHONE', 'AGE']:
                            pass

                        # replace class ID with MEDICALRECORD
                        elif phi_2006 in ['ID']:
                            phi_2014 = 'MEDICALRECORD'

                        # replace i2b2 PATIENT and DOCTOR with real names from USPTO
                        elif phi_2006 in ['PATIENT', 'DOCTOR']:
                            if do_surrogates:
                                phi_real = self.phi_person_text(phi_i2b2, surrogates)

                        # replace i2b2 HOSPITAL with real hospital names from CMS
                        elif phi_2006 in ['HOSPITAL']:
                            if do_surrogates:
                                phi_real = self.phi_hospital_name(phi_i2b2, surrogates)

                        # replace i2b2 LOCATIONS with real person addresses from USPTO
                        elif phi_2006 in ['LOCATION']:
                            if do_surrogates:
                                # phi_real = self.phi_location(phi_i2b2, surrogates)
                                phi_real = self.phi_address_person(phi_i2b2, surrogates)
                                phi_2014 = 'STREET'
                        else:
                            raise Exception(f"Unknown PHI type {phi_2006}\t{phi_i2b2}")

                        cursor = len(''.join(text))
                        charpos = [cursor, cursor + len(phi_real)]
                        phi.append({phi_2014: phi_real, 'range': charpos})
                        changes.append({phi_2006: phi_2014, phi_i2b2: phi_real, 'range': charpos})
                        text.append(phi_real)

            note = ''.join(text)
            tokens = feature_service_client.annotate(note)

            if not os.path.exists(surrogates_ver_dir):
                os.mkdir(surrogates_ver_dir)

            common.write_text(note, os.path.join(surrogates_ver_dir, f"{id}.txt"))
            common.write_json(phi, os.path.join(surrogates_ver_dir, f"{id}.json"))
            common.write_json(tokens, os.path.join(surrogates_ver_dir, f"{id}.featureset.annotate_text.json"))

        # Done with all files
        if do_surrogates:
            common.write_json(changes, os.path.join(surrogates_ver_dir, f"{common.version_text('surrogates')}.json"))

    ###############################################################################
    #
    # Helper methods for surrogate generation from i2b2 data
    #
    ###############################################################################

    def flipcoin(self) -> bool:
        """
        :return: bool random 50/50 True/False
        """
        return random.choice([True, False])

    def phi_person_tokens(self, text, surrogates=Surrogates()):
        """
        :return:
        """
        first_name = surrogates.first_name().pop()
        last_name = surrogates.last_name().pop()
        middle_name = surrogates.middle_name().pop()

        return [first_name, middle_name, last_name]

    def phi_person_text(self, text, surrogates=Surrogates()):
        """
        :param surrogates:
        :return:
        """
        [first_name, middle_name, last_name] = self.phi_person_tokens(surrogates)

        num_name_tokens = len(text.split())

        if ',' in text:  # McMurry, Andrew
            if num_name_tokens:
                return f"{last_name}, {first_name} {middle_name}"  # McMurry, Andrew John
            else:
                return f"{last_name}, {first_name}"  # McMurry, Andrew
        if num_name_tokens >= 3:
            return f"{first_name} {middle_name} {last_name}"  # Andrew John McMurry
        if num_name_tokens == 2:
            return f"{first_name} {last_name}"  # Andrew McMurry
        elif num_name_tokens == 1:
            return last_name if self.flipcoin() else first_name  # Andrew or McMurry

        return last_name

    def num_tokens(self, text: str) -> int:
        return len(text.split())

    def abbreviate(self, text):
        """
        :param text:
        :return:
        """
        return ''.join([token[0].upper() for token in text.split()])

    def phi_hospital_name(self, text, surrogates=Surrogates()):
        """
        :param text: the original i2b2 hospital name
        :param surrogates:
        :return: str
        """
        num_name_tokens = len(text.split())
        hospital_name = surrogates.hospital_name().pop()

        if num_name_tokens == 1:
            return self.abbreviate(hospital_name)
        else:
            return hospital_name.title()

    def phi_location(self, text, surrogates=Surrogates()):
        """
        :param text:
        :param surrogates:
        :return:
        """

        address = surrogates.address_person().pop()
        city = surrogates.city_person().pop()
        zipcode = surrogates.zipcode_person().pop()
        state = surrogates.state_person().pop
        num_commas = text.count(',')

        if num_commas >= 2:
            if self.flipcoin():
                return f"{address}, {city}, {state} {zipcode}"  # 1315 Minna street, San Francisco CA 94118
            else:
                return f"{address},{city},{zipcode}"

        if num_commas == 1:  # %21 of person_address contain commas
            if self.flipcoin():
                return f"{address}, {city}"
            else:
                return f"{address}"

        if self.num_tokens(text) == 1:
            if zipcode.match_zip(text):  # 94118
                return surrogates.zipcode_person().pop()

        return f"{address}"

    def phi_address_person(self, text: str, surrogates=Surrogates()):
        """
        :param text: replacement hint
        :param surrogates:
        :return:
        """
        return surrogates.address_person().pop()

    def get_phi_class_frequency(self, phi):
        """
        :param phi: list of dict
        :return:
        """
        phi_class = set([list(entry.keys())[0] for entry in phi])

        freq = {}
        for c in phi_class: freq[c] = list()

        for entry in phi:
            for k, v in entry.items():
                freq[k].append(v)

        for k, v in freq.items():
            operations_logger.info(f'{k} = {len(v)}')

        return freq

    def test_surrogates(self):
        real = Surrogates()

        operations_logger.info('EXAMPLES')
        operations_logger.info('PATIENT or DOCTOR')
        operations_logger.info(f'first_name {real.first_name().pop()}')
        operations_logger.info(f'last_name  {real.last_name().pop()}')
        operations_logger.info(f'middle_name {real.middle_name().pop()}')
        operations_logger.info(f'address_person  {real.address_person().pop()}')
        operations_logger.info(f'city_person  {real.city_person().pop()}')
        operations_logger.info(f'state_person  {real.state_person().pop()}')
        operations_logger.info(f'zipcode_person  {real.zipcode_person().pop()}')
        operations_logger.info('HOSPITAL')
        operations_logger.info(f'hospital_name {real.hospital_name().pop()}')
        operations_logger.info(f'address_hospital {real.address_hospital().pop()}')
        operations_logger.info(f'city_hospital {real.city_hospital().pop()}')
        operations_logger.info(f'county_hospital {real.county_hospital().pop()}')
        operations_logger.info(f'state_hospital {real.state_hospital().pop()}')
        operations_logger.info(f'zipcode_hospital {real.zipcode_hospital().pop()}')
        operations_logger.info('PHONE')
        operations_logger.info(f'phone_numeric {real.phone_numeric().pop()}')
        operations_logger.info('DATE')
        operations_logger.info(f'date_start {real.date_start().pop()}')
