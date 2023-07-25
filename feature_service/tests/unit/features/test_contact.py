import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.contact import ContactInfo
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class ContactInfoTests(AnnotateTestsBase):
    feature = ContactInfo()

    def test_annotate(self):
        actual = self.feature.annotate(self.TEST_INPUT_CAROLYN)

        # all of these should be regex hits in the text
        self.assertTrue(self.find_match('$TELEPHONE0', actual))
        self.assertTrue(self.find_match('$TELEPHONE1', actual))
        self.assertTrue(self.find_match('$TELEPHONE2', actual))

    def test_vectorize(self):
        text = """Name: Mike
Email: mike.banos
Phone: +1 123-456-7890 extens. 1"""

        machine_annotation = annotation.annotate_text(text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        expected = {
            5: [1, 0, 0, 0, 0, 0, 0],
            6: [1, 0, 0, 0, 0, 0, 0],
            7: [1, 0, 0, 0, 0, 0, 0],
            10: [0, 0, 1, 1, 0, 0, 0],
            11: [0, 0, 0, 1, 1, 0, 1],
            12: [0, 1, 0, 0, 0, 0, 0],
            13: [0, 1, 0, 0, 0, 0, 0],
            14: [0, 1, 0, 0, 0, 0, 0]
        }

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
