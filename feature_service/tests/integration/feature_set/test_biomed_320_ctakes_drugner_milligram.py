import unittest

from feature_service.nlp.nlp_reader import DrugReader


class TestBiomed320(unittest.TestCase):

    def assertMilligramNotMagnesium(self, text, expected=None) -> None:
        """
        :param text:
        :param expected:
        :return:
        """
        mentioned = DrugReader(text).uniq_result_text()
        preferred = DrugReader(text).uniq_concept_text()

        self.assertNotIn('mg', mentioned)
        self.assertNotIn('mg', preferred)

        if expected:
            self.assertEqual(1, len(mentioned))
            self.assertEqual(1, len(preferred))

    def test_milligram(self):
        self.assertMilligramNotMagnesium('Aspirin 20 mg', 'aspirin')
        self.assertMilligramNotMagnesium('Colace 100 mg', 'Colace')
        self.assertMilligramNotMagnesium('mg')

    @unittest.skip('JIRA/BIOMED-480')
    def test_aspirin_abbreviation(self):
        self.assertMilligramNotMagnesium('ASA 20 mg', 'aspirin')
