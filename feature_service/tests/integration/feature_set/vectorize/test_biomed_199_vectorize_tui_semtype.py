import unittest

from text2phenotype.constants import umls
from feature_service.nlp.nlp_reader import ClinicalReader, DrugReader
from feature_service.feature_set.umls import vectorize, match_tui


###############################################################################
#
# Test Vectorization
#
###############################################################################

class TestBiomed199AspectTUI(unittest.TestCase):

    def test_vectorize(self):
        self.assertEqual(30, len(list(umls.TUI)))
        self.assertEqual([1] + [0] * 28 + [1],
                         vectorize(match_tui(umls.TUI, ['T019', 'T203'])))

    def test_vectorize_drug_tui(self):
        """
        Drug TUI is provided mostly by RXNORM (and some synonyms)
        """
        self.assertEqual([1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         vectorize(match_tui(umls.DRUG_TUI, ['T109', 'T121'])))

    def test_vectorize_problem_tui(self):
        """
        problem and diagnosis TUI are the same
        """
        self.assertEqual([0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                         vectorize(match_tui(umls.PROBLEM_TUI, ['T046', 'T047'])))

    def test_vectorize_lab_tui(self):
        """
        there is only one lab TUI, there is no reason to have a TUI feature for lab.
        +------+--------------------+-------+----------+
        | TUI  | STY                | cnt   | prct     |
        +------+--------------------+-------+----------+
        | T201 | Clinical Attribute | 66670 | 100.0000 |
        +------+--------------------+-------+----------+
        """
        pass

    def test_dimension_default_clinical(self):
        self.assertEqual(30, len(match_tui(umls.TUI, ClinicalReader('patient had a disease').list_concept_tuis())))

    def test_dimension_drug(self):
        self.assertEqual(12, len(self.drug('aspirin')))

    def test_dimension_problem(self):
        self.assertEqual(10, len(self.problem('heart attack')))

    def test_drug(self):

        self.assertEqual(  # Organic Chemical + Pharmacologic Substance
            ['T109', None, 'T121', None, None, None, None, None, None, None, None, None],
            self.drug('hydroxyamphetamine'))

        self.assertEqual(  # Organic Chemical + Pharmacologic Substance + VITAMIN
            [None, None, 'T121', None, 'T125', 'T127', None, None, None, None, None, None],
            self.drug('Vitamin D'))

        self.assertEqual(  # NUCLEIC ACID + Biologically Active Substance
            [None, None, None, 'T123', None, None, None, None, None, None, None, None],
            self.drug('Thymine'))

        self.assertEqual(  # Amino Acid, Peptide, or Protein + Pharmacologic Substance + IMMUNE FACTOR
            [None, 'T116', 'T121', None, None, None, 'T129', None, None, None, None, None],
            self.drug('hepatitis B immune globulin'))

        self.assertEqual(  # Organic Chemical + Pharmacologic Substance + Biologically Active Substance
            ['T109', None, 'T121', 'T123', None, None, None, None, None, None, None, None],
            self.drug('Heparin Co-Factor I'))

        self.assertEqual(  # Amino Acid, Peptide, or Protein + Pharmacologic Substance
            [None, 'T116', 'T121', None, None, None, None, None, None, None, None, None],
            self.drug('Antithrombin III'))

        # self.assertEqual(  # BIOMEDICAL OR DENTAL MATERIAL
        #     [None, None, None, None, 'T122', None, None, None, None, None, None, None],
        #     self.drug('Sublingual Powder'))

        self.assertEqual(  # Amino Acid, Peptide, or Protein + Pharmacologic Substance + Biologically Active Substance
            [None, 'T116', 'T121', 'T123', None, None, None, None, None, None, None, None],
            self.drug('Coagulation factor IX'))

        self.assertEqual(  # Organic Chemical  + Pharmacologic Substance + HORMONE
            ['T109', None, 'T121', None, 'T125', None,  None,  None, None, None,  None,  None],
            self.drug('Estrogens'))

        self.assertEqual(  # Pharmacologic Substance + Inorganic Chemical
            [None, None, 'T121', None, None, None, None, None, None, 'T197', None, None],
            self.drug('Potassium nitrate'))

    @unittest.skip('BIOMED-199')
    def ignore_test_drug_T200_clinical_drug(self):
        self.assertEqual(  # Clinical Drug
            [None, None, None, None, None, None, None, None, None, None, None, 'T200', None],
            self.drug('Potassium nitrate'))

    @unittest.skip('BIOMED-199')
    def ignore_test_drug_T203_drug_delivery_device(self):
        self.assertEqual(  # Clinical Drug
            [None, None, None, None, None, None, None, None, None, None, None, None, 'T203'],
            self.drug('Low-Ogestrel 28 Day Pack'))

    def test_problem(self):
        self.assertEqual(  # Congenital Abnormality
            ['T019', None, None, None, None, None, None, None, None, None],
            self.problem('Megalogastria'))

        self.assertEqual(  # Acquired Abnormality
            [None, 'T020', None, None, None, None, None, None, None, None],
            self.problem('Vaginal Prolapse'))

        self.assertEqual(  # Finding
            [None, None, 'T033', None, None, None, None, None, None, None],
            self.problem('Hyperventilation'))

        self.assertEqual(  # Injury or poison
            [None, None, None, 'T037', None, None, None, None, None, None],
            self.problem('Head Injury'))

        self.assertEqual(  # Disease with Pathologic Function
            [None, None, None, None, 'T046', 'T047', None, None, None, None],
            self.problem('Acute Myocardial Infarction'))

        self.assertEqual(  # Disease (will also match drug endpoint for protein)
            [None, None, None, None, None, 'T047', None, None, None, None],
            self.problem('hepatitis B immune globulin'))

        self.assertEqual(  # Mental or Behavioral Dysfunction
            [None, None, None, None, None, None, 'T048', None, None, None],
            self.problem('Paranoid schizophrenia'))

        self.assertEqual(  # Sign or Symptom
            [None, None, None, None, None, None, None, 'T184', None, None],
            self.problem('POLYDIPSIA'))

        self.assertEqual(  # Sign or Symptom
            [None, None, None, None, None, None, None, 'T184', None, None],
            self.problem('Excessive thirst'))

        self.assertEqual(  # Congenital Abnormality + Sign Symptom
            ['T019', None, None, None, None, None, None, 'T184', None, None],
            self.problem('Congenital koilonychia'))

        self.assertEqual(  # Congenital Abnormality
            [None, None, None, None, None, None, None, None, 'T190', None],
            self.problem('Ventricular septal defect'))

        self.assertEqual(  # Neoplastic Process
            [None, None, None, None, None, None, None, None, None, 'T191'],
            self.problem('Breast Cancer'))

    def problem(self, example: str):
        return match_tui(umls.PROBLEM_TUI, ClinicalReader(example).list_concept_tuis())

    def drug(self, text: str):
        return match_tui(umls.DRUG_TUI, DrugReader(text).list_concept_tuis())


if __name__ == '__main__':
    unittest.main()
