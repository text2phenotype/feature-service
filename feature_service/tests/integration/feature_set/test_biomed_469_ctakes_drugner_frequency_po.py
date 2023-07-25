import unittest
from feature_service.nlp.nlp_reader import DrugReader


class TestBiomed469(unittest.TestCase):

    def assertDrugNER(self, text, expected='Colace'):
        actual = DrugReader(text).uniq_result_text()

        self.assertIn(expected, actual)
        self.assertEqual(1, len(actual))

    def test_drugner_colace_po_take_drug_orally(self):
        self.assertDrugNER('Colace 100 mg', 'Colace')
        self.assertDrugNER('Colace 100 mg p.o.', 'Colace')
        self.assertDrugNER('Colace 100 mg p.o. use as prescribed', 'Colace')
        self.assertDrugNER('Colace 100 mg p.o. three times a day', 'Colace')

    def test_drugner_with_frequency(self):
        self.assertDrugNER('Colace 100 mg p.o. b.i.d.', 'Colace')  # twice a day
        self.assertDrugNER('Colace 100 mg p.o. t.i.d.', 'Colace')  # three times a day
