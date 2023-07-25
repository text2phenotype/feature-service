import unittest

from feature_service.features.medgen import ClinicalMedgen, MedgenGene
from feature_service.tests.integration.features.test_clinical import TestClincalBase


class TestClinicalMedgen(TestClincalBase):
    def test_annotate(self):
        """Test annotating text using the MEDGEN clinical pipeline."""
        self._annotate(ClinicalMedgen())


class TestMedgenGene(unittest.TestCase):
    def test_annotate(self):
        response = MedgenGene().annotate("""Tumor is EGFR+.""")

        self.assertEqual(1, len(response))

        span, concept = response[0]
        self.assertTupleEqual((9, 13), span)
        self.assertEqual('positive', concept[0]['polarity'])


if __name__ == '__main__':
    unittest.main()
