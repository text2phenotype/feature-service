import unittest
import os

from text2phenotype.common import common
from text2phenotype.common.log import operations_logger

from feature_service.nlp import nlp_cache
from feature_service.feature_service_env import FeatureServiceEnv


class TestBiomed202(unittest.TestCase):

    def test_nlp_cache_openemr_features_for_summary(self):
        open_emr_dir = os.path.join(FeatureServiceEnv.TEXT2PHENOTYPE_SAMPLES_PATH.value, 'emr', 'OpenEMR')

        for f in common.get_file_list(open_emr_dir, 'txt'):
            operations_logger.debug(f)

            text = common.read_text(f)

            nlp_cache.hash_dir(text)
            nlp_cache.save_text(text)

            nlp_cache.clinical(text)
            nlp_cache.hepc_clinical(text)
            nlp_cache.lab_value(text)
            nlp_cache.hepc_lab_value(text)
            nlp_cache.drug_ner(text)
            nlp_cache.hepc_drug_ner(text)
            nlp_cache.smoking(text)
            nlp_cache.temporal(text)
