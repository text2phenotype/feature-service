import collections
import operator
import os
import unittest

from text2phenotype.common import common
from text2phenotype.common.feature_data_parsing import from_bag_of_words
from text2phenotype.common.log import logger

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.features import latinizer


###############################################################################
#
# https://github.com/text2phenotype/text2phenotype-samples/tree/dev/mtsamples/clean
#
###############################################################################
MTSAMPLES_DIR = os.path.join(FeatureServiceEnv.TEXT2PHENOTYPE_SAMPLES_PATH.value, 'mtsamples', 'clean')


class TestBiomed848_LatinPrefixSuffix(unittest.TestCase):

    def test_performance(self, do_output=False):
        trans = latinizer.Latinizer()

        latin_list = dict()
        eng_list = dict()
        token_vector = list()

        for mtsample in common.get_file_list(MTSAMPLES_DIR, '.txt'):
            text = common.read_text(mtsample)
            logger.info(mtsample)

            for token in text.lower().split():
                token = latinizer.remove_punctuation(token)
                annot = trans.annotate(token)

                # token =  sum(vector)
                # for easier human/computer testing
                token_vector.append({str(token): sum(trans.vectorize(annot))})

                if annot.get('prefix') is not None:
                    latin = annot['prefix']['latin']
                    eng = annot['prefix']['eng']

                    if not latin_list.get(latin):
                        latin_list[latin] = list()
                    latin_list[latin].append(token)

                    if not eng_list.get(eng):
                        eng_list[eng] = list()
                    eng_list[eng].append(token)

                if annot.get('suffix'):
                    latin = annot['suffix']['latin']
                    eng = annot['suffix']['eng']

                    if not latin_list.get(latin):
                        latin_list[latin] = list()
                    latin_list[latin].append(token)

                    if not eng_list.get(eng):
                        eng_list[eng] = list()
                    eng_list[eng].append(token)

            stats = {key: len(val) for key, val in latin_list.items()}
            stats = sorted(stats.items(), key=operator.itemgetter(1), reverse=True)
            stats = collections.OrderedDict(stats)

            eng_tf = {}
            for eng, tokens in eng_list.items():
                eng_tf[eng] = from_bag_of_words(tokens)

            if do_output:
                common.write_json(stats, f'{MTSAMPLES_DIR}/latin.stats.json')
                common.write_json(eng_tf, f'{MTSAMPLES_DIR}/eng.tf.json')
