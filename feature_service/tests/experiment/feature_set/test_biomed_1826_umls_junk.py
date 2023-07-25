import os
import unittest
import re
from typing import List, Dict
from text2phenotype.common.feature_data_parsing import from_bag_of_words
from text2phenotype.common import common
from text2phenotype.constants.features import FeatureType
from feature_service.nlp.nlp_reader import ClinicalReader, DrugReader, LabReader
from feature_service.nlp import nlp_cache

# TODO: Point in time
# TODO: [Presence]
# TODO: [Units/volume]
# TODO: hex codes https://www.codetable.net/hex/7c
# TODO: :Pt:

UMLS_BSV_DIR = os.environ.get('UMLS_DICT_DIR', '/Users/andy.mcmurry/code/ctakes/src/main/resources/com/text2phenotype/ctakes/resources/dictionaries/')

def match_semtype(text:str)->str:
    """
    :param text:
    :return:
    """
    semtype = "\(([a-z]+\s?)+\)"
    match = re.search(semtype, text)
    if match:
        start,stop = match.span()
        return text[start:stop]
    return None

class TestBiomed1826_UMLS_Update_JunkWords(unittest.TestCase):

    def test_vocab(self, vocab='snomedct'):
        res = list()

        for f in common.get_file_list(f'{UMLS_BSV_DIR}/{vocab}' '.bsv'):
            print(f)
            text = common.read_text(f)
            for line in text.splitlines():
                match =match_semtype(line)
                if match and len(match) > 3:
                    res.append(match)

        bow = from_bag_of_words(res)
        print(bow)
        common.write_json(bow, f'./junk.{vocab}.json')