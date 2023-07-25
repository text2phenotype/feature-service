import unittest

from feature_service.features import ZipCode
from text2phenotype.common.featureset_annotations import MachineAnnotation


class ZipcodeVectorizeTests(unittest.TestCase):

    def test_zipcode_vectorize_vector_length(self):
        """ Test Zipcode vector length """

        input_token = MachineAnnotation(json_dict_input={'zipcode': {'0':  [{'city': 'PALO ALTO', 'state': 'CA', 'country': 'US'}]}, 'token':[0]})
        target = ZipCode()

        actual = target.vectorize(input_token)[0]

        # verify length
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0], 1)

    def test_zipcode_vectorize_invalid_token(self):
        """ Test Zipcode invalid token """

        input_token = MachineAnnotation()

        target = ZipCode()

        actual = target.vectorize(input_token)

        self.assertFalse(0 in actual)
