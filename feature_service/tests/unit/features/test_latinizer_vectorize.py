import unittest

from feature_service.features.latinizer import Latinizer, LatinizerBinary
from text2phenotype.common.featureset_annotations import MachineAnnotation


class TestLatinizerVectorize(unittest.TestCase):

    def test_latinizer_vectorize_procedure(self):
        test_token = MachineAnnotation(json_dict_input={'token': ['apendiscitis']})
        actual = Latinizer().vectorize(test_token, feature_name='token')[0]

        self.assertEqual(actual[1], 1)
        self.assertEqual(actual[4], 1)

    def test_latinizer_vectorize_random_word(self):
        test_token = MachineAnnotation(json_dict_input={'token': ['playground']})
        actual = Latinizer().vectorize(test_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_latinizer_default_vector(self):
        actual = Latinizer().default_vector

        self.assertEqual(len(actual), 10)
        self.assertEqual(sum(actual), 0)

    def test_latinizer_prefix(self):
        test_token = MachineAnnotation(json_dict_input={'token': ['ectotable']})
        actual = Latinizer().vectorize(test_token, feature_name='token')[0]

        self.assertEqual(actual[0], 1)
        self.assertEqual(actual[7], 1)

    def test_vectorize_binary_with_matches(self):
        test_token = MachineAnnotation(json_dict_input={'token': ['apendiscitis']})

        actual = LatinizerBinary().vectorize(test_token, feature_name='token')[0]

        self.assertListEqual(actual, [1])

    def test_vectorize_binary_no_matches(self):
        test_token = MachineAnnotation(json_dict_input={'token': ['playground']})

        actual = LatinizerBinary().vectorize(test_token, feature_name='token')

        self.assertDictEqual({}, actual)
