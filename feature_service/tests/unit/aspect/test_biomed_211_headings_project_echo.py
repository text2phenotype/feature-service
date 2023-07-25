import unittest
from feature_service.feature_set.feature_cache import FeatureCache


class TestBiomed211(unittest.TestCase):
    def setUp(self) -> None:
        self.aspect_map = FeatureCache().aspect_map()

    def assertHeadingsExists(self, expected: list):
        for heading in expected:
            heading = heading.upper().strip()
            self.assertIn(heading, self.aspect_map)

    def test_biomed_211(self):
        expected = [
            'Reason for Consultation',
            'History of Present Illness',
            'Review of Systems',
            'Allergies',
            'Medications',
            'Problem List',
            'Family History',
            'Social History',
            'Physical Exam',
            'Assessment/Plan',
            'Results',
            'FINDINGS',
        ]
        self.assertHeadingsExists(expected)

    @unittest.skip('JIRA/BIOMED-228')
    def test_biomed_228_provider_legal_sections(self):
        """
        These headings should be added to improve Aspect Mapping from known headers.
        """
        expected = [
            'Consult Requestor',
            'Review of Systems',
            'Encounter info',
            'Signature Line',
            'Completed Action List'
        ]
        self.assertHeadingsExists(expected)
