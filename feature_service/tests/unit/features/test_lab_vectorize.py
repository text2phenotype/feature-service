import copy
import unittest

from feature_service.features.lab import LabLoinc, LabHepc, LabHepCLabWithAtttibutes, LabHepcBinary
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType


class LabVectorizeTests(unittest.TestCase):
    TEST_INPUT = MachineAnnotation(json_dict_input={
        "lab_loinc": {0: [{'Lab': [{'code': '41995-2', 'tui': ['T201'], 'tty': ['COMP'], 'codingScheme': 'LNC',
                                    'cui': 'C1624104', 'preferredText': 'Hemoglobin A1c'},
                                   {'code': '41995-2', 'tui': ['T201'], 'tty': ['COMP'],
                                    'codingScheme': 'LNC', 'cui': 'C1624104', 'preferredText': 'A1c'},
                                   {'code': '41995-2', 'tui': ['T201'], 'tty': ['COMP'],'codingScheme': 'LNC',
                                    'cui': 'C1624104', 'preferredText': 'HbA1c'},
                                   {'code': '55454-3', 'tui': ['T201'], 'tty': ['COMP'],'codingScheme': 'LNC',
                                    'cui': 'C2707530', 'preferredText': 'Hemoglobin A1c'}],
                           'polarity': 'positive', 'attributes': {'labValue': '10', 'labUnit': 'mg'}}],
                      1: [{'labValue': '10'}], 2: [{'labUnit': 'mg'}]},
        "lab_hepc": {0: [{'Lab': [{'code': '41995-2', 'tui': ['T201'], 'tty': ['COMP'], 'codingScheme': 'LNC',
                                   'cui': 'C1624104', 'preferredText': 'Hemoglobin A1c'},
                                  {'code': '41995-2', 'tui': ['T201'], 'tty': ['COMP'],'codingScheme': 'LNC',
                                   'cui': 'C1624104', 'preferredText': 'HbA1c'},
                                  {'code': '55454-3', 'tui': ['T201'], 'tty': ['COMP'],'codingScheme': 'LNC',
                                   'cui': 'C2707530', 'preferredText': 'Hemoglobin A1c'}],
                          'polarity': 'positive', 'attributes': {'labValue': '10', 'labUnit': 'mg'}}],
                     1: [{'labValue': '10'}], 2: [{'labUnit': 'mg'}],
                     3: [{'Lab': [{'code': '41995-2', 'tui': ['T201'], 'tty': ['COMP'], 'codingScheme': 'LNC',
                                   'cui': 'C1624104', 'preferredText': 'Hemoglobin A1c'}],
                          'attributes': {'labValue': [], 'labUnit': []}}]},
        "token": ['hemoglobin', '10', 'mg', 'hemoglobin']
    })

    def test_lab_hepc_vectorize_attributes(self):
        target = LabHepCLabWithAtttibutes()
        actual = target.vectorize(self.TEST_INPUT, feature_name=FeatureType.lab_hepc)
        self.assertEqual(actual[0], [1, 1])
        self.assertFalse(3 in actual)

    def test_lab_loinc_vectorize_no_token(self):
        """ Test LabLoinc with no valid token """

        target = LabLoinc()

        actual = target.vectorize(MachineAnnotation(json_dict_input={}))

        all_zeros = all(v == 0 for v in target.default_vector)

        total_length = len(target.vectorize_sab_vocab([])) + \
                       len(target.vectorize_tui_semtype([])) + \
                       len(target.vectorize_tty_termtype([]))

        total_length += 4

        # length should match and all values should be 0
        self.assertTrue(all_zeros)
        self.assertFalse(1 in actual)

    def test_lab_loinc_vectorize_positive_polarity(self):
        """ if positive polarity, first item should be 1 """

        target = LabLoinc()

        actual = target.vectorize(self.TEST_INPUT)[0]

        # the first and 2nd item should be 1
        self.assertEqual(actual[0], 1)
        self.assertEqual(actual[1], 1)

    def test_lab_loinc_vectorize_lab_value_polarity(self):
        """ if positive polarity, first item should be 1 """

        target = LabLoinc()

        actual = target.vectorize(self.TEST_INPUT)[0]

        self.assertEqual(actual[0], 1)

    def test_lab_loinc_vectorize_validate_vocab_index(self):
        """ Test to see if the corresponding flag was set for LNC """

        target = LabLoinc()

        # find the index for LNC
        target_sab_vocab_vector = target.vectorize_sab_vocab(["LNC"])
        index = target_sab_vocab_vector.index(1)

        actual = target.vectorize(self.TEST_INPUT)[0]

        # the correct index should be set
        self.assertEqual(actual[4 + index], 1)

    def test_lab_hepc_vectorize_no_token(self):
        """ Test LabHepc with no valid token """
        target = LabHepc()

        actual = target.vectorize(MachineAnnotation(json_dict_input={}))

        all_zeros = all(v == 0 for v in target.default_vector)

        total_length = len(target.vectorize_sab_vocab([])) + \
                       len(target.vectorize_tui_semtype([])) + \
                       len(target.vectorize_tty_termtype([]))

        total_length += 4

        # length should match and all values should be 0
        self.assertTrue(all_zeros)
        self.assertFalse(1 in actual)

    def test_lab_hepc_vectorize_positive_polarity(self):
        """ if positive polarity, first item should be 1 """

        target = LabHepc()

        actual = target.vectorize(self.TEST_INPUT)[0]

        # the first and 2nd item should be 1
        self.assertEqual(actual[0], 1)
        self.assertEqual(actual[1], 1)

    def test_lab_hepc_vectorize_lab_value_polarity(self):
        """ if positive polarity, first item should be 1 """

        target = LabHepc()

        actual = target.vectorize(self.TEST_INPUT)
        expected = {0: [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                    1: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    2: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    3: [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]}

        self.assertDictEqual(actual, expected)

    def test_lab_hepc_vectorize_validate_vocab_index(self):
        """ Test to see if the corresponding flag was set for LNC """

        target = LabHepc()

        # find the index for LNC
        target_sab_vocab_vector = target.vectorize_sab_vocab(["LNC"])
        index = target_sab_vocab_vector.index(1)

        actual = target.vectorize(self.TEST_INPUT)[0]

        # the correct index should be set
        self.assertEqual(actual[4 + index], 1)

    def test_vectorize_with_positive_lab(self):
        input_token = copy.deepcopy(self.TEST_INPUT)
        input_token.add_item("lab_hepc_binary", input_token["lab_hepc"])

        actual = LabHepcBinary().vectorize(input_token)[0]

        self.assertListEqual([1, 1], actual)

    def test_vectorize_with_negative_lab(self):
        test_input = MachineAnnotation(json_dict_input={
            "lab_hepc": {0: [{'Lab': [{'code': '41995-2', 'tui': ['T201'], 'tty': ['COMP'], 'codingScheme': 'LNC'}],
                              'polarity': 'negative'},
                             {'labValue': ''},
                             {'labUnit': ''}
                             ]},
            "token": ['hemoglobin', 'abs']
        })

        actual = LabHepcBinary().vectorize(test_input)[0]

        self.assertListEqual([1, 0], actual)

    def test_vectorize_no_lab(self):
        test_input = MachineAnnotation(json_dict_input={
            "lab_loinc": {0: []},
            "lab_hepc": {0: []},
            "token": ['n/a']
        })

        actual = LabHepcBinary().vectorize(test_input)

        self.assertDictEqual({}, actual)
