import unittest

from feature_service.features.clinical import Clinical
from feature_service.features.cancer import (Topography, TopographyCode, Morphology, MorphologyCode)


class TestBiomed1009_ICDO(unittest.TestCase):
    def _test_annotate(self, annotator: Clinical, text: str, exp_code: str, concept_key: str):
        results = annotator.annotate(text)

        found_match = False
        for _, annotations in results:
            for annotation in annotations:
                for concept in annotation[concept_key]:
                    if concept['preferredText'] == exp_code:
                        found_match = True

                        break

                if found_match:
                    break

            if found_match:
                break

        self.assertTrue(found_match)


class TestTopography(TestBiomed1009_ICDO):
    def test_annotate(self):
        self._test_annotate(Topography(), 'Commissure of lip', 'C00.6', 'AnatomicalSite')


class TestTopographyCode(TestBiomed1009_ICDO):
    def test_annotate(self):
        exp_code = 'C00.6'

        self._test_annotate(TopographyCode(), f'Topo. code is ({exp_code})', exp_code, 'AnatomicalSite')


class TestMorphology(TestBiomed1009_ICDO):
    def test_annotate(self):
        self._test_annotate(Morphology(), 'Pleomorphic carcinoma', '8022/3', 'DiseaseDisorder')


class TestMorphologyCode(TestBiomed1009_ICDO):
    def test_annotate(self):
        exp_code = '8022/3'

        self._test_annotate(MorphologyCode(), f'Morph. code is {exp_code}', exp_code, 'DiseaseDisorder')


if __name__ == '__main__':
    unittest.main()
