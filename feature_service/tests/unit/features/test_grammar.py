import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.grammar import Grammar
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class GrammarTests(AnnotateTestsBase):
    feature = Grammar()

    def test_annotate(self):
        actual = self.feature.annotate(self.TEST_INPUT_CAROLYN)

        self.assertTrue(self.find_match('$COLON', actual))
        self.assertTrue(self.find_match('$COMMA', actual))
        self.assertTrue(self.find_match('$CONTAINS_SLASH', actual))
        self.assertTrue(self.find_match('$CONTAINS_DASH', actual))
        self.assertTrue(self.find_match('$OPEN BRACKET', actual))
        self.assertTrue(self.find_match('$CLOSE BRACKET', actual))

    def test_vectorize(self):
        machine_annotation = annotation.annotate_text('Hello, world', feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {1: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
