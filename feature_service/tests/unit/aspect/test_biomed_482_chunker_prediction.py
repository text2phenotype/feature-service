from enum import Enum
import unittest

from text2phenotype.ccda.section import Aspect
from text2phenotype.constants.features import FeatureType

from feature_service.aspect.chunker import Chunker


class TestBiomed482(unittest.TestCase):
    def setUp(self) -> None:
        self.chunker = Chunker()

    def assertChunker(self, text, expected: Aspect):
        if isinstance(expected, Enum):
            expected = str(expected.name)

        for predicted in self.chunker.return_aspect_emb_section_positions_enforce(text):
            aspect_pred = predicted[FeatureType.aspect.name]
            self.assertEqual(expected, aspect_pred)

    @staticmethod
    def header_lvg(header) -> list:
        """
        :param header: "PATIENT INFO"
        :return: list [PATIENT INFO, PATIENT_INFO:, Patient Info, Patient Info:
        """
        return [header, f"{header}:", f"{header.title()}", f"{header.title()}"]

    def test_chunker_demographics_simple(self):
        simple = ['DEMOGRAPHICS',
                  'PATIENT INFO',
                  'MRN',
                  'DOB',
                  'DATE OF BIRTH',
                  'SEX',
                  'AGE']

        for header in simple:
            for variant in self.header_lvg(header):
                self.assertChunker(variant, Aspect.demographics)

    @unittest.skip('JIRA/BIOMED-482')
    def test_chunker_medical_record_number(self):
        self.assertChunker('MEDICAL RECORD #', Aspect.demographics)
        self.assertChunker('PATIENT ID', Aspect.demographics)
