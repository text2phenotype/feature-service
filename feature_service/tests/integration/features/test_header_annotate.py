from feature_service.features import Header
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class HeaderAnnotateTests(AnnotateTestsBase):

    def test_header_annotate(self):

        target = Header()
        actual = target.annotate(self.TEST_INPUT_DVAUGHAN_SUBSET)

        # should have 6 items in the list
        self.assertEqual(len(actual), 6)

        # test for the different matches that should be returned
        self.assertTrue(self.find_match('DISCHARGE DIAGNOSES', actual))
        self.assertTrue(self.find_match('DIAGNOSES', actual))
        self.assertTrue(self.find_match('HISTORY', actual))
        self.assertTrue(self.find_match('COURSE', actual))
        self.assertTrue(self.find_match('DOB', actual))
        self.assertTrue(self.find_match('PATIENT', actual))


