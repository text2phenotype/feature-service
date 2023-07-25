import unittest

from feature_service.features import UnitsOfMeasure
from feature_service.constants.unit_bin import UnitBin


class UnitsOfMeasureTests(unittest.TestCase):
    test_case1 = {
        'text': 'Aspirin 50 mg twice daily',
        'annotations': {
            (11, 13): ['mg']
        },
        'vectors': {
            (11, 13): [1, 0, 0, 1, 0, 0, 0, 0]
        }
    }
    test_case2 = {
        'text': 'Potassium 5.9 g/L',
        'annotations': {
            (14, 17):  ['g/l']
        },
        'vectors': {
            (14, 17): [1, 1, 0, 0, 0, 0, 0, 0]
        }
    }

    test_case3 = {
        'text': 'Text without units',
        'annotations': {},
        'vectors': {}
    }

    test_case4 = {
        'text': 'Test vectors for: days , g/mmol , hours/days , pound',
        'annotations': {
            (18, 22): ['days'],
            (25, 31): ['g/mmol'],
            (34, 44): ['hours/days'],
            (47, 52): ['pound']
        },
        'vectors': {
            (18, 22): [1, 0, 0, 0, 0, 1, 0, 0],
            (25, 31): [1, 1, 0, 0, 1, 0, 0, 0],
            (34, 44): [1, 1, 0, 0, 0, 1, 1, 0],
            (47, 52): [1, 0, 0, 0, 0, 0, 0, 1]
        }
    }

    def test_units_annotation(self):
        feature = UnitsOfMeasure()

        # for test_case in [self.test_case1, self.test_case2, self.test_case3, self.test_case4]:
        for test_case in [self.test_case4]:
            annotations = feature.annotate(test_case['text'])
            self.assertEqual(len(annotations), len(test_case['annotations']))
            for annotation in annotations:
                key = tuple(annotation[0])
                self.assertIn(key, test_case['annotations'])
                expected_annotation = test_case['annotations'][key]
                self.assertEqual(annotation[1], expected_annotation)

    def test_units_vectorization(self):
        feature = UnitsOfMeasure()

        non_unit_token = {}
        non_unit_vector = feature.feature_zero(len(UnitBin.__members__) + 1)

        for test_case in [self.test_case1, self.test_case2, self.test_case3, self.test_case4]:
            # convert text to featured tokens
            tokens = test_case['text'].split(sep=' ')
            for token in tokens:
                token_range = (test_case['text'].find(token), test_case['text'].find(token) + len(token))
                expected_vector = test_case['vectors'].get(token_range, non_unit_vector)
                if token_range in test_case['vectors']:
                    actual_vector = feature.vectorize_token(test_case['annotations'][token_range])
                    self.assertEqual(actual_vector, expected_vector)
                else:
                    self.assertEqual(expected_vector, feature.default_vector)
