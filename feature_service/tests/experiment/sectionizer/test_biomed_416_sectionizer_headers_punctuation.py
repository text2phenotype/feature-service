import unittest
from feature_service.features.sectionizer import Sectionizer

TEST_TEXT = """ADDRESS LINE 1
ADDRESS LINE 2
HOMELESS,ETC.
MOTHER'S NAME
S.S.
Environmental Allergies
CLINICAL INSTRUCTIONS/PATIENT DECISION AIDS
REASON FOR VISIT/CHIEF COMPLAINTPROCEDURES AND SURGICAL/MEDICAL HISTORY
REASON FOR VISIT/CHIEF COMPLAINT
PROCEDURES AND SURGICAL/MEDICAL HISTORY
ALLERGIES, ADVERSE REACTIONS, ALERTS
ALLERGIES & ADVERSE REACTIONS
ALLERGIES,  ADVERSE REACTIONS & ALERTSMEDICAL (GENERAL) HISTORY
ALLERGIES,  ADVERSE REACTIONS & ALERTS
MEDICAL (GENERAL) HISTORY
ASSESSMENT/PLAN
IMPRESSION/PLAN
TEXT2PHENOTYPE_SAMPLES_VERSION
MEDICAL RECORD #
EAR/NOSE/THROAT
"""


class TestBiomed416HeadersPunctuation(unittest.TestCase):

    def test_sectionizer(self):

        expected_matches = [
            {'HEADER_UPPER': ['ADDRESS LINE 1', 0, 14]},
            {'HEADER_UPPER': ['ADDRESS LINE 2', 15, 29]},
            {'HEADER_UPPER': ['HOMELESS,ETC.', 30, 43]},
            {'HEADER_UPPER': ["MOTHER'S NAME", 44, 57]},
            {'HEADER_UPPER': ['S.S.', 58, 62]},
            {'HEADER_TITLE': ['Environmental Allergies', 63, 86]},
            {'HEADER_UPPER': ['CLINICAL INSTRUCTIONS/PATIENT DECISION AIDS', 87, 130]},
            {'HEADER_UPPER': ['REASON FOR VISIT/CHIEF COMPLAINTPROCEDURES AND SURGICAL/MEDICAL HISTORY', 131, 202]},
            {'HEADER_UPPER': ['REASON FOR VISIT/CHIEF COMPLAINT', 203, 235]},
            {'HEADER_UPPER': ['PROCEDURES AND SURGICAL/MEDICAL HISTORY', 236, 275]},
            {'HEADER_UPPER': ['ALLERGIES, ADVERSE REACTIONS, ALERTS', 276, 312]},
            {'HEADER_UPPER': ['ALLERGIES & ADVERSE REACTIONS', 313, 342]},
            {'HEADER_UPPER': ['ALLERGIES,  ADVERSE REACTIONS & ALERTSMEDICAL (GENERAL) HISTORY', 343, 406]},
            {'HEADER_UPPER': ['ALLERGIES,  ADVERSE REACTIONS & ALERTS', 407, 445]},
            {'HEADER_UPPER': ['MEDICAL (GENERAL) HISTORY', 446, 471]},
            {'HEADER_UPPER': ['ASSESSMENT/PLAN', 472, 487]},
            {'HEADER_UPPER': ['IMPRESSION/PLAN', 488, 503]},
            {'HEADER_UPPER': ['TEXT2PHENOTYPE_SAMPLES_VERSION', 504, 525]},
            {'HEADER_UPPER': ['MEDICAL RECORD #', 526, 542]},
            {'HEADER_UPPER': ['EAR/NOSE/THROAT', 543, 558]}
        ]

        found_matches = Sectionizer().match_pattern(TEST_TEXT, 'HEADER')

        for found_match in found_matches:
            key, value = list(found_match.items())[0]
            with self.subTest(pattern=key, parsed_value=value):
                self.assertTrue(found_match in expected_matches,
                                f"Match not found in expected values for pattern {key}.")

        self.assertEqual(len(found_matches), len(expected_matches),
                         "Count of found matches not equal to expected.")
