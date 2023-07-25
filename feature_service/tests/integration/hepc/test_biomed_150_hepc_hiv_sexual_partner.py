import unittest

from feature_service.hep_c.form import autofill_hepc_form


class TestBiomed150(unittest.TestCase):

    @unittest.skip('JIRA/BIOMED-150')
    def test_hiv_route_of_infection(self):

        form = autofill_hepc_form('HIV')

        for dx in form['ROUTE_OF_INFECTION']:
            if dx['suggest'] == 'sexual_partner_has_hepc':
                self.assertIsNone(dx['evidence'])
