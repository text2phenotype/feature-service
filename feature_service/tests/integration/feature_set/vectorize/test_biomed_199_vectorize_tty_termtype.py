import unittest

from text2phenotype.constants import umls
from feature_service.feature_set.umls import vectorize, match_termtype


class TestBiomed199_TermType(unittest.TestCase):

    def test_dimension_drug(self):
        self.assertEqual(16, len(list(umls.DRUG_TTY)))
        self.assertEqual([0] * 16, vectorize(match_termtype(umls.DRUG_TTY, list())))

    def test_dimension_diagnosis(self):
        self.assertEqual(8, len(list(umls.DIAGNOSIS_TTY)))
        self.assertEqual([0] * 8, vectorize(match_termtype(umls.DIAGNOSIS_TTY, list())))

    def test_vectorize_drug_psn_prescribable_name(self):
        psn = match_termtype(umls.DRUG_TTY, ['PSN'])

        self.assertEqual(['PSN']+[None]*15, psn)
        self.assertEqual([1] + [0] * 15, vectorize(psn))

    def test_vectorize_diagnosis_pt_preferred_term(self):
        pt = match_termtype(umls.DIAGNOSIS_TTY, ['PT'])

        self.assertEqual(['PT'] + [None] * 7, pt)

        self.assertEqual([1] + [0] * 7, vectorize(pt))

    def test_vectorize_diagnosis_syn_abbreviation_lower_level_term(self):
        syn = match_termtype(umls.DIAGNOSIS_TTY, ['SY', 'AB', 'LLT'])

        self.assertEqual([None, 'AB', None, None, 'SY', None, 'LLT', None], syn)
        self.assertEqual([0, 1, 0, 0, 1, 0, 1, 0], vectorize(syn))

    def test_vectorize_lab(self):
        self.assertEqual(4, len(list(umls.LAB_TTY)))
        self.assertEqual([0, 0, 0, 0], vectorize(match_termtype(umls.LAB_TTY, ['useless_tty'])))
        self.assertEqual([1, 0, 0, 0], vectorize(match_termtype(umls.LAB_TTY, ['COMP'])))
        self.assertEqual([0, 1, 1, 1], vectorize(match_termtype(umls.LAB_TTY, ['useless', 'OSN', 'LC', 'LN'])))
        self.assertEqual([1, 1, 1, 1], vectorize(match_termtype(umls.LAB_TTY, ['COMP', 'OSN', 'LC', 'LN'])))
