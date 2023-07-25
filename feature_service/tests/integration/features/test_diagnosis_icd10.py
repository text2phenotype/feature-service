import unittest

from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features.feature_type import FeatureType

from feature_service.feature_set.annotation import annotate_text

class TestDiagnosisICD10(unittest.TestCase):
    text = "Diabetes Mellitus Non Insulin Dependent"

    def test_coded_response(self):
        annot = annotate_text(text=self.text, feature_types={FeatureType.icd10_diagnosis})
        for idx in annot[FeatureType.icd10_diagnosis].token_indexes:
            for entry in annot[FeatureType.icd10_diagnosis][idx]:
                self.assertIn('ICD10',  entry['DiseaseDisorder'][0]['codingScheme'], entry)

