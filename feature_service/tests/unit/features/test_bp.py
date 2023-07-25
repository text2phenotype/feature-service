import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.bp import BloodPressure
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class BloodPressureTests(AnnotateTestsBase):
    feature = BloodPressure()

    def test_annotate(self):
        actual = self.feature.annotate(self.TEST_INPUT_CAROLYN)

        self.assertTrue(self.find_match('$BLOOD_PRESSURE_CHART', actual))

    def test_vectorize(self):
        machine_annotation = annotation.annotate_text('BP: 120/80.  Pt would be dead at 300/100',
                                                      feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {2: [1]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
