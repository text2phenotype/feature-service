import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.features import Person


class PersonVectorizeTests(unittest.TestCase):

    def test_person_vectorize_vector_length(self):
        input_token = MachineAnnotation(json_dict_input={'person': {'0': ['Bob']}, 'token': ['Bob']})

        target = Person()

        actual = target.vectorize(input_token)

        self.assertEqual(len(actual), 1)  # should only be 1 length
        self.assertEqual(actual[0], [1])  # 1st item should be zero

    def test_person_vectorize_invalid_token(self):
        """ Test Person vectorize with invalid token"""

        input_token = MachineAnnotation(json_dict_input={'token': ['123']})

        target = Person()

        actual = target.vectorize(input_token)

        self.assertFalse(0 in actual)
