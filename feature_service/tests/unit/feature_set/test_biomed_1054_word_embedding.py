# Basic unit test for word embedding load and type
import unittest


from text2phenotype.common.featureset_annotations import  MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.vectorization import vectorize_from_annotations


class TestBiomed1054WordEmbedding(unittest.TestCase):

    def test_word_embedding(self):

        actual = vectorize_from_annotations(
            MachineAnnotation(json_dict_input={'token': ['the', 'UNK']}),
            feature_types=[FeatureType.word2vec_mimic])

        for i in range(len(actual)):
            self.assertTrue(isinstance(actual[FeatureType.word2vec_mimic.name][i], list))
            for j in range(len(actual[FeatureType.word2vec_mimic.name][i])):
                self.assertTrue(isinstance(actual[FeatureType.word2vec_mimic.name][i][j], float))
