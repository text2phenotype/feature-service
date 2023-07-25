import unittest

from feature_service.common.bsv import parse_bsv_semantic_aspect
from feature_service.resources import TUI_RULE_BSV


class TestBiomed243(unittest.TestCase):

    def test_semantic_aspect_bsv(self):
        """
        JIRA/BIOMED-243
        """
        # parse ruleset from expert curated TUI_RULE file
        curated = parse_bsv_semantic_aspect(TUI_RULE_BSV)

        # Allergy spot-checing a well known example
        aspect_list_t131 = curated['T131']['aspect_list']

        self.assertEqual(1,  len(aspect_list_t131))
        self.assertEqual(22, len(curated))
        self.assertEqual('allergy', aspect_list_t131.pop())
