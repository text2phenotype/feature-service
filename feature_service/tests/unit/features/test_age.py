import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.age import Age
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class AgeTests(AnnotateTestsBase):
    feature = Age()

    def test_annotate(self):
        actual = self.feature.annotate(self.TEST_INPUT_CAROLYN)

        # all of these should be regex hits in the text
        self.assertTrue(self.find_match('$AGE6', actual))
        self.assertTrue(self.find_match('$YEARS_word', actual))

    def test_vectorize(self):
        machine_annotation = annotation.annotate_text('Pt is 35yo female', feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        # AGE6, AGE8, AGE_word, YEARS_word
        expected = {2: [0, 1, 0, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
