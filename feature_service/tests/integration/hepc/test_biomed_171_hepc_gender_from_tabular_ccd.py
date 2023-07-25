import unittest

from feature_service.hep_c.form import autofill_hepc_form
from text2phenotype.common import common


class TestBiomed171(unittest.TestCase):

    def assertGenderMale(self, text_file: str):
        text = common.read_text(text_file)

        form = autofill_hepc_form(text)

        expected = ['C0086582', 'C3839079', 'C0086582', 'C0432475', 'C1706429', 'C0419384']
        actual = None

        for question in form.get('DEMOGRAPHICS'):
            if question['suggest'] == 'gender':
                evidence = question.get('evidence', None)

                if evidence:
                    cui = evidence.get('cui')
                    self.assertTrue(cui in expected, f'{cui} was not expected')
                    actual = cui

        self.assertIsNotNone(actual)
