import unittest

from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed216(unittest.TestCase):

    def test_total_bili(self):
        lab_t_bili = HepcLabReader('T. Bili 5.63 mg/dL').first_lab()

        self.assertEqual('Bili', lab_t_bili.text)
        self.assertEqual('5.63', lab_t_bili.value)
        self.assertEqual('mg/dL', lab_t_bili.units)

    def test_total_protein(self):
        lab_total_protein = HepcLabReader('Total Prot	5.9	g/dL').first_lab()

        self.assertEqual('Prot', lab_total_protein.text)  # TODO: warning: too broad?
        self.assertEqual('5.9',  lab_total_protein.value)
        self.assertEqual('g/dL', lab_total_protein.units)

