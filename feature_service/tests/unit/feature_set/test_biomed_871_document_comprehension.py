import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.annotation import annotate_text
from feature_service.feature_set.vectorization import vectorize_from_annotations

text = 'patient X presented on 07/08/93, recurrent in September 1999, final incident 1 February, 2016 '
expected_annotation_2 = MachineAnnotation(
    json_dict_input={
        'date_comprehension':
            {4: [{'first': True, 'last': False, 'day': 8, 'month': 7, 'year': 1993}],
             5: [{'first': True, 'last': False, 'day': 8, 'month': 7, 'year': 1993}],
             8: [{'first': False, 'last': False, 'day': 1, 'month': 9, 'year': 1999}],
             9: [{'first': False, 'last': False, 'day': 1, 'month': 9, 'year': 1999}],
             10: [{'first': False, 'last': False, 'day': 1, 'month': 9, 'year': 1999}],
             13: [{'first': False, 'last': True, 'day': 1, 'month': 2, 'year': 2016}],
             14: [{'first': False, 'last': True, 'day': 1, 'month': 2, 'year': 2016}],
             15: [{'first': False, 'last': True, 'day': 1, 'month': 2, 'year': 2016}],
             16: [{'first': False, 'last': True, 'day': 1, 'month': 2, 'year': 2016}]},
        'token': ['patient', 'X', 'presented', 'on', '07/08/93', ',',
                  'recurrent', 'in', 'September', '1999', ',',
                  'final', 'incident', '1', 'February', ',', '2016'],
        'speech': ['JJ', 'NNP', 'VBD', 'IN', 'CD', ',', 'NN', 'IN',
                   'NNP', 'CD', ',', 'JJ', 'NN', 'CD', 'NNP', ',',
                   'CD'],
        'range': [[0, 7], [8, 9], [10, 19], [20, 22], [23, 31],
                  [31, 32], [33, 42], [43, 45], [46, 55], [56, 60],
                  [60, 61], [62, 67], [68, 76], [77, 78], [79, 87],
                  [87, 88], [89, 93]]})

expected_vectorization = [[0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                          [1, 1, 0], [1, 1, 0], [0, 0, 0], [0, 0, 0],
                          [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 0],
                          [0, 0, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1]]


class TestBiomed871(unittest.TestCase):
    def test_annotate(self):
        actual = annotate_text(text, feature_types=[FeatureType.date_comprehension])
        self.assertEqual(actual.to_dict(), expected_annotation_2.to_dict())

    def test_vectorize(self):
        vector = vectorize_from_annotations(expected_annotation_2, feature_types=[FeatureType.date_comprehension])
        for t in expected_annotation_2[FeatureType.date_comprehension.name].input_dict.keys():
            self.assertListEqual(vector[FeatureType.date_comprehension.name][t], expected_vectorization[t])
