import unittest

from feature_service.feature_set import annotation, vectorization
from feature_service.features.address import Address
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class AddressTests(AnnotateTestsBase):
    feature = Address()
    text = 'Our address is: 1 S. CALIFORNIA ST, 4TH Fl, SAN FRANCISCO, CA 94111-0111.  Visit us anytime.'

    def test_annotate(self):
        actual = list(self.feature.annotate(self.text))

        self.assertEqual(6, len(actual))
        self.find_match('$STREET_TYPE', actual)
        self.find_match('$CARDINALS', actual)
        self.find_match('$LOCATION_FLOOR_1', actual)
        self.find_match('$ADDRESS4', actual)
        self.find_match('$ADDRESS5', actual)
        self.find_match('$ADDRESS7', actual)


    def test_vectorize(self):
        machine_annotation = annotation.annotate_text(self.text, feature_types=[self.feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[self.feature.feature_type])

        observed = vectors.output_dict[self.feature.feature_type].input_dict

        # CARDINALS, LOCATION_FLOOR_1, LOCATION_FLOOR_2, POBOX, ROOM, STREET_TYPE
        expected = {7: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                    5: [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                    9: [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                    10: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    12: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    13: [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    14: [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    15: [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    16: [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    4: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    6: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    8: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]}

        self.assertDictEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
