import unittest

from feature_service.features.family import Family
from feature_service.tests.integration.features.annotate_tests import MatchHintVectorizeBase, AnnotateTestsBase


class FamilyTests(AnnotateTestsBase, MatchHintVectorizeBase):
    feature = Family()

    def test_annotate(self):
        kwargs = {"feature_name": "RELATIVES"}

        actual = self.feature.annotate("Patient's mother has history of heart disease", **kwargs)

        self.assertTrue(self.find_polarity_type_match('mother', actual, **kwargs))

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(self.feature)

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(self.feature)


if __name__ == '__main__':
    unittest.main()
