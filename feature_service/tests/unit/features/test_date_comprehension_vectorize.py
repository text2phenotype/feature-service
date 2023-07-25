import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.features import DateComprehension


class DateComprehensionVectorizeTests(unittest.TestCase):
    INPUT_TOKEN = MachineAnnotation(json_dict_input={"date_comprehension": {'0':[{
            "first": True,
            "last": False
        }]}, "token": [2001]})

    def test_date_comprehension_vectorize_valid_token(self):
        """ date comprehension present """
        target = DateComprehension()

        actual = target.vectorize(self.INPUT_TOKEN)
        # the first item should be 1
        self.assertEqual(actual[0][0], 1)

    def test_date_comprehension_vectorize_invalid_token(self):
        """ date comprehension not present """

        test_input = MachineAnnotation(json_dict_input={"token": ['abc']})

        target = DateComprehension()

        actual = target.vectorize(test_input)

        self.assertFalse(0 in actual)

    def test_date_comprehension_vectorize_time_since_first_date_0(self):
        """ date comprehension present """

        target = DateComprehension()

        actual = target.vectorize(self.INPUT_TOKEN)

        # the 2nd item should be 1
        self.assertEqual(actual[0][1], 1)
