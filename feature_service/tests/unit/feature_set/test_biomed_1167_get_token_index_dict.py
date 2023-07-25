from unittest import TestCase
from text2phenotype.common.featureset_annotations import MachineAnnotation


class TestBiomed1167(TestCase):
    def test_get_token_index_dict(self):
        INPUT_RANGES = [[0,5],  [10,15], [16, 19], [19,24]]
        annotation = MachineAnnotation()
        annotation.output_dict['range'] = INPUT_RANGES
        annotation.text_len = 25
        output = annotation.range_to_token_idx_list
        for i in range(0, 5):
            self.assertEqual(output[i], 0)
        for i in range(5,  10):
            self.assertEqual(output[i], (0, 1))
        for i in range(10, 15):
            self.assertEqual(output[i], 1)
        self.assertEqual(output[15], (1, 2))
        for i in range(16,19):
            self.assertEqual(output[i], 2)
        for i in range(19,  24):
            self.assertEqual(output[i], 3)
        self.assertEqual(output[25],  (3, 0))
