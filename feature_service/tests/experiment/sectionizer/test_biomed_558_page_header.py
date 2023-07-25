import os
import unittest
from feature_service.features.sectionizer import Sectionizer

path = os.path.join(os.getcwd(), os.path.dirname(__file__))


class TestBiomed558PageHeader(unittest.TestCase):

    def test_sectionizer(self):

        expected_matches = [
            {'PAGE_HEADER': ['page 1 of 3', 0, 11]},
            {'PAGE_HEADER': ['Page 2', 208, 214]},
            {'PAGE_HEADER': ['page 3', 216, 222]},
            {'PAGE_HEADER': ['PAGE 1', 224, 230]},
            {'PAGE_HEADER': ['Page 21', 241, 248]},
            {'PAGE_HEADER': ['page 1 Of 3', 485, 496]},
            {'PAGE_HEADER': ['page 33', 749, 756]},
            {'PAGE_HEADER': ['page 1 OF 3', 1206, 1217]},
            {'PAGE_HEADER': ['Page 1 of 3', 1252, 1263]},
            {'PAGE_HEADER': ['Page 1 Of 3', 1887, 1898]},
            {'PAGE_HEADER': ['Page 1 OF 3', 2369, 2380]},
            {'PAGE_HEADER': ['PAGE 1 of 3', 2674, 2685]},
            {'PAGE_HEADER': ['PAGE 1 Of 3', 3154, 3165]},
            {'PAGE_HEADER': ['PAGE 1 OF 3', 3494, 3505]},
            {'PAGE_HEADER': ['page 5 of 13', 3771, 3783]},
            {'PAGE_HEADER': ['page 5 Of 13', 4025, 4037]},
            {'PAGE_HEADER': ['page 5 OF 13', 4654, 4666]},
            {'PAGE_HEADER': ['PAGE 19', 5000, 5007]},
            {'PAGE_HEADER': ['Page 5 of 13', 5327, 5339]},
            {'PAGE_HEADER': ['Page 5 Of 13', 5633, 5645]},
            {'PAGE_HEADER': ['Page 5 OF 13', 6000, 6012]},
            {'PAGE_HEADER': ['PAGE 5 of 13', 6279, 6291]},
            {'PAGE_HEADER': ['PAGE 5 Of 13', 6292, 6304]},
            {'PAGE_HEADER': ['PAGE 5 OF 13', 6305, 6317]},
            {'PAGE_HEADER': ['page 15 of 23', 6511, 6524]},
            {'PAGE_HEADER': ['page 15 Of 23', 6525, 6538]},
            {'PAGE_HEADER': ['page 15 OF 23', 6996, 7009]},
            {'PAGE_HEADER': ['Page 15 Of 23', 7197, 7210]},
            {'PAGE_HEADER': ['Page 15 of 23', 7425, 7438]},
            {'PAGE_HEADER': ['Page 15 OF 23', 7440, 7453]},
            {'PAGE_HEADER': ['PAGE 15 of 23', 7717, 7730]},
            {'PAGE_HEADER': ['PAGE 15 Of 23', 7764, 7777]},
            {'PAGE_HEADER': ['PAGE 15 OF 23', 7857, 7870]}
        ]
        test_target = Sectionizer()
        with open(os.path.join(path, 'page-header-sample-text.txt'), 'r') as f:
            found_matches = test_target.match_pattern(f.read(), 'PAGE_HEADER')

        for found_match in found_matches:
            key, value = list(found_match.items())[0]
            with self.subTest(pattern=key, parsed_value=value):
                self.assertTrue(found_match in expected_matches,
                                f"Match not found in expected values for pattern {key}.")

        self.assertEqual(len(found_matches), len(expected_matches),
                         "Count of found matches not equal to expected.")
