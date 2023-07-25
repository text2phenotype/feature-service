import unittest
import string
from feature_service.nlp.nlp_reader import ClinicalReader, DrugReader, LabReader
from feature_service.nlp.nlp_reader import HepcReader, HepcDrugReader, HepcLabReader

# BIOMED-476 discovered during test of BIOMED-214
TEXT_NEGATIVE_HEPATITIS = 'He has never had any treatment in the past for his chronic hepatitis C.'
TEXT_NEGATIVE_HCV = 'He has never had any treatment in the past for his HCV.'
TEXT_FALSE_POSITIVES = ['h', 'H', 'c', 'C', 'f', 'F', 'm', 'M']


class TestBiomed476(unittest.TestCase):

    def assertTrueNegative(self, text, expected=0):
        self.assertEqual(expected, HepcReader(text).count_results())
        self.assertEqual(expected, HepcLabReader(text).count_results())
        self.assertEqual(expected, HepcDrugReader(text).count_results())
        self.assertEqual(expected, ClinicalReader(text).count_results())
        self.assertEqual(expected, LabReader(text).count_labs())
        self.assertEqual(expected, DrugReader(text).count_concepts())

    def test_c_is_not_abbreviation_for_cocaine(self):
        cocaine = 'C0009170'

        for text in ['C', TEXT_NEGATIVE_HEPATITIS, TEXT_NEGATIVE_HCV]:
            reader = HepcReader(text)
            self.assertFalse(cocaine in reader.list_concept_cuis(), f'bad drug user match for HCV, text was {text}')

    def test_biomed_478_ctakes_specificity_no_single_char(self):
        for punc in string.punctuation:
            self.assertTrueNegative(punc)

        for letter in string.ascii_letters:
            if letter not in TEXT_FALSE_POSITIVES:
                self.assertTrueNegative(letter)

    @unittest.skip('JIRA/BIOMED-478')
    def test_biomed_478_regression(self):
        for single_char in TEXT_FALSE_POSITIVES:
            self.assertTrueNegative(single_char)
