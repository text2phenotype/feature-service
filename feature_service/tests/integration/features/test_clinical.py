import abc
import unittest

from feature_service.feature_set.annotation import annotate_text
from feature_service.features.clinical import *

from text2phenotype.constants.features import FeatureType


class TestClincalBase(unittest.TestCase):
    def _annotate(self, clinical: Clinical):
        response = clinical.annotate("""6yo female pt arrived at ER with headache, nausea and vomiting.
    Temp: 101.5
    Ht: 3'8\"
    Wt: 44lbs""")

        # just make sure something came back
        # avoiding hard coding expected values so this isn't contingent on cTAKES, dictionaries, etc.
        self.assertGreater(len(response), 0)

        last_start = -1
        for hit in response:
            # make sure they are sorted
            start = hit[0][0]
            self.assertGreaterEqual(start, last_start)
            last_start = start

            for type_dict in hit[1]:
                has_polarity = False
                has_concepts = False
                for sem_type, concepts in type_dict.items():
                    if sem_type == 'polarity' and concepts:
                        has_polarity = True
                    elif len(concepts):
                        has_concepts = True

                self.assertTrue(has_polarity)
                self.assertTrue(has_concepts)


class TestClinical(TestClincalBase):
    def test_annotate(self):
        """Test annotating text using the default clinical pipeline."""
        self._annotate(Clinical())


class TestClinicalSnomed(TestClincalBase):
    def test_annotate(self):
        """Test annotating text using the SNOMED clinical pipeline."""
        self._annotate(ClinicalSnomed())


class TestClinicalGeneral(TestClincalBase):
    def test_annotate(self):
        """Test annotating text using the general clinical pipeline."""
        self._annotate(ClinicalGeneral())


class __TestClinicalCode(TestClincalBase, abc.ABC):

    def _test_annotate(self, text: str, exp_code: str):
        response = self._get_clincal().annotate(text)

        self.assertGreater(len(response), 0)

        matched_code = False
        for hit in response:
            for type_dict in hit[1]:
                for sem_type, concepts in type_dict.items():
                    if sem_type == 'polarity':
                        continue

                    for concept in concepts:
                        self.assertTrue(exp_code.startswith(concept['code']))

                        if concept['code'] == exp_code:
                            matched_code = True

        self.assertTrue(matched_code)

    def _test_regression_biomed_935(self):
        response = self._get_clincal().annotate('1/2/2019')

        self.assertEqual(0, len(response))

    @abc.abstractmethod
    def _get_clincal(self) -> Clinical:
        pass


class TestICD10ClinicalCode(__TestClinicalCode):
    def test_annotate(self):
        icd10 = 'J70.2'

        self._test_annotate(f"Patient found to have acute drug-induced interstitial lung disorder ({icd10})", icd10)

    def test_regression_biomed_935(self):
        self._test_regression_biomed_935()

    def _get_clincal(self) -> Clinical:
        return ICD10ClinicalCode()


class TestICD9ClinicalCode(__TestClinicalCode):
    def test_annotate(self):
        icd9 = '006.2'

        self._test_annotate(f"Patient found to have amebic nondysenteric colitis ({icd9})", icd9)

    def test_regression_biomed_935(self):
        self._test_regression_biomed_935()

    def _get_clincal(self) -> Clinical:
        return ICD9ClinicalCode()

class TestPartialTypes(unittest.TestCase):
    text = "Patient has alzheimers and leukemia stage 3"

    annotation = annotate_text(
        text, {FeatureType.clinical_medgen,  FeatureType.clinical,  FeatureType.clinical_snomed_sem_type, FeatureType.clinical_general})

    def assert_right_len(self, target: Feature):
        vector = target().vectorize(self.annotation, feature_name=target.annotated_feature)
        self.assertEqual(len(list(vector.values())[0]), target.vector_length, target.feature_type.name)
        self.assertGreaterEqual(sum(list(vector.values())[0]), 0, target.feature_type.name)

    def test_right_len_vectorize(self):
        self.assert_right_len(ClinicalMedGenVocab)
        self.assert_right_len(ClinicalSnomedVocab)
        self.assert_right_len(ClinicalVocab)


        self.assert_right_len(ClinicalTty)
        self.assert_right_len(ClinicalSnomedTTY)
        self.assert_right_len(ClinicalMedGenTTY)

        self.assert_right_len(ClinicalSnomedTui)
        self.assert_right_len(ClinicalMedGenTui)
        self.assert_right_len(ClinicalTui)

        self.assert_right_len(ClinicalSnomedSemType)
        self.assert_right_len(ClinicalMedGenSemType)
        self.assert_right_len(ClinicalSemType)



