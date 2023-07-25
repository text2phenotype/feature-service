import unittest

from text2phenotype.common.feature_data_parsing import from_bag_of_words

from feature_service.feature_set.feature_cache import FeatureCache


class TestBiomed386(unittest.TestCase):

    def test_create_header_tf(self):
        word_list = list()
        for header in FeatureCache().aspect_map():
            word_list += header.split()

        from_bag_of_words(word_list)
