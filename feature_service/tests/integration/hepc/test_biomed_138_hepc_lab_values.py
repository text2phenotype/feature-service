import unittest
from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed138(unittest.TestCase):

    def assertLabValue(self, text, match, value, units=None):
        reader = HepcLabReader(text)
        first = reader.first_lab()

        self.assertEqual(1, reader.count_labs(), f'expected only one lab for text {text}')
        self.assertEqual(match, first.text)
        self.assertEqual(value, first.value)

        if units:
            self.assertEqual(units, first.units)

    def test_labs_numeric(self):
        self.assertLabValue('Albumin 3.5', 'Albumin', '3.5')
        self.assertLabValue('WBC 6.5\n', 'WBC', '6.5')
        self.assertLabValue('WBC 6.5\t', 'WBC', '6.5')
        self.assertLabValue('WBC 6.5', 'WBC', '6.5')  # TODO: fails
        self.assertLabValue('HCV viral load 210,000,000 IU/L', 'HCV viral load', '210,000,000', 'IU/L')

        self.assertLabValue('AFP 30 ng/ml', 'AFP', '30', 'ng/ml')

    def test_lab_as_vitals(self):
        self.assertLabValue('Height 185 cm', 'Height', '185')

    @unittest.skip('JIRA/BIOMED-138')
    def test_labs_interpreted(self):
        # HCV specific, not yet in deployed ctakes dictionary
        # HBV Core Antibody
        self.assertLabValue('HBV Core Ab reactive', 'HBV Core Ab', 'reactive')
        self.assertLabValue('HBV Core Ab\treactive', 'HBV Core Ab', 'reactive')
        self.assertLabValue('HBV Core Ab\tnonreactive', 'HBV Core Ab', 'nonreactive')
        self.assertLabValue('HBV SAg nonreactive', 'HBV SAg', 'nonreactive')
