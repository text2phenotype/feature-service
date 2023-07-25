import copy
import unittest

from feature_service.features import DrugRXNorm, DrugRXNormBinary
from text2phenotype.common.featureset_annotations import MachineAnnotation


class DrugRxNormVectorizeTests(unittest.TestCase):
    TEST_INPUT = MachineAnnotation(json_dict_input={"drug_rxnorm": {'0':  [
        {'Medication': [{'code': '1191', 'tui': 'T109', 'tty': 'SY', 'codingScheme': 'RXNORM', 'cui': 'C0004057', 'preferredText': 'Aspirin'},
                        {'code': '1191', 'tui': 'T109', 'tty': 'IN', 'codingScheme': 'RXNORM', 'cui': 'C0004057', 'preferredText': 'Aspirin'},
                        {'code': '1191', 'tui': 'T121', 'tty': 'SY', 'codingScheme': 'RXNORM', 'cui': 'C0004057', 'preferredText': 'Aspirin'},
                        {'code': '1191', 'tui': 'T121', 'tty': 'IN', 'codingScheme': 'RXNORM', 'cui': 'C0004057', 'preferredText': 'Aspirin'}],
         'attributes': {'polarity': 'positive', 'medStrengthNum': [], 'medStrengthUnit': [], 'medFrequencyUnit': [],
                        'medFrequencyNum': []}}],
         1: [{'medUnit': ['mg']}]},
        'token': ['aspirin', 'mg']})

    def test_drug_rxnorm_vectorize_length(self):
        """ Validate total vector length """

        target = DrugRXNorm()

        actual = target.vectorize(self.TEST_INPUT)

        expected_total_length = 6
        expected_total_length += len(target.vectorize_sab_vocab([])) + \
                                 len(target.vectorize_tui_semtype([])) + \
                                 len(target.vectorize_tty_termtype([]))

        # length should match
        self.assertEqual(len(actual[0]), expected_total_length)

    def test_drug_rxnorm_vectorize_polarity_flag_set(self):
        """ Validate polarity flag """

        target = DrugRXNorm()

        actual = target.vectorize(self.TEST_INPUT)

        # dosage should have 4th index flag set to true
        self.assertEqual(actual[0][0], 1)

    def test_drug_rxnorm_vectorize_medunit_flag_set(self):
        """ Validate medUnit flag """

        target = DrugRXNorm()

        actual = target.vectorize(self.TEST_INPUT)

        # medUnit should have 5th index flag set to true
        self.assertEqual(actual[1][5], 1)

    def test_drug_rxnorm_vectorize_validate_vocab_index(self):
        """ Test to see if the corresponding flag was set for RXNORM """

        target = DrugRXNorm()

        # find the index for RXNORM
        target_sab_vocab_vector = target.vectorize_sab_vocab(["RXNORM"])
        index = target_sab_vocab_vector.index(1)

        actual = target.vectorize(self.TEST_INPUT)

        # the correct index should be set
        self.assertEqual(actual[0][6 + index], 1)

    def test_vectorize_binary_with_positive_drug_mention(self):
        input_token = copy.deepcopy(self.TEST_INPUT)
        input_token.add_item("drug_rxnorm_binary", input_token["drug_rxnorm"])

        actual = DrugRXNormBinary().vectorize(input_token)[0]

        self.assertListEqual([1, 1], actual)

    def test_vectorize_binary_with_negative_drug_mention(self):
        test_input = copy.deepcopy(self.TEST_INPUT)
        test_input.add_item("drug_rxnorm_binary", test_input["drug_rxnorm"])
        test_input['drug_rxnorm_binary']['0'][0]['attributes']['polarity'] = 'negative'

        actual = DrugRXNormBinary().vectorize(test_input)[0]

        self.assertListEqual([1, 0], actual)

    def test_vectorize_binary_no_drug_mentions(self):
        test_input = MachineAnnotation(json_dict_input={'token': ['n/a']})

        self.assertDictEqual({}, DrugRXNormBinary().vectorize(test_input))
