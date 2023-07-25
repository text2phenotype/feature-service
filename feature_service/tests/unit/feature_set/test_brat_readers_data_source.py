from typing import Dict, List
from unittest import TestCase
import os

from feature_service.common.data_source import FeatureServiceDataSource
from text2phenotype.annotations.file_helpers import Annotation


class TestBratReader(TestCase):
    BRAT_FORMAT_FILE = os.path.join(os.path.dirname(__file__), 'sample_brat.ann')
    SANDS_FORMAT_FILE = os.path.join(os.path.dirname(__file__), 'sample_sands.ann')

    def test_parse_brat_format(self):
        brat_output = FeatureServiceDataSource.parse_brat_ann_with_link_info(self.BRAT_FORMAT_FILE)
        expected_output = [{'aspect': 'facility_name',
                            'range': [934, 954],
                            'text': 'Partners Health Care',
                            'link': [],
                            'tag': 'T32'},
                           {'aspect': 'facility_name',
                            'range': [955, 971],
                            'text': 'Prudential Tower',
                            'link': ['T32'],
                            'tag': 'T32_1'},
                           {'aspect': 'DATE',
                            'range': [1255, 1265],
                            'text': '02/12/2014',
                            'link': None,
                            'tag': 'T1'},
                           {'aspect': 'DATE',
                            'range': [1331, 1341],
                            'text': '02/12/2014',
                            'link': None,
                            'tag': 'T39'},
                           {'aspect': 'DATE',
                            'range': [1408, 1418],
                            'text': '02/12/2014',
                            'link': None,
                            'tag': 'T40'},
                           {'aspect': 'DATE',
                            'range': [1489, 1499],
                            'text': '02/12/2014',
                            'link': None,
                            'tag': 'T41'},
                           {'aspect': 'DATE',
                            'range': [1576, 1586],
                            'text': '02/12/2014',
                            'link': None,
                            'tag': 'T42'}]
        self.assert_annotation_dict_equal(brat_output, expected_output)

    def assert_annotation_dict_equal(self, brat_output: Dict[str, Annotation], dict_list: List[dict]):
        self.assertEqual(len(brat_output), len(dict_list))
        for i in range(len(brat_output)):
            expected_entry = dict_list[i]
            tag = dict_list[i]['tag']
            annotation = brat_output[tag]
            self.assertEqual(annotation.label, expected_entry['aspect'])
            self.assertEqual(annotation.uuid, expected_entry['tag'])
            self.assertEqual(annotation.text_range, expected_entry['range'])
            self.assertEqual(annotation.text, expected_entry['text'])

    def test_parse_sands_format(self):
        brat_output = FeatureServiceDataSource.parse_brat_ann_with_link_info(self.SANDS_FORMAT_FILE)
        expected_output = [{'aspect': 'problem',
                            'range': [3106, 3119],
                            'text': 'adenocarcinoma',
                            'link': None,
                            'tag': '71e911746a7043c89e9f5a1d9ee32a84'},
                           {'aspect': 'problem',
                            'range': [7481, 7485],
                            'text': 'NSCLC',
                            'link': None,
                            'tag': '0d75eab9ede94136a83898c86a5ef49a'},
                           {'aspect': 'problem',
                            'range': [8083, 8087],
                            'text': 'NSCLC',
                            'link': None,
                            'tag': '49423132c84c485d8185337577f5c88c'},
                           {'aspect': 'med',
                            'range': [6818, 6825],
                            'text': 'tyrosine',
                            'link': None,
                            'tag': '8171cb25a5924a2d910791295212e2cc'},
                           {'aspect': 'med',
                            'range': [6965, 6973],
                            'text': 'Erlotinib',
                            'link': None,
                            'tag': '1d7c3aadf1294bb8b0f0f6d5f8dfbdf8'},
                           {'aspect': 'med',
                            'range': [8294, 8304],
                            'text': 'osimertinib',
                            'link': None,
                            'tag': '54ea9543bd674244872fd3c51137c8d9'},
                           {'aspect': 'hospital',
                            'range': [3, 12],
                            'text': 'UNIVERSITY',
                            'link': None,
                            'tag': '251be28bd06f4414966b6ea3d3581e5a'}]
        self.assert_annotation_dict_equal(brat_output, expected_output)
