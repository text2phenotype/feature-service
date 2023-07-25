import unittest

from feature_service.features import History, SocialHistory, PersonalHistory, FamilyHistory
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class HistoryAnnotateTests(AnnotateTestsBase):
    def test_annotate(self):
        kwargs = {"feature_name": "HISTORY_OF"}

        actual = History().annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        self.assertEqual(len(actual), 10)
        self.assertTrue(self.find_polarity_type_match('HISTORY OF', actual, **kwargs))


class HistoryVectorizeTests(MatchHintVectorizeBase):
    def test_history_vectorize_no_token(self):
        """ Test History with no valid token """
        self._test_vectorize_no_match(History())

    def test_history_vectorize_all(self):
        self._test_vectorize_all_definitions(History())


class FamilyHistoryTests(AnnotateTestsBase, MatchHintVectorizeBase):
    def test_annotate(self):
        kwargs = {"feature_name": "FAMILY_HISTORY"}

        actual = FamilyHistory().annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        self.assertEqual(len(actual), 2)
        self.assertTrue(self.find_polarity_type_match('family history', actual, **kwargs))

    def test_history_vectorize_no_token(self):
        """ Test History with no valid token """
        self._test_vectorize_no_match(FamilyHistory())

    def test_history_vectorize_all(self):
        self._test_vectorize_all_definitions(FamilyHistory())


class SocialHistoryTests(AnnotateTestsBase, MatchHintVectorizeBase):
    def test_annotate_alcohol(self):
        kwargs = {"feature_name": "ALCOHOL"}

        actual = SocialHistory().annotate("Patient drinks Alcohol occasionally", **kwargs)

        self.assertEqual(len(actual), 1)
        self.assertTrue(self.find_polarity_type_match('drinks', actual, **kwargs))

    def test_annotate_social(self):
        kwargs = {"feature_name": "SOCIAL"}

        actual = SocialHistory().annotate("Patient works in the retail business")

        self.assertEqual(len(actual), 1)
        self.assertTrue(self.find_polarity_type_match('works', actual, **kwargs))

    def test_history_vectorize_no_token(self):
        """ Test History with no valid token """
        self._test_vectorize_no_match(SocialHistory())

    def test_history_vectorize_all(self):
        self._test_vectorize_all_definitions(SocialHistory())


class PersonalHistoryTests(AnnotateTestsBase, MatchHintVectorizeBase):
    def test_annotate(self):
        kwargs = {"feature_name": "PERSONAL_HISTORY"}

        actual = PersonalHistory().annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        self.assertEqual(len(actual), 5)
        self.assertTrue(self.find_polarity_type_match('HISTORY OF PRESENT ILLNESS', actual, **kwargs))
        self.assertTrue(self.find_polarity_type_match('PAST SURGICAL HISTORY', actual, **kwargs))
        self.assertTrue(self.find_polarity_type_match('SURGICAL HISTORY', actual, **kwargs))
        self.assertTrue(self.find_polarity_type_match('PERSONAL HISTORY', actual, **kwargs))

    def test_history_vectorize_no_token(self):
        """ Test History with no valid token """
        self._test_vectorize_no_match(PersonalHistory())

    def test_history_vectorize_all(self):
        self._test_vectorize_all_definitions(PersonalHistory())


if __name__ == '__main__':
    unittest.main()
