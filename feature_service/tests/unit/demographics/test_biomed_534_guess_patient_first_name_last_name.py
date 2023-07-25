import unittest
from enum import Enum
from typing import Optional

from feature_service.feature_set.feature_cache import FeatureCache


class NameType(Enum):
    FIRST = 0
    MID = 1
    LAST = 2


class TestPatientNames(unittest.TestCase):
    def setUp(self) -> None:
        self.feature_cache = FeatureCache()

    def test_hard_to_do(self):
        """
        https://www.momjunction.com/articles/last-names-as-first-names-boys-girls_00413500/#gref
        """
        hard = ['Adler', 'Anderson', 'Beckett', 'Brady', 'Carson', 'Carter', 'Cohen', 'Coleman', 'Cooper', 'Copeland',
                'Davis', 'Peyton', 'West']

        for last_name in hard:
            self.assertLastName(last_name)

    def assertFirstName(self, name_token):
        self.assertEqual(NameType.FIRST, self.guess_pat_name_type(name_token))

    def assertLastName(self, name_token):
        self.assertEqual(NameType.LAST, self.guess_pat_name_type(name_token))

    def assertMiddleName(self, name_token):
        self.assertEqual(NameType.MID, self.guess_pat_name_type(name_token))

    def test_european(self):
        self.assertFirstName('Andy')
        self.assertFirstName('Andrew')
        self.assertLastName('McMurry')
        self.assertLastName('Murry')
        self.assertLastName('Murray')
        self.assertMiddleName('J.')

    def test_asian(self):
        # self.assertFirstName('Richen') TODO: no name entry for richen
        self.assertLastName('Zhang')

        self.assertFirstName('Vanessa')
        self.assertLastName('Cheng')

    def test_russian(self):
        self.assertFirstName('Anton')
        self.assertLastName('Vasin')

    @staticmethod
    def guess_name_type(name_token: str, tf_first: dict, tf_last: dict) -> Optional[NameType]:
        """
        :param name_token: DEID predicted name token
        :param tf_first: first name term frequency
        :param tf_last: last name term frequency
        :return: NameType or None
        """
        if len(name_token) <= 2:
            return NameType.MID

        name_token = name_token.upper()

        first = tf_first.get(name_token, 0)
        last = tf_last.get(name_token, 0)

        # First name average length = 6
        # Last name average is slightly longer
        #
        # https://www.quora.com/What-is-the-average-length-of-first-names-in-the-United-States
        # https://www.quora.com/What-is-the-average-length-of-last-names-in-the-United-States

        if first > last:
            return NameType.FIRST

        elif last > first:
            return NameType.LAST

        elif first == last and first > 0:
            if len(name_token) >= 6:
                return NameType.LAST
            else:
                return NameType.FIRST
        else:
            return None

    def guess_pat_name_type(self, patient_name: str) -> NameType:
        """
        :param patient_name: patient name token SINGLE WORD ONLY!
        :return: NameType or None if not in TF dictionary
        """
        return self.guess_name_type(patient_name,
                                    self.feature_cache.tf_patients_first_name(),
                                    self.feature_cache.tf_patients_last_name())

    def guess_dr_name_type(self, dr_name: str) -> NameType:
        """
        :param dr_name: doctor name token SINGLE WORD ONLY !
        :return: NameType or None if not in TF dictionary
        """
        return self.guess_name_type(dr_name,
                                    self.feature_cache.tf_npi_first_name(),
                                    self.feature_cache.tf_npi_last_name())
