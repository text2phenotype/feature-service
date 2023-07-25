from feature_service.features import Polarity
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase, MatchHintVectorizeBase


class PolarityAnnotateTests(AnnotateTestsBase):

    def test_polarity_annotate_positive(self):

        target = Polarity()

        kwargs = {"feature_name": "POSITIVE"}
        actual = target.annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        # 2 positive hits
        self.assertTrue(len(actual), 2)

    def test_polarity_annotate_yes(self):

        target = Polarity()

        kwargs = {"feature_name": "YES"}
        actual = target.annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        # 9 yes hits
        self.assertTrue(len(actual), 9)
        self.assertTrue(self.find_polarity_type_match('YES', actual, **kwargs))
        self.assertTrue(self.find_polarity_type_match('yes', actual, **kwargs))

    def test_polarity_annotate_no(self):

        target = Polarity()

        kwargs = {"feature_name": "NO"}
        actual = target.annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        # 24 no positive hits
        self.assertTrue(len(actual), 24)
        self.assertTrue(self.find_polarity_type_match('No', actual, **kwargs))
        self.assertTrue(self.find_polarity_type_match('no', actual, **kwargs))
        self.assertTrue(self.find_polarity_type_match('not', actual, **kwargs))
        self.assertTrue(self.find_polarity_type_match('NO', actual, **kwargs))

    def test_polarity_annotate_change(self):

        target = Polarity()

        kwargs = {"feature_name": "CHANGE"}
        actual = target.annotate(self.TEST_INPUT_CAROLYN, **kwargs)

        # 2 change  hits
        self.assertTrue(len(actual), 2)
        self.assertTrue(self.find_polarity_type_match('changes', actual, **kwargs))

    def test_polarity_annotate_deny(self):

        target = Polarity()

        kwargs = {"feature_name": "DENY"}
        actual = target.annotate(self.TEST_INPUT_DVAUGHAN_SUBSET, **kwargs)

        # 1 deny hit
        self.assertTrue(len(actual), 1)
        self.assertTrue(self.find_polarity_type_match('denied', actual, **kwargs))

    def test_polarity_annotate_without(self):

        target = Polarity()

        kwargs = {"feature_name": "WITHOUT"}
        actual = target.annotate(self.TEST_INPUT_DVAUGHAN_SUBSET, **kwargs)

        # 1 without hit
        self.assertTrue(len(actual), 1)
        self.assertTrue(self.find_polarity_type_match('without', actual,  **kwargs))

    def test_polarity_annotate_negative(self):

        target = Polarity()

        kwargs = {"feature_name": "NEGATIVE"}
        actual = target.annotate(self.TEST_INPUT_DVAUGHAN_SUBSET, **kwargs)

        # 1 negative hit
        self.assertTrue(len(actual), 1)
        self.assertTrue(self.find_polarity_type_match('negative', actual, **kwargs))


class PolarityVectorizeTests(MatchHintVectorizeBase):
    def test_polarity_vectorize_no_matches(self):
        """ Test Polarity vector length"""
        self._test_vectorize_no_match(Polarity())

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(Polarity(), exclusions={'CHANGE_NO', 'RULEOUT_NO'})

    def test_change_no(self):
        self._test_vectorize('unchanged', Polarity(), [Polarity.CONST_KEYS['CHANGE_NO']])

    def test_ruleout_no(self):
        self._test_vectorize('cannot rule out', Polarity(), [Polarity.CONST_KEYS['RULEOUT_NO']])

