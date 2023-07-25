import os
import unittest

from text2phenotype.common import common

from feature_service.nlp.nlp_reader import ClinicalReader, DrugReader
from feature_service.feature_service_env import FeatureServiceEnv


class TestBiomed421(unittest.TestCase):

    def setUp(self):
        self.text = common.read_text(os.path.join(FeatureServiceEnv.DATA_ROOT.value,
                                                  'himss',
                                                  '1-vista-pcp-note',
                                                  '1-vista-pcp-note.txt'))

    def assertClinicalResultCount(self, text, count):
        self.assertGreater(ClinicalReader(text).count_results(), count)

    def assertMedicationResultCount(self, text, count):
        self.assertGreater(DrugReader(text).count_results(), count)

    @staticmethod
    def get_med_tokens(res) -> list:
        return list(filter(None, [token.get('MED') for token in res]))

    def test_autocode_clinical(self):
        """
        Test NLP autocode function on its own
        """
        self.assertClinicalResultCount(self.text, 10)

    def test_drug_ner(self):
        """
        Expect at least one drug using CTAKES ( no deep learning )
        """
        # at least one drug
        self.assertMedicationResultCount(self.text, 1)
