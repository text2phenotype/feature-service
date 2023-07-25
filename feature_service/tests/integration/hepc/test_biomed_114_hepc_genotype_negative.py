import unittest

from feature_service.nlp.nlp_reader import HepcLabReader

from feature_service.nlp import autocode

TEXT_GENOTYPE_NEGATIVE = 'HCV Genotype 2 Negative'


class TestBiomed114(unittest.TestCase):

    def test_genotype_negative(self):
        reader = HepcLabReader(TEXT_GENOTYPE_NEGATIVE, autocode.hepc_lab_value)

        self.assertEqual(1, reader.count_labs())
        self.assertEqual(1, reader.count_results())

        self.assertEqual({'C3532920'}, reader.uniq_concept_cuis())
        self.assertEqual('negative', reader.first_lab().polarity)
