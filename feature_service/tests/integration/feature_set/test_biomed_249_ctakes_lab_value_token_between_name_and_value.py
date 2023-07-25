import unittest

from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed249(unittest.TestCase):

    def assertLabValue(self, text, expected) -> None:
        """
        :param text: str contains lab name and value
        :param expected: the expected lab value
        """
        actual = HepcLabReader(text).list_lab_values()

        self.assertIn(expected, actual)

    def assertMilligramLabUnits(self, text) -> None:
        """
        :param text:
        :return:
        """
        reader = HepcLabReader(text)

        self.assertNotIn('mg', reader.list_result_text())
        self.assertNotIn('mg', reader.list_concept_text())
        self.assertNotIn('Mg', reader.list_concept_text())
        self.assertNotIn('MG', reader.list_concept_text())

        self.assertEqual(1, reader.count_results())
        self.assertEqual(1, reader.count_labs())

    def test_lab_value_token_between_match_and_value(self):

        self.assertLabValue('platelet count is 723,000', '723,000')
        self.assertLabValue('platelet count was 723,000', '723,000')
        self.assertLabValue('platelet count of 723,000', '723,000')
        self.assertLabValue('Hematocrit was 40', '40')
        self.assertLabValue('The patient’s CBC showed a white blood cell count of 24,000', '24,000')
        self.assertLabValue('which showed a pH of 7.02', '7.02')

    def test_diagnostic_data(self):  # TODO: more LabReader improvements to get at Lab Entity Types
        text = """
        DIAGNOSTIC DATA: The patient’s admission laboratory data was notable for his 
        initial blood gas, which showed a pH of 7.02 with a pCO2 of 118 and a pO2 of 103. 
        The patient’s electrocardiogram  showed nonspecific ST-T wave changes. 
        The patent’s CBC showed a white count of 24,000, with 56% neutrophils and 3% bands.         
        """
        self.assertLabValue(text, '7.02')
        self.assertLabValue(text, '118')
        self.assertLabValue(text, '103')
        self.assertLabValue(text, '24,000')
        self.assertLabValue(text, '56')

    # JIRA/BIOMED-320
    def test_milligram_lab_units(self):

        self.assertMilligramLabUnits('hemoglobin 20 mg/L')
        self.assertMilligramLabUnits('Hemoglobin 20 mg/L')
        self.assertMilligramLabUnits('Hemoglobin A1C 20 mg/L')
