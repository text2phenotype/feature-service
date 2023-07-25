import unittest
import os

from text2phenotype.common import common
from text2phenotype.entity.attributes import Polarity

from feature_service.hep_c.form import autofill_hepc_form
from feature_service.feature_service_env import FeatureServiceEnv


class TestBiomed162(unittest.TestCase):
    RICARDO_HPI_TXT = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'himss', '1-vista-pcp-note', '1-vista-pcp-note.txt')

    def assertNotAlcoholic(self, text):
        form = autofill_hepc_form(text)

        social = form.get('SUBSTANCE_USE_HISTORY', None)

        if social:
            for question in social:
                if question['suggest'] in ['alcohol_problem', 'alcohol_user']:
                    evidence = question.get('evidence', None)

                    if evidence:
                        med_strength_num = evidence.get('attributes').get('medStrengthNum')
                        med_frequency_number = evidence.get('attributes').get('medFrequencyNumber')

                        self.assertEqual(0, len(med_strength_num))
                        self.assertEqual(0, len(med_frequency_number))

                        alcohol_user = Polarity(evidence.get('polarity'))

                        self.assertFalse(alcohol_user.is_positive())

    def test_alcohol_intake_confused_lab_value(self):
        """
        Test that HCV Viral Load is not confused as alcohol intake
        """
        self.assertNotAlcoholic(common.read_text(self.RICARDO_HPI_TXT))

    def test_alcohol_abuse(self):
        """
        Test that Ricardo campos is not an alcohol_user (or alcohol_abuse)
        """
        self.assertNotAlcoholic(common.read_text(self.RICARDO_HPI_TXT))

    def test_alcohol_does_not_have_alochol_problem(self):
        """
        JIRA/BIOMED-113
        """
        self.assertNotAlcoholic('Does not have alcohol problem')
