import unittest

from feature_service.common.bsv import read_curated
from feature_service.resources import PUBMED_BSV
from text2phenotype.ccda.section import Aspect


class TestBiomed240(unittest.TestCase):

    def test_reading_writing_expert_annotations(self):

        bsv, mapping = read_curated(PUBMED_BSV)

        expected = [Aspect.__members__.keys(), 'IGNORE']

        for aspect_name in mapping.keys():
            self.assertIn(aspect_name, expected)
