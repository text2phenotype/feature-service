import unittest

from feature_service.nlp.nlp_reader import ClinicalReader, DrugReader, LabReader, SummaryReader
from feature_service.nlp.nlp_reader import HepcReader, HepcDrugReader, HepcLabReader


class TestBiomed236(unittest.TestCase):

    def test_blacklist_generic_drug(self):

        text = 'Drugs'
        cui = 'C0013146'

        self.assertEqual(0, len(SummaryReader(text).medications))

        for reader in [ClinicalReader, LabReader, DrugReader, HepcReader, HepcDrugReader, HepcLabReader]:
            reader = reader(text)

            self.assertNotIn(cui, reader.uniq_concept_cuis())
            self.assertNotIn(text, reader.uniq_concept_text())
