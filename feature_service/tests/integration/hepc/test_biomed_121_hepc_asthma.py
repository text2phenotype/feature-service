import unittest

from feature_service.hep_c.form import autofill_hepc_form
from text2phenotype.entity.attributes import Polarity


class TestBiomed121(unittest.TestCase):

    @unittest.skip('JIRA/BIOMED-121')
    def test_asthma(self):
        form = autofill_hepc_form('asthma does not disturb sleep')

        for dx in form['DIAGNOSIS_OTHER']:
            if dx['suggest'] == 'asthma':
                polarity = Polarity(dx['evidence']['polarity'])

                self.assertTrue(polarity.is_positive())
