import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.vectorization import vectorize_from_annotations
from feature_service.features import Case


class CaseVectorizeTests(unittest.TestCase):
    INPUT_TOKEN = MachineAnnotation(json_dict_input={'token': ['UPPER', 'lower', 'Title', 'aiYjnfsdTY9']})

    def test_case_vectorize(self):
        target = Case()
        actual = target.vectorize(self.INPUT_TOKEN)

        self.assertListEqual([1, 0, 0], actual[0])
        self.assertListEqual([0, 1, 0], actual[1])
        self.assertListEqual([0, 0, 1], actual[2])
        self.assertFalse(3 in actual)

    def test_vectorization_case(self):
        actual = vectorize_from_annotations(self.INPUT_TOKEN, feature_types=[FeatureType.case])[FeatureType.case.name]

        self.assertListEqual([1, 0, 0], actual[0])
        self.assertListEqual([0, 1, 0], actual[1])
        self.assertListEqual([0, 0, 1], actual[2])
        self.assertFalse(3 in actual.input_dict)
