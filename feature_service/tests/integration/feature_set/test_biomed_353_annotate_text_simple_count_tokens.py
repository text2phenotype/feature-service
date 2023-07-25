import unittest
from feature_service.feature_set.annotation import annotate_text


class TestBiomed353(unittest.TestCase):

    def test_annotate_text_simple_tokenization(self):
        machine_annotation = annotate_text('The patient name is Stephan Garcia and his PCP is DeLeys Brandman')

        self.assertEqual(12, len(machine_annotation))
        self.assertEqual('Stephan', machine_annotation.tokens[4])
        self.assertEqual('Garcia', machine_annotation.tokens[5])
