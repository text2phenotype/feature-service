import unittest

from feature_service.nlp.nlp_reader import ClinicalReader


class TestNLPSummaryOpenEMR(unittest.TestCase):

    def test_biomed_280_heart_attack(self):
        res = ClinicalReader('The patient had a heart attack at 11PM on Tuesday')

        self.assertIn('C0027051', res.list_concept_cuis())
        self.assertIn('T047', res.list_concept_tuis())
        self.assertIn('SNOMEDCT_US', res.list_concept_vocab())
        self.assertIn('Myocardial Infarction', res.list_concept_text())