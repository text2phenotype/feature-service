import unittest
from feature_service.feature_set.umls import match_vocab, vectorize
from feature_service.nlp.nlp_reader import ClinicalReader, LabReader

from feature_service.nlp import autocode
from text2phenotype.constants import umls


class TestBiomed199_Vocab(unittest.TestCase):

    def test_vectorize_drug(self):
        self.assertEqual([1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                         vectorize(match_vocab(umls.DRUG_VOCAB, ['RXNORM', 'SNOMEDCT_US', 'MMSL'])))

    def test_vectorize_problem(self):
        self.assertEqual([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                         vectorize(match_vocab(umls.PROBLEM_VOCAB, ['SNOMEDCT_CORE', 'CHV', 'RCDAE', 'BI'])))

    def test_vectorize_diagnosis(self):
        self.assertEqual([1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                         vectorize(match_vocab(umls.DIAGNOSIS_VOCAB, ['ICD10CM', 'CCS_10', 'NCI', 'MTH'])))

    def test_vectorize_lab(self):
        self.assertEqual([1, 1, 0, 1],
                         vectorize(match_vocab(umls.LAB_VOCAB, ['LNC', 'LNC2000', 'LNCICU'])))

    def test_vectorize(self):
        self.assertEqual([0, 0, 1] + [0] * 41 + [1, 0, 1],
                         vectorize(match_vocab(umls.Vocab, ['BI', 'SNOMEDCT_US', 'VANDF'])))

    def test_dimension(self):
        self.assertEqual(47, len(list(umls.Vocab)))

    def test_dimension_drug(self):
        self.assertEqual(12, len(self.drug('aspirin 50 mg twice daily')))
        self.assertEqual(len(set(umls.DRUG_VOCAB)), len(umls.DRUG_VOCAB))

    def test_dimension_problem(self):
        self.assertEqual(17, len(self.problem('heart attack')))
        self.assertEqual(len(set(umls.PROBLEM_VOCAB)), len(umls.PROBLEM_VOCAB))

    def test_dimension_diagnosis(self):
        self.assertEqual(20, len(
            self.diagnosis('Acute myocardial infarction of unspecified site, initial episode of care')))
        self.assertEqual(20, len(self.diagnosis('AMI NOS, initial')))
        self.assertEqual(len(set(umls.DIAGNOSIS_VOCAB)), len(umls.DIAGNOSIS_VOCAB))

    def assertVocabSet(self, expected, actual):
        """
        assert simple set of vocabs
        """
        expected = set(list(filter(None, list(expected))))
        actual = set(list(filter(None, list(actual))))
        self.assertEqual(expected, actual)

    def test_diagnosis(self):
        self.assertVocabSet({'MSH', 'NDFRT', 'NCI'}, self.diagnosis('heart attack'))

        self.assertVocabSet({'ICD9CM'}, self.diagnosis('AMI NOS, initial'))

        self.assertVocabSet({'NCI', 'ICD9CM'}, self.diagnosis('Acute MI'))

        self.assertVocabSet({'NCI', 'NDFRT', 'ICD9CM', 'MSH'}, self.diagnosis('Acute myocardial infarction'))
        self.assertVocabSet({'NCI', 'NDFRT', 'ICD9CM', 'MSH'},
                            self.diagnosis('Acute myocardial infarction of unspecified site'))
        self.assertVocabSet({'NCI', 'NDFRT', 'ICD9CM', 'MSH'},
                            self.diagnosis('Acute myocardial infarction of unspecified site, initial episode of care'))

    def test_problem(self):
        self.assertVocabSet({'MSH', 'NCI'}, self.problem('heart attack'))
        self.assertVocabSet({'NCI'}, self.problem('Acute MI'))

        self.assertEqual(
            [None, None, None, None, None, None, 'NCI', None, None, None, None, None, None, None, None, None, None],
            self.problem('Acute MI'))

        self.assertEqual(
            [None, None, 'MSH', None, None, None, 'NCI', None, None, None, None, None, None, None, None, None, None],
            self.problem('Acute Myocardial Infarction'))

    def diagnosis(self, example: str):
        return match_vocab(umls.DIAGNOSIS_VOCAB, ClinicalReader(self.autocode_general(example)).list_concept_vocab())

    def problem(self, example: str):
        return match_vocab(umls.PROBLEM_VOCAB, ClinicalReader(self.autocode_general(example)).list_concept_vocab())

    def drug(self, example: str):
        return match_vocab(umls.DRUG_VOCAB, ClinicalReader(self.autocode_general(example)).list_concept_vocab())

    def lab(self, example: str):
        return match_vocab(umls.LAB_VOCAB, LabReader(self.autocode_general(example)).list_concept_vocab())

    def autocode_general(self, example: str):
        return autocode.autocode(example, autocode.dest(autocode.Vocab.general))
