import unittest

from feature_service.features import ZipCode
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class ZipCodeAnnotateTests(AnnotateTestsBase):
    feature = ZipCode()

    TEST_INPUT_5DIGITS = 'Our address is: 1 CALIFORNIA STREET, SAN FRANCISCO, CA 94111.  Visit us anytime.'
    TEST_INPUT_9DIGITS = 'Our address is: 1 CALIFORNIA STREET, SAN FRANCISCO, CA 94111-0111.  Visit us anytime.'
    TEST_INPUT_MULTILINE = '''Our address is:
1 CALIFORNIA STREET
SAN FRANCISCO
CA 94111
Visit us anytime'''

    def test_annotate_5digits(self):
        self.__test_zipcode_annotate(self.TEST_INPUT_5DIGITS, (55, 60))

    def test_annotate_9digits(self):
        self.__test_zipcode_annotate(self.TEST_INPUT_9DIGITS, (55, 65))

    def test_annotate_multiline(self):
        self.__test_zipcode_annotate(self.TEST_INPUT_MULTILINE, (53,  58))

    def __test_zipcode_annotate(self, text, span):
        actual = list(self.feature.annotate(text))

        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0][0], span)  # end pos
        self.assertEqual(actual[0][1][0]['city'], 'SAN FRANCISCO')  # key should be zip code

    def test_zipcode_annotate_invalid_text(self):
        actual = self.feature.annotate('Our address is in San Francisco')

        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()
