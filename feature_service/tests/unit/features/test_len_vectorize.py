import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.features import Len


class LenVectorizeTests(unittest.TestCase):

    def test_len_vectorize_low(self):
        """ Test Len vectorize with low value"""

        input_token = MachineAnnotation(json_dict_input={'token': ['the', 'then', 'dinosaursin']})

        target = Len()

        actual = target.vectorize(input_token)

        self.assertListEqual(actual[0], [1, 0, 0])  # low
        self.assertListEqual(actual[1], [0, 1, 0]) # medium
        self.assertListEqual(actual[2], [0, 0, 1]) # high
