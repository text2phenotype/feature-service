import os
import unittest

from feature_service.nlp.autocode import _expand_ctakes_response
from text2phenotype.common import common


class TestAutocode(unittest.TestCase):
    def test_expand_ctakes(self):
        local_dir = os.path.dirname(__file__)

        exp_response = common.read_json(os.path.join(local_dir, 'ctakes_expanded_response.json'))

        raw_response = common.read_json(os.path.join(local_dir, 'ctakes_raw_response.json'))
        obs_response = _expand_ctakes_response(raw_response)

        self.assertDictEqual(exp_response, obs_response)


if __name__ == '__main__':
    unittest.main()
