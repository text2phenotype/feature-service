import unittest
from text2phenotype.entity.accuracy import Accuracy
from feature_service.feature_set.feature_cache import FeatureCache


class TestBiomed23(unittest.TestCase):
    def setUp(self) -> None:
        self.aspect_map = FeatureCache().aspect_map()

    @staticmethod
    def get_headers_for_drchrono():
        drchrono = """        
        Last Name,
        First Name,
        Full Name,
        Chart ID,
        Nick Name,
        Home Phone,
        Work Phone,
        Work Phone Extension,
        Cell Phone,
        Email,
        Street Address,City,State,Zip,
        Date of Birth,
        Last Visit Date,
        Gender,
        Social Security Number,
        Signature on File,
        Insurance Company,
        Insurance ID Number,
        Insurance Group Number,
        Insurance Subscriber Name,
        Insurance Subscriber Date of Birth,
        Insurance Subscriber SSN,
        Secondary Insurance,
        Secondary Insurance ID Number,
        Secondary Insurance Group Number,
        Secondary Insurance Subscriber Name,
        Secondary Insurance Subscriber Date of Birth,
        Secondary Insurance Subscriber SSN,
        Doctor
        """
        drchrono = drchrono.replace('\n', '')
        drchrono = list(filter(None, drchrono.split(',')))
        return drchrono

    def assertHeaderAccuracy(self, recall=0.0, precision=0.0):

        drchrono = self.get_headers_for_drchrono()
        expected = [header.strip().upper() for header in drchrono]
        actual = list()

        for heading in drchrono:
            heading = heading.strip().upper()
            if self.aspect_map.get(heading):
                actual.append(heading)

        score = Accuracy().compare_sets(set(expected), set(actual))

        if recall:
            self.assertGreaterEqual(score.recall(), recall)
        if precision:
            self.assertGreaterEqual(score.recall(), precision)

    def test_section_headings_strict(self):

        self.assertHeaderAccuracy(recall=1.0)
