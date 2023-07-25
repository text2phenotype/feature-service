import unittest

from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed90(unittest.TestCase):

    def test_hepc_lab_vitamin_d_25_oh_value_equals_18(self):

        reader = HepcLabReader('Vit D 25-OH 18 ng/ml')

        first = reader.first_lab()

        self.assertEqual(18, int(first.value))
        self.assertEqual('ng/ml', first.units)
