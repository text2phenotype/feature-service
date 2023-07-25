import unittest

from feature_service.hep_c.form import autofill_hepc_form


class TestBiomed169(unittest.TestCase):

    def test_hiv_negative(self):
        form = autofill_hepc_form('HIV negative')

        for dx in form['DIAGNOSIS_OTHER']:
            if dx['suggest'] == 'hiv':
                self.assertEqual('HIV', dx['evidence']['text'][0])
                self.assertEqual('negative', dx['evidence']['polarity'])
