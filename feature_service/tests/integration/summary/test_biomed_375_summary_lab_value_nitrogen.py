from enum import Enum
import unittest

from feature_service.nlp.nlp_reader import LabReader, DrugReader
from feature_service.nlp.nlp_reader import HepcReader, HepcLabReader, HepcDrugReader

#########################
# Blood Urea Nitrogen CUI
#########################
BUN_CUI = 'C0005845'


#########################
# BUN Examples Normal
#########################
class EXAMPLES(Enum):
    urea_normal_value = "Blood Urea 10 mg/dl"
    urea_normal_range = 'Blood Urea normal range 7 to 20 mg/dL (2.5 to 7.1 mmol/L)'
    nitrogen_normal = 'Blood Urea nitrogen was normal'
    nitrogen_normal_range = 'Blood Urea nitrogen 5-23 mg/dl'
    nitrogen_list = ['Nitrogen',
                     'Nitrogen [Chemical/Ingredient]',
                     'N element',
                     'N2 element',
                     'N - Nitrogen',
                     'N2 - Nitrogen',
                     'Nitrogen (substance)',
                     'Nitrogen, NOS']


#########################
# BUN Challenging text
#########################
class CHALLENGE(Enum):
    urea_normal_value = "Urea 10 mg/dl"  # TODO: add concept "Urea" as shorthand for "Blood Urea"
    urea_normal_range = 'Urea normal range 7 to 20 mg/dL (2.5 to 7.1 mmol/L)'
    nitrogen_normal = 'Urea nitrogen was normal'
    # nitrogen_normal_range = 'Urea nitrogen 5-23 mg/dl'


class TestBiomed375(unittest.TestCase):

    def test_BUN_normal(self):
        """
        https://www.mayoclinic.org/tests-procedures/blood-urea-nitrogen/about/pac-20384821
        """
        for example in EXAMPLES:

            if '_list' in example.name:
                continue
            else:
                text = example.value

                self.assertEqual(1, HepcLabReader(text).count_labs())
                self.assertEqual(0, HepcDrugReader(text).count_results())

                self.assertIn(BUN_CUI, HepcReader(text).uniq_concept_cuis())

    def test_nitrogen_standalone(self):
        """
        BIOMED-1402: note that LabReader and HepcLabReader both use HEPC LabValue pipeline (01/29/2020)
        """
        for nitrogen in EXAMPLES.nitrogen_list.value:
            self.assertEqual(0, LabReader(nitrogen).count_labs())
            self.assertEqual(0, HepcLabReader(nitrogen).count_labs())

    @unittest.skip('BIOMED-375')
    def test_BUN_challenge(self):
        text = CHALLENGE.urea_normal_value.value
        value = {'10'}
        units = {'mg/dl'}

        self.assertEqual('Urea', HepcLabReader(text).uniq_result_text())
        self.assertEqual(value, HepcLabReader(text).list_lab_values())
        self.assertEqual(units, HepcLabReader(text).list_lab_units())

    @unittest.skip('BIOMED-375')
    def test_BUN_false_positives_drugner(self):

        text = EXAMPLES.urea_normal_value.value
        cui_urea_drug = 'C0041942'

        self.assertEqual(0, DrugReader(text).count_results())

    @unittest.skip('BIOMED-486')
    def test_BUN_false_positives_hepc_drugner_mg_milligrams(self):

        text = EXAMPLES.urea_normal_value.value
        cui_mg_disease = 'C0026896'

        self.assertEqual(0, HepcReader(text).count_results())
