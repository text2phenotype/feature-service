import unittest

from text2phenotype.ccda.section import Aspect
from text2phenotype.constants.features import FeatureType

from feature_service.aspect.chunker import Chunker
from feature_service.feature_set.feature_cache import FeatureCache


class TestAspectMedication(unittest.TestCase):
    def setUp(self) -> None:
        self.chunker = Chunker()

    def assertMed(self, section_text):
        actual = self.chunker.predict_aspect_emb_by_section_no_enforce(section_text)
        actual = actual[0][FeatureType.aspect.name]
        self.assertEqual(Aspect.medication.name, actual)

    def test_biomed_204_aspirin_medication(self):
        self.assertMed('Medication List')
        self.assertMed('MEDICATION LIST')
        self.assertMed('MEDICATION LIST:')
        self.assertMed('DISCHARGE MEDICATIONS')
        self.assertMed('MEDICATIONS')
        self.assertMed('Medication:')
        self.assertMed('Aspirin 50 mg')
        self.assertMed('Aspirin 50 mg twice')
        self.assertMed('Aspirin 50 mg twice daily')
        self.assertMed('Aspirin twice daily')
        self.assertMed('Aspirin daily')

    @unittest.skip('JIRA/BIOMED-276')
    def test_biomed_276_aspirin_allergy(self):
        self.assertMed('Aspirin')
        self.assertMed('Aspirin 50')
        self.assertMed('Aspirin 50mg')

    def test_sections_medication(self):
        aspect_map = FeatureCache().aspect_map()
        for section, curated in aspect_map.items():
            if curated == 'Aspect.medication':
                self.assertMed(section)
