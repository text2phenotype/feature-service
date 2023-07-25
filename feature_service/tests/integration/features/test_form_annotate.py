from feature_service.features import Form
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class FormAnnotateTests(AnnotateTestsBase):

    def test_form_annotate(self):
        target = Form()
        actual = target.annotate(self.TEST_INPUT_DVAUGHAN_SUBSET)

        # TODO Muhammad, revisit this if bug is fixed to capture DOB
        # should have 5 items in the list
        self.assertEqual(len(actual), 4)

        # test for the different matches that should be returned
        self.assertTrue(self.find_match('End-stage renal disease', actual))
        self.assertTrue(self.find_match('Diabetes', actual))
        self.assertTrue(self.find_match('Protein', actual))
        self.assertTrue(self.find_match('male', actual))
        # self.assertTrue(self.find_match('DOB', actual))

    # def test_form_annotate_dob(self):
    #    target = Form()
    #    blurb = '''DOB:1940-07-18 Sex:Male'''
    #    actual = target.annotate(blurb)
    #    self.assertTrue(self.find_match('DOB', actual))

    # valid entries:
    # '''DOB:1940-07-18'''
    # '''DOB:1940-07-18 '''
    # '''DOB:1940-07-18. Sex:Male'''
    # '''DOB:1940-07-18.  Sex:Male'''
    # '''Sex:Male DOB:1940-07-18'''
    # '''Sex:Male.  DOB:1940-07-18'''
    # '''Sex:Male
    #   DOB:1940-07-18'''

    # invalid entries:
    # '''DOB:1940-07-18.''' .
    # '''DOB:1940-07-18.   Sex:Male'''  . & 3 spaces
    # '''DOB:1940-07-18 Sex:Male''' 1 space
    # '''DOB:1940-07-18  Sex:Male''' 2 spaces
