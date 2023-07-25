import os
import unittest

from text2phenotype.common.log import operations_logger
from text2phenotype.common import common

from feature_service.tests.experiment.i2b2 import i2b2_2014


#####################################################################################
#
# Dictionary counts from CTAKES processed examples
#
#####################################################################################

def get_dict_count_for_i2b2_deid_samples() -> dict:
    """
    :return: dict counts of vocab:tf ( str:int )
    """

    train_file_list = i2b2_2014.get_training_files(file_type='.json')
    test_file_list = i2b2_2014.get_testing_files(file_type='.json')

    dict_count = dict()
    # train this model on both training and testing folder of i2b2 dataset
    train_file_list.extend(test_file_list)
    for _file_tokens in train_file_list:

        if os.path.exists(_file_tokens):
            operations_logger.debug(_file_tokens)
            _json = common.read_json(_file_tokens)
            for token in _json['tokenize']:
                if 'umls' in token.keys():
                    for hit in token['umls']:  # TODO: this is no longer umls, it is now "clinical", "drug_ner", etc.
                        dictionary = list(hit.values())[0]
                        if dictionary in dict_count:
                            dict_count[dictionary] += 1
                        else:
                            dict_count[dictionary] = 1
    return dict_count


#####################################################################################

class TestBiomed24(unittest.TestCase):

    @unittest.skip('JIRA/BIOMED-224')
    def test_dict_count(self):
        dict_count = get_dict_count_for_i2b2_deid_samples()

        self.assertTrue(False)
