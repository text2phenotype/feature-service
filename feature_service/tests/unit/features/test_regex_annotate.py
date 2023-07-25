from feature_service.features import DateRegEx, AllergyRegex
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class RegExAnnotateTests(AnnotateTestsBase):
    def test_date_regex_annotate(self):

        target = DateRegEx()

        kwargs = {}
        actual = target.annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        # all of these should be regex hits in the text
        self.assertTrue(self.find_match('$DATE_SEPARATORS', actual))
        self.assertTrue(self.find_match('$DATE', actual))
        self.assertTrue(self.find_match('$DATE1', actual))
        self.assertTrue(self.find_match('$DATE2', actual))
        self.assertTrue(self.find_match('$DATE12', actual))
        self.assertTrue(self.find_match('$YEAR_CENTURY', actual))

    def test_allergy_regex_annotate(self):

        target = AllergyRegex()
        actual = target.annotate(self.TEST_INPUT_CAROLYN)

        self.assertTrue(self.find_match('$ALLERG', actual))
