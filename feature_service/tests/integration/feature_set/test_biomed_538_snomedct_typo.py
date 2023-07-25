import unittest

from feature_service.nlp.autocode import PipelineURL, autocode
from feature_service.nlp.nlp_reader import ClinicalReader

TEXT = "EXCESSIVE BODY WEIGHT GAIN"


class TestBiomed538(unittest.TestCase):

    def assert_SNOMEDCT_US(self, result):

        vocab_list = ClinicalReader(result).list_concept_vocab()

        self.assertGreater(len(vocab_list), 0, 'Expected at least one response with named vocabulary')

        for vocab in vocab_list:
            if 'SNOMED' in vocab:
                self.assertEqual('SNOMEDCT_US', vocab)

    def test_ctakes_pipelines(self):
        """
        snomedct, original, and general
        """
        pipelines = [
            PipelineURL.original,
            PipelineURL.general,
            PipelineURL.snomedct]

        for target in pipelines:
            self.assert_SNOMEDCT_US(autocode(TEXT, target))
