import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.gender import Gender
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class GenderTests(AnnotateTestsBase):
    feature = Gender()

    def test_annotate(self):
        actual = self.feature.annotate(self.TEST_INPUT_CAROLYN)

        # FEMALE - 3
        self.assertEqual(3, self.find_match_count('$GENDER1', actual))

    def test_vectorize(self):
        text = 'Pt is 40yo female'

        machine_annotation = annotation.annotate_text(text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {3: [1, 0, 0, 0, 0, 0, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
