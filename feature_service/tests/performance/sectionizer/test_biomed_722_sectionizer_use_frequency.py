import os
import unittest
import pandas

from text2phenotype.common import common
from text2phenotype.common.log import operations_logger

from feature_service.features import Sectionizer
from feature_service.feature_service_env import FeatureServiceEnv


header_patterns = ['HEADER', 'HEADER_UPPER', 'HEADER_TITLE', 'LIST_HEADER', 'HEADER_COLON', 'SUBHEADER_COLON']


class TestBiomed722SectionizerUsage(unittest.TestCase):

    def test_batch(self, save_output=False):
        output_dict = dict()
        sectionizer = Sectionizer()
        for f in common.get_file_list(FeatureServiceEnv.DATA_ROOT.value, '.txt'):
            text = common.read_text(f)

            res = sectionizer.match_sectionizer(text)
            for h in res:
                for key, value in h.items():
                    if key in header_patterns:
                        if 'match' in value:
                            header = value['match'][0]
                            match = True
                        else:
                            header = value[0]
                            match = False
                        if header in output_dict:
                            output_dict[header]['Frequency'] += 1
                        else:
                            output_dict[header] = {'Frequency': 1, 'Matched': match}
        output = pandas.DataFrame(output_dict)
        output_t = output.transpose()
        output_ts = output_t.sort_values(['Matched', 'Frequency'], ascending=[1, 0])

        if save_output:
            ver = 'Sectionizer_Usage'
            json_path = os.path.join(FeatureServiceEnv.DATA_ROOT.value, f'{ver}.json')

            output_ts.to_json(json_path)
        else:
            operations_logger.info(output_ts)
