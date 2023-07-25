import os
import unittest

from text2phenotype.common import common
from text2phenotype.constants.features import FeatureType

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.feature_set.annotation import annotate_text
from feature_service.features.form import Form


class TestBiomed633HepC(unittest.TestCase):
    SAMPLE_DIR = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'himss', 'Ricardo_Campos_Regression')

    def test_annotate_text_form_values_present(self):
        for sample_file in common.get_file_list(self.SAMPLE_DIR, '.txt'):
            sample_text = common.read_text(sample_file)

            annotations = annotate_text(sample_text, [FeatureType.form])
            # make sure we see form values
            for annot in annotations.to_json():
                if annot.get('form'):
                    break
            else:
                self.assertTrue(False, sample_file)

    def test_annotate(self):
        ff = Form()
        for sample_file in common.get_file_list(self.SAMPLE_DIR, '.txt'):
            sample_text = common.read_text(sample_file)

            annotations = ff.annotate(sample_text)
            for annot in annotations:
                indices = annot[0]
                evidence_list = annot[1]

                exp_text = sample_text[indices[0]:indices[1]]
                for evidence in evidence_list:
                    self.assertIn(exp_text, evidence)


if __name__ == '__main__':
    unittest.main()
