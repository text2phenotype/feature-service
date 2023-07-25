import unittest

from feature_service.nlp.nlp_reader import LabReader
from text2phenotype.entity.accuracy import Accuracy

from feature_service.nlp import autocode


class TestBiomed130(unittest.TestCase):

    ###############################################################################
    #
    # asert Accuracy
    #
    ###############################################################################
    def assertAccuracy(self, expected: set, actual: set):
        """
        :param expected: truth set
        :param actual:   recognized set
        """
        self.assertAccuracyThreshold(expected, actual, recall=0, precision=0)

    def assertAccuracyThreshold(self, expected: set, actual: set, recall=0.8, precision=0.8):
        """
        :param expected: truth set
        :param actual:   recognized set
        :param recall:   float threshold ( or None )
        :param precision: float threshold ( or None )
        """
        accuracy = Accuracy().compare_sets(expected, actual)

        if recall:
            self.assertGreaterEqual(accuracy.recall(), recall)

        if precision:
            self.assertGreaterEqual(accuracy.precision(), recall)

    ###############################################################################
    #
    # assert Panel
    #
    ###############################################################################

    def assertPanel(self, text, expected: set, values: set):
        self.assertPanelText(text, expected, autocode.lab_value)
        self.assertPanelText(text, expected, autocode.hepc_lab_value)
        self.assertPanelLabValues(text, values, autocode.lab_value)
        self.assertPanelLabValues(text, values, autocode.hepc_lab_value)

    def assertPanelText(self, text, expected: set, pipeline=autocode.lab_value):
        """
        :param text: panel text string containing panel name with lab names and values
        :param expected: the set of lab values found in the text
        :param pipeline: default nlp.lab_value
        ** SEE ALSO nlp.hepc_lab_value**
        :return:
        """
        return self.assertAccuracy(expected, set(LabReader(text, pipeline).list_lab_text()))

    def assertPanelLabValues(self, text, expected: set, pipeline=autocode.lab_value):
        """
        :param text: panel text string containing panel name with lab names and values
        :param expected: the set of lab values found in the text
        :param pipeline: default nlp.lab_value
        ** SEE ALSO nlp.hepc_lab_value**
        :return:
        """
        return self.assertAccuracy(expected, set(LabReader(text, pipeline).list_lab_values()))

    ###############################################################################
    #
    # CBC Complete Blood Count
    #
    ###############################################################################

    TEXT_PANEL_CBC_BLOOD_COUNT = """
    CBC Complete Blood Count Panel
    ----------------------------------
    WBC		9	K/ul
    ANC		68	%	
    HGB		16	g/dL
    HCT		46	%
    Platelets 	24,000	ul
    """

    def test_panel_cbc_complete_blood_count(self):

        text = self.TEXT_PANEL_CBC_BLOOD_COUNT
        expected = {'WBC', 'ANC', 'HGB', 'HCT', 'Platelets'}
        values = {'9', '68', '16', '46', '24,000'}

        self.assertPanel(text, expected, values)

    ###############################################################################
    #
    # BMP Basic Metabolic Panel
    #
    ###############################################################################

    TEXT_PANEL_BMP_METABOLIC = """
    BMP Basic Metabolic Panel
    ----------------------------------
    Creatinine	0.6	mg/dL
    Glucose		79	mg/dL
    BUN		9	mg/dL
    Calcium 	7.3	mg/dL
    C02		23.7	mmol/L
    Chloride 	104	mmol/L
    Potassium	3.5	mmol/L
    Sodium		136	mmol/L
    """

    def test_panel_bmp_metabolic(self):
        text = self.TEXT_PANEL_BMP_METABOLIC
        expected = {'Creatinine', 'Glucose', 'BUN', 'Calcium', 'C02', 'Chloride', 'Potassium', 'Sodium'}
        values = {'0.6', '79', '9', '7.3', '23.7', '104', '3.5', '136'}

        self.assertPanel(text, expected, values)

    ###############################################################################
    #
    # CMP Comprehensive Metabolic Panel
    #
    ###############################################################################
    TEXT_PANEL_CMP_COMPREHENSIVE = """
    CMP Comprehensive Metabolic Panel
    ----------------------------------
    Albumin		2.5	g/dL
    ALT		68	U/L
    AST		56	U/L
    Alk Phos	165	U/L
    T. Bili		5.63	mg/dL
    Direct Bili
    Total Prot	5.9	g/dL
    """

    def test_panel_cmp_comprehensive_metabolic_panel(self):

        text = self.TEXT_PANEL_CMP_COMPREHENSIVE
        expected = {'Albumin', 'ALT', 'AST', 'Alk Phos', 'T. Bili', 'Direct Bili', 'Total Prot'}
        values = {'2.5', '68', '56', '165', '5.63', '5.9'}

        self.assertPanelText(text, expected, autocode.lab_value)
        self.assertPanelText(text, expected, autocode.hepc_lab_value)

        self.assertPanelLabValues(text, values, autocode.lab_value)
        self.assertPanelLabValues(text, values, autocode.hepc_lab_value)

    ###############################################################################
    #
    # LFT Liver Function Test
    #
    ###############################################################################

    TEXT_PANEL_LFT_LIVER_FUNCTION_TEST = """
    LFT Liver Function Tests
    ----------------------------------
    Protime		
    INR		3.84
    Fe    		171	mcg/dL
    tibc		607	mcg/dL 
    Ferritin	494	ng/ml
    Vitamin D 25-OH	18	ng/ml
    AFP	  	30	ng/ml
    """

    def test_panel_lft_liver_function_test(self):
        text = self.TEXT_PANEL_LFT_LIVER_FUNCTION_TEST
        expected = {'Protime', 'INR', 'Fe', 'tibc', 'Ferritin', 'Vitamin D 25-OH', 'AFP'}
        values = {'3.84', '171', '607', '494', '18', '30'}

        self.assertPanelText(text, expected, autocode.lab_value)
        self.assertPanelText(text, expected, autocode.hepc_lab_value)

        self.assertPanelLabValues(text, values, autocode.lab_value)
        self.assertPanelLabValues(text, values, autocode.hepc_lab_value)

    ###############################################################################
    #
    # Viral Genotype
    #
    ###############################################################################
    TEXT_PANEL_VIRAL_TESTS = """
    Viral Tests 
    ----------------------------------------
    HIV Ab		    <1		negative
    HCV Genotype	2		positive
    HCV Viral Load	210,000,000	IU/L
    """

    def test_panel_viral(self):
        text = self.TEXT_PANEL_VIRAL_TESTS
        expected = ['HIV Ab', 'HCV Genotype', 'HCV Viral Load']
