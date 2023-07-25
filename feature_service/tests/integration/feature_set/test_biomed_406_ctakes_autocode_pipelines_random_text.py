import unittest
import random
import string

from feature_service.nlp import autocode


class TestBiomed406(unittest.TestCase):

    @staticmethod
    def randtext(n=None) -> str:
        """
        https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python"
        :param n: number of characters, if None, pick a number between 1 and 1,000
        :return: random character string of length N
        """
        if n is None:
            n = random.randint(1, 1000)

        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

    def test_summary_ctakes_autocode(self):
        """
        Test cTAKES support for **biomed.summary**
        """
        text = self.randtext(100)

        self.assertIsNotNone(autocode.clinical(text))
        self.assertIsNotNone(autocode.drug_ner(text))
        self.assertIsNotNone(autocode.lab_value(text))
        self.assertIsNotNone(autocode.smoking(text))
        self.assertIsNotNone(autocode.temporal(text))

    def test_hepc_ctakes_autocode(self):
        """
        Test cTAKES support for **biomed.hepc**
        """
        text = self.randtext(100)

        self.assertIsNotNone(autocode.hepc_clinical(text))
        self.assertIsNotNone(autocode.hepc_drug_ner(text))
        self.assertIsNotNone(autocode.hepc_lab_value(text))

    @unittest.skip('JIRA/BIOMED-406')
    def test_pipeline_url(self):
        """
        Test that each PipelineURL can be called -- every pipeline should respond.
        NOTE: some pipelines like ICD9/ICD10 for SHRINE and specific code extraction have changed and
        need further testing before we include into main code.
        """
        for url in autocode.PipelineURL:
            text = self.randtext(100)
            res = autocode.autocode(text, url.value)
            self.assertIsNotNone(res)
