import unittest

from text2phenotype.ccda.section import Aspect
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.features import HeaderAspect


class HeaderAspectVectorizeTests(unittest.TestCase):
    def test_header_vectorize_no_token(self):
        """ Test Header with no valid token """

        input_token = MachineAnnotation(json_dict_input={'token': ['123']})

        target = HeaderAspect()

        actual = target.vectorize(input_token)

        # we should have all zeros and the length of Aspect enum
        self.assertEqual(len(target.default_vector), len(Aspect.__members__))
        self.assertFalse(0 in actual)

    def test_header_vectorize_with_token(self):
        """ Test Header with valid token """

        input_token = MachineAnnotation(json_dict_input={"header": {'0': [{"DISCHARGE DIAGNOSES": "Aspect.diagnosis"}]}, 'token': 'Diagnosis'})

        target = HeaderAspect()

        actual = target.vectorize(input_token, feature_name='header')[0]

        # Aspect encounter (8) should be flagged
        self.assertEqual(actual[Aspect.diagnosis.value], 1)

