import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.patient import Patient
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class PatientTests(AnnotateTestsBase):
    feature = Patient()

    def test_annotate(self):
        actual = dict(self.feature.annotate(self.TEST_INPUT_CAROLYN))

        expected = {
            (193, 195): [{'$MR': 'Mr'}],
            (373, 382): [{'$SUSPICIOUS_NUM': '266919005'}, {'$SSN': '266919005'}],
            (227, 233): [{'$ACCESSION_KP': '530-79'}],
            (227, 238): [{'$SSN': '530-79-5301'}],
            (89, 96): [{'$SUSPICIOUS_NUM2': '000-000'}, {'$ACCESSION_KP': '000-000'}],
            (117, 124): [{'$SUSPICIOUS_NUM2': '000-000'}, {'$ACCESSION_KP': '000-000'}],
            (231, 238): [{'$SUSPICIOUS_NUM2': '79-5301'}],
            (93, 101): [{'$RN_KPNW': '000-0000'}],
            (121, 129): [{'$RN_KPNW': '000-0000'}]
        }

        self.assertDictEqual(expected, actual)

    def test_vectorize(self):
        machine_annotation = annotation.annotate_text('Pt SSN: 123-45-6789', feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {3: [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
