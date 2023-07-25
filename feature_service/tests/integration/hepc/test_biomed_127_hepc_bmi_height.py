import unittest

from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed127(unittest.TestCase):

    def test_bmi_height_usa(self):

        height = HepcLabReader('height 6 feet 1 inch').first_lab()

        self.assertEqual(height.text, 'height')
        self.assertEqual(height.value, '6')
