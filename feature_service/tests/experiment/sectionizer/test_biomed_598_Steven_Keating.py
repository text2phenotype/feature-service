import os
import json
import unittest
from feature_service.features.sectionizer import Sectionizer


class TestBiomed598StevenKeating(unittest.TestCase):

    def test_sectionizer(self):
        test_target = Sectionizer()
        dir_path = os.path.join(os.getcwd(), os.path.dirname(__file__))
        with open(os.path.join(dir_path, 'Steven_Keating_Health_Summary_Report.txt'), 'r') as f:
            found_matches = test_target.match_sectionizer(f.read())

        with open(os.path.join(dir_path, 'Steven_Keating_Health_Summary_Report_expected_matches.json'), 'r') as f:
            expected_matches = json.load(f)

        for found_match in found_matches:
            key, value = list(found_match.items())[0]
            with self.subTest(pattern=key, parsed_value=value):
                self.assertTrue(found_match in expected_matches,
                                f"Match not found in expected values for pattern {key}.")

        self.assertEqual(len(found_matches), len(expected_matches),
                         "Count of found matches not equal to expected.")
