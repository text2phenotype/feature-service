import unittest

from text2phenotype.common.speech import tokenize


class TestBiomed75(unittest.TestCase):

    @unittest.skip('JIRA/BIOMED-75')
    def test_nltk_tokenizer_colon(self):
        tokens = tokenize('MRN:53023691')

        self.assertEqual(len(tokens), 3)
