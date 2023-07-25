from feature_service.features import Sectionizer
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class SectionizerAnnotateTests(AnnotateTestsBase):

    def test_date_regex_annotate(self):

        target = Sectionizer()

        actual = target.annotate(self.TEST_INPUT_CAROLYN)

        # there should be 3 page headers
        self.assertEqual(self.find_match_count('PAGE_HEADER', actual), 3)

        # there should be a bunch of these
        self.assertTrue(self.find_match('HEADER_TITLE', actual))
        self.assertTrue(self.find_match('HEADER_COLON', actual))
        self.assertTrue(self.find_match('SUBHEADER_COLON', actual))
        self.assertTrue(self.find_match('LIST', actual))
