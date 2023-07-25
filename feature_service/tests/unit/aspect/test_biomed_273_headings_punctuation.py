import unittest

from text2phenotype.constants.features import FeatureType

from feature_service.aspect.chunker import Chunker
from feature_service.feature_set.feature_cache import FeatureCache


class TestBiomed273(unittest.TestCase):
    def setUp(self) -> None:
        self.chunker = Chunker()
        self.aspect_map = FeatureCache().aspect_map()

    @staticmethod
    def get_headers_with_punctuation():
        return [
            'ADDRESS LINE 1',  # demographics, predicted encounter
            'ADDRESS LINE 2',  # demographics, predicted encounter
            'HOMELESS,ETC.',
            "MOTHER'S NAME",
            "S.S.",
            "Environmental Allergies",
            "CLINICAL INSTRUCTIONS/PATIENT DECISION AIDS",
            "REASON FOR VISIT/CHIEF COMPLAINT"  # aspect map is wrong, actual is problem
            "PROCEDURES AND SURGICAL/MEDICAL HISTORY",
            "REASON FOR VISIT/CHIEF COMPLAINT",
            "PROCEDURES AND SURGICAL/MEDICAL HISTORY",
            "ALLERGIES, ADVERSE REACTIONS, ALERTS",
            "ALLERGIES & ADVERSE REACTIONS",
            "ALLERGIES,  ADVERSE REACTIONS & ALERTS"  # double space ?
            "MEDICAL (GENERAL) HISTORY",
            "ALLERGIES,  ADVERSE REACTIONS & ALERTS",  # double space ?
            "MEDICAL (GENERAL) HISTORY",
            "ASSESSMENT/PLAN",
            "IMPRESSION/PLAN",
            "TEXT2PHENOTYPE_SAMPLES_VERSION",  # SKIP THIS
            "MEDICAL RECORD #",
            "EAR/NOSE/THROAT"
        ]

    def assertChunkerKnownHeader(self, exclude_list=None):

        for header, aspect_type in self.aspect_map.items():
            aspect_type = aspect_type.replace('Aspect.', '')
            expected = aspect_type
            predicted = self.chunker.return_aspect_emb_section_positions_enforce(header)[0][FeatureType.aspect.name]

            if exclude_list:
                if header not in exclude_list:
                    self.assertEqual(expected, predicted)
            else:
                self.assertEqual(expected, predicted)

    def test_headers_punctuation_relax(self):
        self.assertChunkerKnownHeader(exclude_list=self.get_headers_with_punctuation())

    @unittest.skip('JIRA/BIOMED-273')
    def test_headers_punctuation_strict(self):
        self.assertChunkerKnownHeader()
