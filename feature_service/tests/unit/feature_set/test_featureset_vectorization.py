import unittest
import numpy

from feature_service.feature_set.factory import get_features
from feature_service.feature_set.vectorization import vectorize_from_annotations

# the goal of this test is assert any vectorization code change
# without the intention to change the logic of vectorization
# doesn't break the encoding of the annotations given the same annotation
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType


class TestFeaturesetVectorization(unittest.TestCase):
    TEST_TOKEN = {'date_comprehension':
                      {4: [{'first': True, 'last': False, 'temporal': -1, 'rank': 0}],
                       5: [{'first': True, 'last': False, 'temporal': -1, 'rank': 0}],
                       8: [{'first': False, 'last': False, 'temporal': -1, 'rank': 1}],
                       9: [{'first': False, 'last': False, 'temporal': -1, 'rank': 1}],
                       10: [{'first': False, 'last': False, 'temporal': -1, 'rank': 1}],
                       13: [{'first': False, 'last': True, 'temporal': None, 'rank': 2}],
                       14: [{'first': False, 'last': True, 'temporal': None, 'rank': 2}],
                       15: [{'first': False, 'last': True, 'temporal': None, 'rank': 2}]},
                  'token': ['patient', 'X', 'presented', 'on', '07/08/93', ',', 'recurrent', 'in', 'September', '1999',
                            ',', 'final', 'incident', '1', 'February', ',', '2016'],
                  'len': [7, 1, 9, 2, 8, 1, 9, 2, 9, 4, 1, 5, 8, 1, 8, 1, 4],
                  'speech': ['JJ', 'NNP', 'VBD', 'IN', 'CD', ',', 'NN', 'IN', 'NNP', 'CD', ',', 'JJ', 'NN', 'CD', 'NNP',
                             ',', 'CD'],
                  'speech_bin': ['Adjectives', 'Nouns', 'Verbs', 'com_dep_wd', 'Numbers', 'unknown', 'Nouns',
                                 'com_dep_wd', 'Nouns', 'Numbers', 'unknown', 'Adjectives', 'Nouns', 'Numbers', 'Nouns',
                                 'unknown', 'Numbers'],
                  'range': [[0, 7], [8, 9], [10, 19], [20, 22], [23, 31], [31, 32], [33, 42], [43, 45], [46, 55],
                            [56, 60], [60, 61], [62, 67], [68, 76], [77, 78], [79, 87], [87, 88], [89, 93]]}

    def test_all_vectorizations_numpy_convertible(self):
        features = get_features()
        vectors = vectorize_from_annotations(MachineAnnotation(json_dict_input=self.TEST_TOKEN),
                                             feature_types={feature.feature_type for feature in features})

        # check all vectors are the correct length
        for feature in features:
            self.assertEqual(len(feature.default_vector), feature.vector_length, feature.feature_type.name)
            if vectors[feature.feature_type.name].input_dict:
                if feature.feature_type != FeatureType.document_type:
                    val = list(vectors[feature.feature_type.name].input_dict.values())[0]
                else:
                    val = vectors[feature.feature_type.name].input_dict
                self.assertEqual(len(val), feature.vector_length, feature.feature_type.name)
                numpy_vector = numpy.array(val)
                self.assertEqual(feature.vector_length, len(numpy_vector), feature.feature_type.name)
