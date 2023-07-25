import unittest
from feature_service.nlp.nlp_reader import HepcLabReader

TEXT_GENOTYPE_POSITIVE = 'Chronic hepatitis C genotype 3a positive'


class TestBiomed107(unittest.TestCase):
    # BIOMED-107          # see rrf  test_chronic_hepc_geno_3a_positive
    # no match for Chronic hepatitis C genotype 3a positive
    # should find C4049436
    def test_chronic_hcv_genotype_3a(self):

        reader = HepcLabReader(TEXT_GENOTYPE_POSITIVE)

        # Expected CUI
        self.assertEqual({'C4049436'}, reader.uniq_concept_cuis())

        # Expected Synonyms
        self.assertEqual(1, len(reader.uniq_concept_text()))
        self.assertIn('CHRONIC HEPATITIS C GENOTYPE 3A', reader.uniq_concept_text())

        # Expected Value is "normal"
        self.assertEqual(1, reader.count_labs())
        self.assertEqual('positive', reader.first_lab().polarity)

    @unittest.skip('JIRA/BIOMED-107')
    def test_value_is_positive(self):
        first = HepcLabReader(TEXT_GENOTYPE_POSITIVE).first_lab()

        self.assertEqual('positive', first.value)
