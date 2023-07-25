import unittest
import os

from text2phenotype.common import common

from feature_service.aspect.chunker import Chunker
from feature_service.feature_service_env import FeatureServiceEnv


class TestBiomed250(unittest.TestCase):
    def setUp(self) -> None:
        self.chunker = Chunker()

    def assertTextSpan(self, chunker_function):
        """
        This test doesn't check if the aspect is correct.
        This text does check if the test range (aka SPAN) is correct.

        :param chunker_function: see biomed.aspect.chunker
        """
        test_data = os.path.join(FeatureServiceEnv.DATA_ROOT.value, 'emr', 'OpenEMR', 'carolyn-blose.pdf.txt')
        text = common.read_text(test_data)

        positions = chunker_function(text)

        for chunk in positions:
            span = chunk['range']
            expected = text[span[0]:span[1]]

            self.assertEqual(expected, chunk['text'], f"text did not match for span {span}, expected: {expected}")

    def test_predict_aspect_emb_by_line(self):
        """
        Aspect labeler token based similarity (TF+ Neural Nets)
        """
        self.assertTextSpan(self.chunker.predict_aspect_emb_by_line)

    def test_return_aspect_emb_section_positions_enforce(self):
        """
        If we found a header then enforce that aspect on the text.
        """
        self.assertTextSpan(self.chunker.return_aspect_emb_section_positions_enforce)

    @unittest.skip('JIRA/BIOMED-250')
    def test_predict_aspect_emb_by_section_no_enforce(self):
        """
        If we found a header we use aspect labeler to predict the aspect instead of assigning the header aspect.
        """
        self.assertTextSpan(self.chunker.predict_aspect_emb_by_section_no_enforce)
