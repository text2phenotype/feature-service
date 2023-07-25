import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.features import Header


class HeaderVectorizeTests(unittest.TestCase):

    def test_header_vectorize_no_token(self):
        """ Test Header with no valid token """

        input_token = MachineAnnotation(json_dict_input={'token': '123'})

        target = Header()

        actual = target.vectorize(input_token)

        self.assertFalse(0 in actual)

    def test_header_vectorize_valid_token(self):
        """ Test Header with a valid token """

        input_token = MachineAnnotation(json_dict_input={'header': {'0': ['My Header']}, 'token': ['a']})

        target = Header()

        actual = target.vectorize(input_token)[0]

        self.assertEqual(actual[0], 1)


