from typing import List
import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.annotation import annotate_text
from feature_service.features.cancer import (MorphologyCodeRegex, MorphologyDetails,
                                             TNMStaging, TopographyCodeRegex, TumorGradeCode, TumorGradeTerms,
                                             TopographyBinary, MorphologyBinary)


class TestTopography(unittest.TestCase):
    def test_vectorize_binary_with_match(self):
        test_input = MachineAnnotation(json_dict_input={"topography": {"0": [
            {
                "AnatomicalSite": [
                    {'code': '83299001',
                     'cui': 'C0226924',
                     'tui': 'T030',
                     'tty': 'PT',
                     'preferredText': 'C00.6',
                     'codingScheme': 'SNOMEDCT_US'}],
                "polarity": "positive"}]}, "token": ['breast']})

        actual = TopographyBinary().vectorize(test_input)

        self.assertListEqual([1, 1], actual[0])

    def test_vectorize_binary_no_match(self):
        input_token = MachineAnnotation(json_dict_input={"topography": {"0": []}, "token": ['DOB']})

        actual = TopographyBinary().vectorize(input_token)

        self.assertDictEqual({}, actual)


class TestMorphology(unittest.TestCase):
    def test_vectorize_binary_with_match(self):
        test_input = MachineAnnotation(json_dict_input={"morphology": {"0": [
            {
                "DiseaseDisorder": [
                    {'code': '16741004',
                     'cui': 'C0334233',
                     'tui': 'T191',
                     'tty': 'PT',
                     'preferredText': '8022/3',
                     'codingScheme': 'SNOMEDCT_US'}],
                "polarity": "positive"}]}, "token": ['carcinoma']})

        actual = MorphologyBinary().vectorize(test_input)

        self.assertListEqual([1, 1], actual[0])

    def test_vectorize_binary_no_match(self):
        input_token = MachineAnnotation(json_dict_input={"morphology": {"0": []}, "token": ['DOB']})

        actual = MorphologyBinary().vectorize(input_token)

        self.assertDictEqual({}, actual)


class TestMorphologyDetails(unittest.TestCase):
    def test_canonical(self):
        details = MorphologyDetails('8000/1')

        self.assertEqual('8000', details.histology)
        self.assertEqual('1', details.behavior)
        self.assertIsNone(details.grade)

    def test_grade_present1(self):
        details = MorphologyDetails('8000/13')

        self.assertEqual('8000', details.histology)
        self.assertEqual('1', details.behavior)
        self.assertEqual('3', details.grade)

    def test_grade_present2(self):
        details = MorphologyDetails('8000/1 2')

        self.assertEqual('8000', details.histology)
        self.assertEqual('1', details.behavior)
        self.assertEqual('2', details.grade)

    def test_not_a_code1(self):
        details = MorphologyDetails('8000')

        self.assertIsNone(details.histology)
        self.assertIsNone(details.behavior)
        self.assertIsNone(details.grade)

    def test_not_a_code2(self):
        details = MorphologyDetails('8000/112')

        self.assertIsNone(details.histology)
        self.assertIsNone(details.behavior)
        self.assertIsNone(details.grade)


class TestTopographyCodeRegex(unittest.TestCase):
    def test_annotate_expected_format(self):
        """Test to make sure we match codes in the expected format."""
        exp_code = 'C00.6'
        result = list(TopographyCodeRegex().annotate(f'Topo. code is ({exp_code})'))

        self.assertEqual(1, len(result))

        location, annotations = result[0]
        self.assertEqual((15, 20), location)

        self.assertEqual(2, len(annotations))
        for annotation in annotations:
            self.assertEqual(1, len(annotation))
            self.assertEqual(exp_code, list(annotation.values())[0])

    def test_annotate_format_error1(self):
        """Test to make sure we match codes that contain OCR errors."""
        exp_code = 'C0I.6'
        result = list(TopographyCodeRegex().annotate(f'Topo. code is ({exp_code})'))

        self.assertEqual(1, len(result))

        location, annotations = result[0]
        self.assertEqual((15, 20), location)

        self.assertEqual(1, len(annotations))
        self.assertEqual(exp_code, annotations[0]['$OCR_ERRORS1'])

    def test_annotate_format_error2(self):
        """Test to make sure we match codes that contain OCR errors."""
        exp_code = '(0I.6'
        result = list(TopographyCodeRegex().annotate(f'Topo. code is ({exp_code})'))

        self.assertEqual(1, len(result))

        location, annotations = result[0]
        self.assertEqual((15, 20), location)

        self.assertEqual(1, len(annotations))
        self.assertEqual(exp_code, annotations[0]['$OCR_ERRORS2'])

    def test_annotate_no_match(self):
        """Test to make sure we don't match text that looks like a code, but doesn't fall into the valid range."""
        result = TopographyCodeRegex().annotate('Topo. code is (C90.6)')

        self.assertEqual(0, len(result))

    def test_vectorize_expected_format(self):
        """Test to vectorize a match to codes in the expected format."""
        self.__test_vectorize([1, 1, 0], 'C00.6')

    def test_vectorize_format_error1(self):
        """Test to vectorize a match to codes that contain OCR errors."""
        self.__test_vectorize([0, 1, 0], 'C0I.6')

    def test_vectorize_format_error2(self):
        """Test to vectorize a match to codes that contain OCR errors."""
        self.__test_vectorize([0, 0, 1], '(0I.6')

    def __test_vectorize(self, expected: List[int], code: str):
        tcr = TopographyCodeRegex()

        text = f'code is ({code})'

        tokens = annotate_text(text, feature_types=[FeatureType.topography_code_regex])

        actual = tcr.vectorize(tokens)

        self.assertEqual(expected, actual[3])


class TestMorphologyCodeRegex(unittest.TestCase):
    def test_annotate_expected_format(self):
        """Test to make sure we match codes in the expected format."""
        exp_code = '8022/3'
        result = list(MorphologyCodeRegex().annotate(f'Pleomorphic carcinoma ({exp_code})'))

        self.assertEqual(1, len(result))

        location, annotations = result[0]
        self.assertEqual((23, 29), location)

        self.assertEqual(2, len(annotations))
        for annotation in annotations:
            self.assertEqual(1, len(annotation))
            self.assertEqual(exp_code, list(annotation.values())[0])

    def test_annotate_format_error(self):
        """Test to make sure we match codes that may contain OCR errors."""
        exp_code = '8I12/I'
        result = list(MorphologyCodeRegex().annotate(f'Pleomorphic carcinoma ({exp_code})'))

        self.assertEqual(1, len(result))

        location, annotations = result[0]
        self.assertEqual((23, 29), location)

        self.assertEqual(1, len(annotations))

        annotation = annotations[0]
        self.assertEqual(1, len(annotation))
        self.assertEqual(exp_code, list(annotation.values())[0])

    def test_annotate_no_match(self):
        """Test to make sure we don't match text that looks like a code, but doesn't fall into the valid range."""
        result = list(MorphologyCodeRegex().annotate(f'Pleomorphic carcinoma (7022/3)'))

        self.assertEqual(0, len(result))

    def test_vectorize_expected_format(self):
        """Test to vectorize a match to codes in the expected format."""
        self.__test_vectorize([1, 1], '8022/3')

    def test_vectorize_format_error(self):
        """Test to vectorize a match to codes that contain OCR errors."""
        self.__test_vectorize([0, 1], '8I12/I')

    def __test_vectorize(self, expected: List[int], code: str):
        mcr = MorphologyCodeRegex()

        text = f'Pleomorphic carcinoma ({code})'

        tokens = annotate_text(text, feature_types=[FeatureType.morphology_code_regex])
        actual = mcr.vectorize(tokens)

        self.assertEqual(expected, actual[3])


class TestTNMStaging(unittest.TestCase):
    # Material 1 (https://drive.google.com/drive/folders/1fHaQjNd09_Xz2C4TFgaZvCoh3NSUPE1v)
    # Material 2 / patho_reports (https://drive.google.com/drive/folders/19Q1bukq_3adnBbZ77cRe-w3UQ1qM2TLG)
    def test_annotate_breast1_actual(self):
        expected = [((0, 4), [{'$T_FULL': 'pT1c'}]),
                    ((10, 14), [{'$N': 'pN2a'}]),
                    ((23, 25), [{'$M': 'MX'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT1c (m), pN2a (7/25), MX, R0, G2 (L0, V0)')))

    def test_annotate_breast1_extracted(self):
        expected = [((0, 4), [{'$T_OCR_ERROR': 'pTic'}]),
                    ((9, 13), [{'$N': 'pN2a'}]),
                    ((22, 24), [{'$M': 'MX'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pTic(m), pN2a (7/25), MX, RO, G2 (LO, VO)')))

    def test_annotate_breast2_actual(self):
        expected = [((15, 18), [{'$T_FULL': 'pT3'}]),
                    ((25, 29), [{'$N': 'pN1a'}]),
                    ((38, 41), [{'$M': 'pMx'}])]

        self.assertListEqual(expected,
                             list(TNMStaging().annotate('M-8500/3, G 2, pT3, pL1, pN1a (1/13), pMx, stage III A. R0.')))

    def test_annotate_breast2_extracted(self):
        expected = [((15, 18), [{'$T_FULL': 'PT3'}]),
                    ((25, 29), [{'$N_OCR_ERROR': 'pNla'}]),
                    ((38, 41), [{'$M': 'pMx'}])]

        self.assertListEqual(expected,
                             list(TNMStaging().annotate('M-8500/3, G 2, PT3, PL1, pNla (1/13), pMx, stage III A. RO.')))

    def test_annotate_colon23_staging1_actual(self):
        expected = [((0, 3), [{'$T_FULL': 'pT3'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT3, R0; G2')))

    def test_annotate_colon23_staging2_actual(self):
        expected = [((0, 3), [{'$T_FULL': 'pT3'}]),
                    ((4, 7), [{'$N': 'pN0'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT3 pN0 (0/44) L0 V0 R0')))

    def test_annotate_colon23_staging1_extracted(self):
        expected = [((0, 3), [{'$T_FULL': 'pT3'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT3, RO; G2')))

    def test_annotate_colon23_staging2_extracted(self):
        expected = [((0, 3), [{'$T_FULL': 'pT3'}]),
                    ((4, 7), [{'$N_OCR_ERROR': 'pNO'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT3 pNO (0/44) LO VO RO')))

    def test_annotate_colon24_actual(self):
        expected = [((0, 3), [{'$T_FULL': 'pT2'}]),
                    ((4, 7), [{'$N': 'pN0'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT2 pN0 (1/12), L0, V0; G2,')))

    def test_annotate_colon24_extracted(self):
        expected = [((0, 3), [{'$T_FULL': 'pT2'}]),
                    ((4, 7), [{'$N_OCR_ERROR': 'PNO'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT2 PNO (1/12), LO, VO; G2,')))

    def test_annotate_lung68_actual(self):
        expected = [((0, 4), [{'$T_FULL': 'pT2a'}]),
                    ((6, 9), [{'$N': 'pN0'}]),
                    ((18, 21), [{'$M': 'pMx'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT2a, pN0 (0/23), pMx, G3')))

    def test_annotate_lung68_extracted(self):
        expected = [((0, 4), [{'$T_FULL': 'pT2a'}]),
                    ((6, 9), [{'$N_OCR_ERROR': 'PNO'}]),
                    ((18, 21), [{'$M': 'pMx'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT2a, PNO (0/23), pMx, G3')))

    def test_annotate_a6_actual(self):
        expected = [((0, 3), [{'$T_FULL': 'pT2'}]), ((4, 7), [{'$N': 'pNX'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT2 pNX')))

    def test_annotate_a30_actual(self):
        expected = [((0, 3), [{'$T_FULL': 'pT3'}]),
                    ((4, 7), [{'$N': 'pN0'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('pT3 pN0')))

    def test_annotate_a30_extracted(self):
        expected = [((0, 3), [{'$T_FULL': 'PT3'}]),
                    ((4, 7), [{'$N_OCR_ERROR': 'PNO'}])]

        self.assertListEqual(expected, list(TNMStaging().annotate('PT3 PNO')))

    def test_vectorize_complete_specification_no_errors(self):
        """Test to vectorize a perfect match to a fully specified staging code."""
        expected = [[0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        self.__test_vectorize(expected, 'pT1 pN0 M0 R0 G1 S0 L0 V0')

    def test_vectorize_complete_specification_all_errors(self):
        """Test to vectorize an imperfect match to a fully specified staging code."""
        expected = [[0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        self.__test_vectorize(expected, 'pTl pNO MO RO Gi SO LO VO')

    def test_vectorize_no_specification(self):
        """Test to vectorize text that does not containa a staging code."""
        self.__test_vectorize([[0, 0, 0, 0, 0, 0, 0, 0]] * 2, 'Not TNM.')

    def test_annotate_regression1(self):
        expected = [((13, 18), [{'$T_FULL': 'ypT4b'}])]

        self.assertListEqual(expected,
                             list(TNMStaging().annotate('Tumour stage ypT4b (but clinically, known metastatic disease)')))

    def __test_vectorize(self, expected: List[List[int]], code: str):
        tnm = TNMStaging()

        text = f'TNM staging: {code}'

        tokens = annotate_text(text, feature_types=[FeatureType.tnm_code])

        actual = tnm.vectorize(tokens)

        for i in range(3):
            self.assertFalse(i in actual)
        for j in range(len(expected)):
            if expected[j] != tnm.default_vector:
                self.assertListEqual(actual[j+3], expected[j])


class TestTumorGradeTerms(unittest.TestCase):
    def test_annotate_grade(self):
        expected = [((9, 18), [{'$GRADE': 'low grade'}]), ((9, 12), [{'$DEGREE': 'low'}])]

        self.assertListEqual(expected, list(TumorGradeTerms().annotate('likely a low grade adenocarcinoma')))

    def test_annotate_degree(self):
        expected = [((7, 10), [{'$DEGREE': 'low'}]),
                    ((14, 22), [{'$DEGREE': 'moderate'}]),
                    ((14, 35), [{'$DIFFERENTIATE': 'moderate differentiat'}])]

        self.assertListEqual(expected, list(TumorGradeTerms().annotate('Grade: low to moderate differentiation')))

    def test_annotate_diff(self):
        expected = [((9, 15), [{'$DEGREE': 'poorly'}]),
                    ((9, 28), [{'$DIFFERENTIATE': 'poorly differentiat'}])]

        self.assertListEqual(expected, list(TumorGradeTerms().annotate('Tumor is poorly differentiated')))

    def test_vectorize_grade(self):
        text = 'low grade carcinoma'

        feature = TumorGradeTerms()

        tokens = annotate_text(text, feature_types=[FeatureType.tumor_grade_terms])

        self.assertDictEqual({0: [1, 0, 1, 0], 1: [0, 0, 1, 0]}, feature.vectorize(tokens))

    def test_vectorize_degree(self):
        text = 'Grade: intermediate to high'

        tokens = annotate_text(text, feature_types=[FeatureType.tumor_grade_terms])

        self.assertDictEqual({2: [1, 0, 0, 0], 4: [1, 0, 0, 0]},
                             TumorGradeTerms().vectorize(tokens))

    def test_vectorize_diff(self):
        text = 'Tumor is poorly differentiated'

        feature = TumorGradeTerms()

        tokens = annotate_text(text, feature_types=[FeatureType.tumor_grade_terms])

        self.assertDictEqual({2: [1, 1, 0, 0], 3: [0, 1, 0, 0]}, feature.vectorize(tokens))


class TestTumorGradeCode(unittest.TestCase):
    def test_annotate_no_space_numeric(self):
        expected = [((14, 16), [{'$G': 'G1'}])]

        self.assertListEqual(expected, list(TumorGradeCode().annotate('pT1 pN0 M0 R0 G1 S0 L0 V0')))

    def test_annotate_with_space_roman(self):
        expected = [((14, 18), [{'$G': 'G IV'}])]

        self.assertListEqual(expected, list(TumorGradeCode().annotate('pT1 pN0 M0 R0 G IV S0 L0 V0')))

    def test_annotate_ocr_error_no_space(self):
        expected = [((14, 16), [{'$G_OCR_ERROR': 'Gi'}])]

        self.assertListEqual(expected, list(TumorGradeCode().annotate('pT1 pN0 M0 R0 Gi S0 L0 V0')))

    def test_annotate_ocr_error_with_space(self):
        expected = [((14, 17), [{'$G_OCR_ERROR': 'G l'}])]

        self.assertListEqual(expected, list(TumorGradeCode().annotate('pT1 pN0 M0 R0 G l S0 L0 V0')))

    def test_vectorize_no_space_numeric(self):
        text = 'R0 G1'

        feature = TumorGradeCode()

        tokens = annotate_text(text, feature_types=[FeatureType.tumor_grade_code])

        self.assertDictEqual({1: [1, 0]}, feature.vectorize(tokens))

    def test_vectorize_ocr_error_no_space(self):
        text = 'Gi R0'

        feature = TumorGradeCode()

        tokens = annotate_text(text, feature_types=[FeatureType.tumor_grade_code])

        self.assertDictEqual({0: [0, 1]}, feature.vectorize(tokens))


if __name__ == '__main__':
    unittest.main()
