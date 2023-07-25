import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.common import OCR_PAGE_SPLITTING_KEY
from text2phenotype.constants.features.feature_type import FeatureType

from feature_service.feature_set.annotation import annotate_text
from feature_service.feature_set.vectorization import vectorize_from_annotations
from feature_service.features.spacing import Spacing, PageBreak


class TestSpacingFeature(unittest.TestCase):
    FEATURE = Spacing()
    TEXT= 'M rand Mrs Dursley, of number four, Privet Drive, were\nproud to say that they were perfectly normal,' \
          '       thank\n\n  you very much. T'
    EXPECTED_TOKENS = {
        'token': ['M', 'rand', 'Mrs', 'Dursley', ',', 'of', 'number', 'four', ',', 'Privet', 'Drive', ',', 'were',
                  'proud', 'to', 'say', 'that', 'they', 'were', 'perfectly', 'normal', ',', 'thank', 'you', 'very',
                  'much', '.', 'T'],
        'len': [1, 4, 3, 7, 1, 2, 6, 4, 1, 6, 5, 1, 4, 5, 2, 3, 4, 4, 4, 9, 6, 1, 5, 3, 4, 4, 1, 1],
        'speech': ['NNP', 'VBP', 'NNP', 'NNP', ',', 'IN', 'NN', 'CD', ',', 'NNP', 'NNP', ',', 'VBD', 'JJ', 'TO', 'VB',
                   'IN', 'PRP', 'VBD', 'RB', 'JJ', ',', 'NN', 'PRP', 'RB', 'RB', '.', 'VB'],
        'speech_bin': ['Nouns', 'Verbs', 'Nouns', 'Nouns', 'unknown', 'com_dep_wd', 'Nouns', 'Numbers', 'unknown',
                       'Nouns', 'Nouns', 'unknown', 'Verbs', 'Adjectives', 'com_dep_wd', 'Verbs', 'com_dep_wd',
                       'Pronouns', 'Verbs', 'Adverbs', 'Adjectives', 'unknown', 'Nouns', 'Pronouns', 'Adverbs',
                       'Adverbs', 'unknown', 'Verbs'],
        'range': [[0, 1], [2, 6], [7, 10], [11, 18], [18, 19], [20, 22], [23, 29], [30, 34], [34, 35], [36, 42],
                  [43, 48], [48, 49], [50, 54], [55, 60], [61, 63], [64, 67], [68, 72], [73, 77], [78, 82], [83, 92],
                  [93, 99], [99, 100], [107, 112], [116, 119], [120, 124], [125, 129], [129, 130], [131, 132]],
        'spacing': {13: [0], 23: [0, 2], 22: [1]}
    }

    def test_annotate(self):
        annotation = self.FEATURE.annotate(self.TEXT)
        self.assertEqual(len(annotation), 3)
        annotation_list = list()

        for i in annotation:
            annotation_list.append(i[1])

        self.assertListEqual([[0], [0, 2], [1]], annotation_list)

    def test_annotation(self):
        match_annotation = annotate_text(self.TEXT, feature_types=[FeatureType.spacing])
        self.assertDictEqual(self.EXPECTED_TOKENS[FeatureType.spacing.name],
                             match_annotation[FeatureType.spacing].to_dict())

    def test_vectorization(self):
        vectors = self.FEATURE.vectorize(MachineAnnotation(json_dict_input=self.EXPECTED_TOKENS))
        self.assertEqual(vectors, {13: [1, 0, 0], 23: [1, 0, 1], 22: [0, 1, 0]})


class TestPageBreak(unittest.TestCase):
    TEXT = f"""{OCR_PAGE_SPLITTING_KEY[0]} {OCR_PAGE_SPLITTING_KEY[0]}Here is page one. {OCR_PAGE_SPLITTING_KEY[0]} 
Here is page 2.{OCR_PAGE_SPLITTING_KEY[0]} {OCR_PAGE_SPLITTING_KEY[0]}"""
    FEATURE = PageBreak()

    def test_annotate(self):
        expected = {
            (19, 20): {PageBreak.Position.AFTER.name},
            (24, 25): {PageBreak.Position.BEFORE.name}
        }

        self.assertDictEqual(expected, dict(self.FEATURE.annotate(self.TEXT)))

    def test_vectorize(self):
        annotation = annotate_text(text=self.TEXT, feature_types=[self.FEATURE.feature_type])

        vectors = vectorize_from_annotations(annotation, feature_types=[self.FEATURE.feature_type])

        expected = {4: [1, 0], 5: [0, 1]}

        self.assertDictEqual(expected, vectors.to_dict()[self.FEATURE.feature_type.name])


if __name__ == '__main__':
    unittest.main()
