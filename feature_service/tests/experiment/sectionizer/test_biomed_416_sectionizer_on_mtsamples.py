import os
import json
import unittest

from feature_service.features.sectionizer import Sectionizer
from feature_service.feature_service_env import FeatureServiceEnv


class TestBiomed416MTSamples(unittest.TestCase):

    def test_sectionizer(self):

        mtsamples_clean_dir = os.path.join(FeatureServiceEnv.TEXT2PHENOTYPE_SAMPLES_PATH.value, 'mtsamples', 'clean')
        golden_standart_dir = os.path.join(os.getcwd(), os.path.dirname(__file__), 'mtsamples_clean_sectionized')

        for fname in os.listdir(golden_standart_dir):
            with open(os.path.join(golden_standart_dir, fname), 'r') as expected_f:
                expected = json.load(expected_f)

            with open(os.path.join(mtsamples_clean_dir, fname[:-4] + 'txt'), "r") as sample_f:
                matches = Sectionizer().match_sectionizer(sample_f.read())

            self.assertCountEqual(matches,
                                  expected,
                                  msg=f'problem with {fname} ex:{len(expected)} match: {len(matches)}')
