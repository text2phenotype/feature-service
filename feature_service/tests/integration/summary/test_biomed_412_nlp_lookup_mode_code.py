import unittest

from feature_service.nlp import autocode
from feature_service.nlp.nlp_reader import ClinicalReader


class TestBiomed412(unittest.TestCase):

    def icd10_lookup_code(self, text) -> ClinicalReader:
        res = autocode.autocode(text, autocode.PipelineURL.icd10.value, autocode.LookupMode.CODE)
        return ClinicalReader(res)

    def test_lookup_mode_code(self):
        """
        Acute myocardial infarction I21
        https://www.icd10data.com/ICD10CM/Codes/I00-I99/I20-I25/I21-
        """
        for text in ['I21', 'I21.0', 'I21.01', 'I21.02', 'I21.09', 'I21.1', 'I21.11', 'I21.19', 'I21.A', 'I21.A1']:
            reader = self.icd10_lookup_code(text)

            self.assertGreater(reader.count_results(), 0, f'no match found for ICD10 code {text}')

    def test_false_positives(self):
        for text in ['I210', 'I21A1']:
            reader = self.icd10_lookup_code(text)

            self.assertEqual(reader.count_results(), 0, f'false positive for ICD10 code {text}')
