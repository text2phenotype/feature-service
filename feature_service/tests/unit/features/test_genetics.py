import unittest

from feature_service.features.genetics import GenticTestInterpretation


class GenticTestInterpretationTests(unittest.TestCase):
    def test_annotate_positive(self):
        self.__test_annotate('Pt diagnosed with BRCA+ breast cancer.', [((22, 24), ['POSITIVE'])])

    def test_annotate_negative(self):
        self.__test_annotate('Pt diagnosed with BRCA- breast cancer.', [((22, 24), ['NEGATIVE'])])

    def test_annotate_wt(self):
        self.__test_annotate('All genes tested show wild-type.', [((22, 31), ['WILD_TYPE']), ((26, 27), ['NEGATIVE'])])

    def test_annotate_vus(self):
        self.__test_annotate('EGFR identified multiple VUS', [((25, 28), ['VUS'])])

    def test_annotate_mutated(self):
        self.__test_annotate('Gentic testing showed ALK mutants', [((26, 33), ['MUTATED'])])

    def __test_annotate(self, text: str, expected: list):
        self.assertListEqual(sorted(expected), sorted(GenticTestInterpretation().annotate(text)))


if __name__ == '__main__':
    unittest.main()
