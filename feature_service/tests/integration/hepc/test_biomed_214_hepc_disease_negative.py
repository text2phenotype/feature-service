import unittest

from feature_service.nlp.nlp_reader import HepcReader, HepcLabReader

TEXT_NEGATIVE_HEPATITIS = 'He has never had any treatment in the past for his chronic hepatitis C.'
TEXT_NEGATIVE_HCV = 'He has never had any treatment in the past for his HCV.'


class TestBiomed214(unittest.TestCase):

    def assertLabNone(self, text):
        self.assertEqual(0, HepcLabReader(text).count_results())

    def assertNegative(self, text):
        reader = HepcReader(text)

        self.assertGreater(reader.count_results(), 0)

        for r in reader.list_results():
            self.assertEqual('negative', r.attributes.polarity)

    def test_polarity_negative_for_hcv(self):

        for text in [TEXT_NEGATIVE_HCV, TEXT_NEGATIVE_HEPATITIS]:
            self.assertLabNone(text)
            self.assertNegative(text)
