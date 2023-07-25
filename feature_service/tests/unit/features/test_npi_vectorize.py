import copy
import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation

from feature_service.features.npi import NPI, NPIBinary


class NpiVectorizeTests(unittest.TestCase):
    TEST_INPUT = MachineAnnotation(json_dict_input={'token': ['allan', 'b', 'c', 'd', 'e'],
                  'npi': {'0': [{'Provider': {'count': 3, 'codes': [1306921168, 1497864433, 1508822834]}}],
                          '1': [{'Facility': {'count': 3, 'codes': [1306921168, 1497864433, 1508822834]}}],
                          '2': [{'phone': {'count': 3, 'codes': [1306921168, 1497864433, 1508822834]}}],
                          '3': [{'street': {'count': 3, 'codes': [1306921168, 1497864433, 1508822834]}}],
                          '4': [{'fax': {'count': 3, 'codes': [1306921168, 1497864433, 1508822834]}}]}})

    def test_npi_vectorize_length(self):
        target = NPI()
        actual = target.vectorize(self.TEST_INPUT)

        self.assertEqual(len(actual[0]), 10)
        self.assertEqual(actual[0][0], 1)
        self.assertEqual(actual[3][2], 1) # street
        self.assertEqual(actual[1][1], 1) #facility
        self.assertEqual(actual[2][3], 1) # phone
        self.assertEqual(actual[4][4], 1) #fax

    def test_provider_street_overlap_vectorize(self):
        input_token = MachineAnnotation(json_dict_input={'npi': {'0': [{'Provider': {'count': 3, 'codes': [1306921168, 1497864433, 1508822834], 'street': [1497864433]}}]}, 'token': ['a']})
        target = NPI()
        actual = target.vectorize(input_token)[0]

        self.assertEqual(actual[0], 1)
        self.assertEqual(actual[7], 1)

    def test_vectorize_binary_with_match(self):
        input_token = copy.deepcopy(self.TEST_INPUT)
        input_token.add_item("npi_binary", input_token["npi"])

        actual = NPIBinary().vectorize(input_token)[0]

        self.assertListEqual([1], actual)

    def test_vectorize_binary_no_match(self):
        input_token = MachineAnnotation(json_dict_input={'npi_binary': {'0': []}, 'token': ['a']})

        actual = NPIBinary().vectorize(input_token)

        self.assertDictEqual({}, actual)
