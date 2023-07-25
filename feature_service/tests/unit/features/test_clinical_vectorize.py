import copy
import unittest

from feature_service.constants import SemTypeCtakesAsserted
from feature_service.features import Clinical, ClinicalBinary
from text2phenotype.common.featureset_annotations import MachineAnnotation


class ClinicalVectorizeTests(unittest.TestCase):
    TEST_INPUT = MachineAnnotation(json_dict_input={"clinical": {"0": [
        {
            "SignSymptom": [{
                "code": "184099003",
                "cui": "C0421451",
                "tui": "T033",
                "preferredText": "Patient date of birth",
                "codingScheme": "SNOMEDCT_US"},
                {
                    "code": "TCGA",
                    "cui": "C0421451",
                    "tui": "T033",
                    "preferredText": "Patient date of birth",
                    "codingScheme": "NCI"},
                {
                    "code": "MTHU009540",
                    "cui": "C0421451",
                    "tui": "T033",
                    "preferredText": "Patient date of birth",
                    "codingScheme": "LNC"}],
            "polarity": "positive"}]}, "token": ['DOB', 'abc']})

    def test_clinical_vectorize_invalid_token(self):
        """ Validate total vector length and all zeros """

        target = Clinical()
        actual = target.vectorize(self.TEST_INPUT)

        total_length = len(target.vectorize_sab_vocab([])) + \
                       len(target.vectorize_tui_semtype([])) + \
                       len(target.vectorize_tty_termtype([]))

        total_length += 3 + len(SemTypeCtakesAsserted.__members__)

        # length should match and all values should be 0
        self.assertFalse(1 in actual)

    def test_clinical_vectorize_positive_polarity(self):
        """ if positive polarity, first item should be 1 """

        target = Clinical()

        actual = target.vectorize(self.TEST_INPUT)

        # the first item should be 1
        self.assertEqual(actual[0][0], 1)

    def test_clinical_vectorize_sem_type_index_valid(self):
        target = Clinical()

        actual = target.vectorize(self.TEST_INPUT)

        # the SignSymptom index should be set to 1
        self.assertEqual(actual[0][3 + SemTypeCtakesAsserted.SignSymptom.value], 1)

    def test_clinical_vectorize_validate_vocabs(self):
        """ Test to see if the count_vocabs > 1 which means the 2nd item will be set"""

        target = Clinical()

        actual = target.vectorize(self.TEST_INPUT)

        # the 2nd index should be set to 1
        self.assertEqual(actual[0][1], 1)

    def test_clinical_vectorize_validate_concepts(self):
        """ Test to see if the count_concepts > 2 which means the 3rd item will be set """

        target = Clinical()

        actual = target.vectorize(self.TEST_INPUT)[0]

        # the 2nd index should be set to 1
        self.assertEqual(actual[2], 1)

    def test_clinical_vectorize_validate_vocab_index(self):
        """ Test to see if the corresponding flag was set for SNOMEDCT_US """

        target = Clinical()

        # find the index for SNOMEDCT_US
        target_sab_vocab_vector = target.vectorize_sab_vocab(["SNOMEDCT_US"])
        index = target_sab_vocab_vector.index(1)

        actual = target.vectorize(self.TEST_INPUT)

        # the correct index should be set
        self.assertEqual(actual[0][3 + len(SemTypeCtakesAsserted.__members__) + index], 1)

    def test_vectorize_binary_positive_match(self):
        input_token = copy.deepcopy(self.TEST_INPUT)
        input_token.add_item("clinical_binary", input_token["clinical"])

        actual = ClinicalBinary().vectorize(input_token)

        self.assertListEqual([1, 1], actual[0])

    def test_vectorize_binary_negative_match(self):
        input_token = copy.deepcopy(self.TEST_INPUT)
        input_token.add_item("clinical_binary", input_token["clinical"])
        input_token["clinical_binary"]["0"][0]["polarity"] = "negative"

        actual = ClinicalBinary().vectorize(input_token)[0]

        self.assertListEqual([1, 0], actual)

    def test_vectorize_binary_no_match(self):
        input_token = MachineAnnotation(json_dict_input={"clinical": {"0": []}, "token": ['DOB', 'abc']})

        actual = ClinicalBinary().vectorize(input_token)

        self.assertDictEqual({}, actual)
