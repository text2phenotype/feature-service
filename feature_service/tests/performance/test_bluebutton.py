import os
import re
import unittest

from text2phenotype.common import common
from text2phenotype.common.feature_data_parsing import from_bag_of_words

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.nlp.autocode import autocode, PipelineURL


ASPECT_EXPERT_HEADERS_bluebutton_MAP = os.path.join(FeatureServiceEnv.DATA_ROOT.value,
                                                  'biomed',
                                                  'models',
                                                  'expert',
                                                  'summary',
                                                  'BIOMED-391.headers.bluebutton.map.json')

ASPECT_EXPERT_HEADERS_bluebutton_TF = os.path.join(FeatureServiceEnv.DATA_ROOT.value,
                                                 'biomed',
                                                 'models',
                                                 'expert',
                                                 'summary',
                                                 'BIOMED-391.headers.bluebutton.tf.json')


class TestBlueButton(unittest.TestCase):
    @unittest.skip('JIRA/BIOMED-412')
    def test_icd(self, do_output=False):

        for f in self.read_bluebutton_text():
            text = common.read_text(f)
            icd9_res = autocode(text, PipelineURL.icd9)
            icd10_res = autocode(text, PipelineURL.icd10)
            temp_res = autocode(text, PipelineURL.temporal_module)

            icd9_res['user'] = None
            icd10_res['user'] = None
            temp_res['user'] = None

            if do_output:
                common.write_json(icd9_res, f + '.autocode.icd9.json')
                common.write_json(icd10_res, f + '.autocode.icd10.json')
                common.write_json(temp_res, f + '.autocode.temporal.json')

    def test_biomed_391_headers(self, do_output=True):

        feature_cache = FeatureCache()
        headers = list()
        mappings = dict()

        aspect_map = feature_cache.aspect_map()
        for f in self.read_bluebutton_text():
            text = common.read_text(f)
            for line in text.splitlines():
                match = None
                if line == line.title():
                    match = line
                # two other scenario that could potentially be a header 1. all uppercase line. 2.
                # force uppercase the whole line and check section map
                if ":" in line:
                    for fragment in line.split(':'):
                        if fragment == fragment.title():
                            match = fragment

                if match and re.search('[a-zA-Z]', match):
                    if not re.search(r'\d', match):
                        if '  ' not in match:  # double space probably not header
                            if not match.startswith(' '):  # starts with space, probably not a header
                                headers.append(match)
                                mappings[match] = aspect_map.get(match.upper(), None)

        if do_output:
            headers = from_bag_of_words(headers)
            tf_file = ASPECT_EXPERT_HEADERS_bluebutton_TF
            map_file = ASPECT_EXPERT_HEADERS_bluebutton_MAP
            common.write_json(headers, tf_file)
            common.write_json(mappings, map_file)

    @staticmethod
    def read_bluebutton_text():
        expected = common.get_file_list(FeatureServiceEnv.DATA_ROOT.value + '/BIOMED', '.txt')
        expected.append(FeatureServiceEnv.DATA_ROOT.value)

        return expected
