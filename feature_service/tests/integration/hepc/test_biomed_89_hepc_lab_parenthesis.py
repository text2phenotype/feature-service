import unittest

from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed89(unittest.TestCase):

    def assertLabAFP(self, text):

        lab_afp = HepcLabReader(text).first_lab()

        self.assertEqual(30, int(lab_afp.value))
        self.assertEqual('ng/ml', lab_afp.units)

    def test_lab_afp(self):
        self.assertLabAFP('AFP (Alpha feto protein level) 30 ng/ml')
        self.assertLabAFP('(Alpha feto protein level) 30 ng/ml')
        self.assertLabAFP('Result (Alpha feto protein level) 30 ng/ml')
