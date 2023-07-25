import unittest

from feature_service.features import DrugRXNorm


class DrugRXNormAnnotateTests(unittest.TestCase):
    TEST_INPUT = "Presently on Lasix, potassium supplementation, Levaquin, hydralazine 10 mg b.i.d., " \
                 "antibiotic treatments, and thyroid supplementation. ALLERGIES: AMBIEN, CARDIZEM, AND IBUPROFEN."

    def test_drug_rx_norm_annotate_simple(self):
        target = DrugRXNorm()

        actual = list(target.annotate(self.TEST_INPUT))

        # The 9 items are:
        # 0 - Lasix
        # 1 - potassium
        # 2 - levaquin
        # 3 - hydralazine
        # 4 - 10 (dosage)
        # 5 - mg (unit)
        # 6 - ambien
        # 7 - cardizem
        # 8 - ibuprofen

        # there should be 9 items in the list.
        self.assertEqual(len(actual), 9)

        # first item should be Lasix
        self.assertEqual(actual[0][1][0]['Medication'][0]['preferredText'], 'Lasix')
        self.assertEqual(actual[0][1][0]['Medication'][0]['codingScheme'], 'RXNORM')
        self.assertEqual(actual[0][1][0]['Medication'][0]['code'], '202991')
        self.assertEqual(actual[0][1][0]['Medication'][0]['tui'], ['T109', 'T121'])

        # there should be one dosage of 10
        self.assertEqual(actual[4][1][0]['medDosage'], '10')

        # there should be one unit of mg
        self.assertEqual(actual[5][1][0]['medUnit'], 'mg')

