import unittest
import shutil

from text2phenotype.common.log import operations_logger

from feature_service.nlp import nlp_cache
from feature_service.feature_service_env import FeatureServiceEnv


class TestNLPCacheDisable(unittest.TestCase):

    def test_biomed_296_disable_cache(self):

        temp_dir = "BIOMED-296"

        FeatureServiceEnv.NLP_CACHE.value = temp_dir
        FeatureServiceEnv.NLP_CACHE_ENABLE.value = True

        self.assertTrue(nlp_cache.get_cache_dir() is not None)
        self.assertTrue(FeatureServiceEnv.NLP_CACHE_ENABLE.value)

        nlp_cache.init_cache_dir()

        self.assertTrue(FeatureServiceEnv.NLP_CACHE_ENABLE.value)

        nlp_cache.save_text('doctor wrote this note')

        self.assertTrue(FeatureServiceEnv.NLP_CACHE_ENABLE.value)

        try:
            shutil.rmtree(temp_dir)
        except OSError:
            operations_logger.exception(exc_info=True)

        FeatureServiceEnv.NLP_CACHE_ENABLE.value = False
        self.assertFalse(FeatureServiceEnv.NLP_CACHE_ENABLE.value)
