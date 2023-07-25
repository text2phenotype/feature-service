import unittest

from text2phenotype.common.speech import tokenize


class TestTokenize(unittest.TestCase):
    def test_nltk(self):
        text = """Here is some text. Here is some ""funk "


that makes nltk unhappy.\" """
        for token in tokenize(text):
            start, end = token['range']

            self.assertEqual(text[start:end], token['token'])

    def test_regression_bad_colon_split(self):
        exp_tokens = ['4,', '0:', '10.0', ':']

        for exp_token, obs_token in zip(exp_tokens, tokenize(''.join(exp_tokens))):
            self.assertEqual(exp_token, obs_token['token'])

    def test_regression_quotes(self):
        tokenize("""''-'l was seen and discussed with attending physician Dr/*"MBanoshe!""")

    def test_regression_BIOMED_1421(self):
        tokenize("""'I'.'.'.','','''','','','','''''''''''''''''.\n{}""".format('""'))


if __name__ == '__main__':
    unittest.main()
