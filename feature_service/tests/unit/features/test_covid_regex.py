import unittest

from text2phenotype.constants.features.feature_type import FeatureType

from feature_service.feature_set.annotation import annotate_text
from feature_service.feature_set.vectorization import vectorize_from_annotations

class TestCovidRegex(unittest.TestCase):
    def test_covid_annotate_text(self):
        text = "SARS-COV-2 cover up COVID-19  coronavirus HKU1  SARS-CoV-2 NAA  COVID-19 Coronavirus RNA Nasopharyngeal" \
               " MERS-CoV-2"
        annotation = annotate_text(text=text, feature_types=[FeatureType.regex_covid])
        expected = {'token': ['SARS-COV-2', 'cover', 'up', 'COVID-19', 'coronavirus', 'HKU1', 'SARS-CoV-2', 'NAA',
                              'COVID-19', 'Coronavirus', 'RNA', 'Nasopharyngeal', 'MERS-CoV-2'],
                    'speech': ['NN', 'NN', 'IN', 'NNP', 'NN', 'NNP', 'NNP', 'NNP', 'NNP', 'NNP', 'NNP', 'NNP', 'NNP'],

                    'range': [[0, 10], [11, 16], [17, 19], [20, 28], [30, 41], [42, 46], [48, 58], [59, 62], [64, 72],
                              [73, 84], [85, 88], [89, 103], [104, 114]],
                    'regex_covid': {0: [{'$SARS': 'SARS'}, {'$COVID': 'COV'}],
                                    6: [{'$SARS': 'SARS'}, {'$COVID': 'CoV'}],
                                    3: [{'$COVID': 'COVID'}],
                                    8: [{'$COVID': 'COVID'}],
                                    12: [{'$COVID': 'CoV'}, {'$NEG_TEST_MODIFIERS': 'MERS'}],
                                    4: [{'$CORONAVIRUS': 'coronavirus'}],
                                    9: [{'$CORONAVIRUS': 'Coronavirus'}],
                                    7: [{'$TEST_MODIFIERS': 'NAA'}],
                                    10: [{'$TEST_MODIFIERS': 'RNA'}],
                                    5: [{'$NEG_TEST_MODIFIERS': 'HKU1'}]}}

        self.assertDictEqual(annotation.to_dict(), expected)

    def test_vectorization(self):
        text = "SARS-COV-2 cover up COVID-19  coronavirus HKU1  SARS-CoV-2 NAA  COVID-19 Coronavirus RNA Nasopharyngeal" \
               " MERS-CoV-2"

        annotation = annotate_text(text=text, feature_types=[FeatureType.regex_covid])
        vectors = vectorize_from_annotations(annotation, feature_types=[FeatureType.regex_covid])

        expected = {'regex_covid':
                        {0: [0, 1, 0, 1, 0],
                         6: [0, 1, 0, 1, 0],
                         3: [0, 1, 0, 0, 0],
                         8: [0, 1, 0, 0, 0],
                         12: [0, 1, 1, 0, 0],
                         4: [1, 0, 0, 0, 0],
                         9: [1, 0, 0, 0, 0],
                         7: [0, 0, 0, 0, 1],
                         10: [0, 0, 0, 0, 1],
                         5: [0, 0, 1, 0, 0]},
                    'defaults': {'regex_covid': [0, 0, 0, 0, 0]}}


        self.assertDictEqual(vectors.to_dict(), expected)
