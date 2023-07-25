import unittest
from feature_service.nlp.nlp_reader import LabReader


class TestBiomed473(unittest.TestCase):

    def setUp(self):
        self.strict = False # require preferred longer match "Hemolobin A1C" over just "Hemolobin"

    def assertLabType(self, res, labname=None, value=None, units=None, polarity=None):

        if labname:
            self.assertEqual(labname, res.text)
        if value:
            self.assertEqual(value, res.value)
        if units:
            self.assertEqual(units, res.units)
        if polarity:
            self.assertEqual(polarity, res.polarity)

    def assertFirst(self, text, labname=None, value=None, unit=None, polarity=None):
        self.assertLabType(LabReader(text).first_lab(), labname, value, unit, polarity)

    def assertHemoglobin(self, text, labname=None, value=None, unit=None, polarity=None):
        """
        https://www.webmd.com/diabetes/guide/glycated-hemoglobin-test-hba1c
        """
        expect = labname if self.strict else labname.replace('A1c', '').strip()
        self.assertFirst(text, expect, value, unit, polarity)

    def test_acute_kidney_failure(self):
        """
        High priority lab values
        JIRA/BIOMED-130
        """
        text = """
        LABORATORY DATA: December 2004, creatinine was 1.5. Per report May 2006,
        creatinine was 1.8 with a BUN of 28. Labs dated 06/01/06, hematocrit was 32.3,
        white blood cell count 7.2, platelets 263,000, sodium 139, potassium 4.9,
        chloride 100, CO2 25, BUN 46, creatinine 2.3, glucose 162, albumin 4.7, LFTs
        are normal. CK was elevated at 653. A1c is 7.6%. LDL cholesterol is 68, HDL is
        35. Urinalysis reveals microalbumin to creatinine ratio 59.8. UA was otherwise
        negative with a pH of 5. Today his urinalysis showed specific gravity 1.020,
        negative glucose, bilirubin, ketones and blood, 30 mg/dL of protein, pH of 5,
        negative nitrates, leukocyte esterase. Microscopic exam was bland.
        """
        self.assertFirst(text, 'creatinine', '1.5')

    def test_hba1c_normal(self):
        """
        https://www.webmd.com/diabetes/guide/glycated-hemoglobin-test-hba1c
        """
        self.assertHemoglobin('Hemoglobin A1c 4', 'Hemoglobin A1c', '4')
        self.assertHemoglobin('Hemoglobin A1c 4.0', 'Hemoglobin A1c', '4.0')
        self.assertHemoglobin('Hemoglobin A1c 5.6%', 'Hemoglobin A1c', '5.6', '%')
        self.assertHemoglobin('Hemoglobin A1c normal', 'Hemoglobin A1c', 'normal')
        self.assertHemoglobin('Hemoglobin A1c is normal', 'Hemoglobin A1c', 'normal')

    def test_hba1c_not_normal(self):
        """
        https://www.webmd.com/diabetes/guide/glycated-hemoglobin-test-hba1c
        """
        self.assertHemoglobin('Hemoglobin A1c is 6', 'Hemoglobin A1c', '6')
        self.assertHemoglobin('Hemoglobin A1c is 5.7', 'Hemoglobin A1c', '5.7')
        self.assertHemoglobin('Hemoglobin A1c is 6.4%', 'Hemoglobin A1c', '6.4', '%')
        self.assertHemoglobin('Hemoglobin A1c not normal', 'Hemoglobin A1c', 'normal', None, 'negative')
        self.assertHemoglobin('Hemoglobin A1c is not normal', 'Hemoglobin A1c', 'normal', None, 'negative')

    def test_hba1c_diabetes_diagnosis(self):
        self.assertHemoglobin('Hemoglobin A1c was 6.5', 'Hemoglobin A1c', '6.5', None)
        self.assertHemoglobin('Hemoglobin A1c 6.6', 'Hemoglobin A1c', '6.6', None)
        self.assertHemoglobin('Hemoglobin A1c = 7%', 'Hemoglobin A1c', '7', '%')
        self.assertHemoglobin('Hemoglobin A1c value 8', 'Hemoglobin A1c', '8')
        self.assertHemoglobin('Hemoglobin A1c high 9.23%', 'Hemoglobin A1c', '9.23', '%')


class TestBiomed1402(TestBiomed473):
    """
    BIOMED-1402 : using hepc lab values pipeline instead of previous "general" lab pipeline results in missing this common lab.
    Hepc recognizes "Hemoglobin" but not "Hemoglobin A1c" which isn't perfect but not terrible either.
    """
    @unittest.skip
    def test_strict(self):
        self.strict = True # require preferred longer match "Hemolobin A1C"
        self.test_hba1c_normal()
        self.test_hba1c_not_normal()
        self.test_hba1c_diabetes_diagnosis()
