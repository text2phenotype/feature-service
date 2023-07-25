import unittest

from text2phenotype.ccda.section import Aspect as AspectEnum
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.features import (
    Aspect,
    AspectEnforce,
    AspectLine,
)


class AspectVectorizeTests(unittest.TestCase):
    INPUT_TOKEN = MachineAnnotation(json_dict_input={FeatureType.aspect.name: {'0': ['diagnosis']},
                   FeatureType.aspect_enforce.name:  {'0': ['diagnosis']},
                   FeatureType.aspect_line.name:  {'0': ['diagnosis']},
                   'token': ['Diagnosis']
                   })

    def test_aspect_vectorize(self):
        expect = [0] * len(AspectEnum.__members__)
        expect[AspectEnum.diagnosis.value] = 1
        target = Aspect()
        actual = target.vectorize(self.INPUT_TOKEN)

        self.assertListEqual(expect, actual[0])

    def test_aspect_line_vectorize(self):
        expect = [0] * len(AspectEnum.__members__)
        expect[AspectEnum.diagnosis.value] = 1

        target = AspectLine()
        actual = target.vectorize(self.INPUT_TOKEN)

        self.assertListEqual(expect, actual[0])

    def test_aspect_line_with_enforcement(self):

        expect = [0] * len(AspectEnum.__members__)
        expect[AspectEnum.diagnosis.value] = 1

        target = AspectEnforce()
        actual = target.vectorize(self.INPUT_TOKEN)

        self.assertListEqual(expect, actual[0])
