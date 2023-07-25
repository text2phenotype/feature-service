import unittest
from typing import Optional

from feature_service.hep_c.form import autofill_hepc_form


class TestBiomed154(unittest.TestCase):

    @staticmethod
    def get_evidence(form: dict, question: str):
        """
        :param form hepc_form autofill response
        :param question: specific form question
        :return: evidence json or None
        """
        for header, suggest in form.items():
            for s in suggest:
                if s['suggest'] == question:
                    return s['evidence']
        return None

    def assertEvidence(self, form: dict, question: str, expected: Optional[bool] = True):

        if expected is True:
            self.assertIsNotNone(self.get_evidence(form, question))

        elif expected is None:
            self.assertIsNone(self.get_evidence(form, question))

    def test_hepatitis_a_and_b_vaccines(self):
        form = autofill_hepc_form('Hepatitis B immunization')

        self.assertEvidence(form, 'hep_a_immunity', expected=None)
        self.assertEvidence(form, 'hep_b_immunity', expected=True)

        self.assertEvidence(form, 'hcv_diagnosis', expected=None)
        self.assertEvidence(form, 'hcv_prev_treatment', expected=None)
        self.assertEvidence(form, 'hcv_prev_treatment_drugs', expected=None)
