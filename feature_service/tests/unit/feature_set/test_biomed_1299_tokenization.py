import unittest

from text2phenotype.common import speech


class TestBiomed1299(unittest.TestCase):
    def test_correct_tokenization(self):
        input = "Demographics:Male,1996-21-03,92,Hispanic. The gorilla ate an apple the other day. Phone Number:6504892179 Work Phone;(605)-348-2112"
        tokens = speech.tokenize(input)

        self.assertEqual(len(tokens), 27)
        self.assertIn({'token': 'Male,', 'range': [13, 18], 'speech': 'NNP'}, tokens)
        self.assertIn({'token': '1996-21-03,', 'range': [18, 29], 'speech': 'CD'}, tokens)
        self.assertIn({'token': '92',  'range': [29, 31], 'speech': 'CD'}, tokens)
        self.assertIn({'token': '6504892179', 'range': [95, 105], 'speech': 'CD'}, tokens)
        self.assertIn({'token': '(', 'range': [117, 118], 'speech': '('}, tokens)
        self.assertIn({'token': '-348-2112', 'range': [122, 131], 'speech': 'NN'}, tokens)