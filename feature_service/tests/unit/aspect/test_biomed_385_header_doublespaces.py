import unittest

from feature_service.feature_set.feature_cache import FeatureCache


class TestBiomed385(unittest.TestCase):

    def test_double_spaces(self, output=False):

        single_space = dict()
        double_space = dict()

        for header, aspect in FeatureCache().aspect_map().items():
            if '  ' in header:
                double_space[header] = aspect
                single_space[header.replace('  ', ' ')] = aspect

        if output and len(double_space) > 0:
            self.assertEqual(0, len(double_space))
