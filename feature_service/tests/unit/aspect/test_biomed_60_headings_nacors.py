import unittest

from text2phenotype.entity.accuracy import Accuracy
from feature_service.feature_set.feature_cache import FeatureCache


class TestSectionsNACORS(unittest.TestCase):

    @staticmethod
    def get_headers_nacors():
        expected = """
        DEMOGRAPHICS
        ENCOUNTER
        SOAP
        CITY
        STATE
        MOBILE
        MOBILE PHONE
        GUARANTOR
        PATIENT INFO
        PATIENT INFORMATION
        """
        expected = [header.strip() for header in expected.splitlines()]
        expected = list(filter(None, expected))

        return expected

    def test_biomed_60_nacors(self):
        nacors = self.get_headers_nacors()
        actual = []
        aspect_map = FeatureCache().aspect_map()
        for header in nacors:
            if header:
                if aspect_map.get(header) is not None:
                    actual.append(header)

        Accuracy().compare_sets(set(nacors), set(actual))
        self.assertEqual(set(nacors), set(actual))
