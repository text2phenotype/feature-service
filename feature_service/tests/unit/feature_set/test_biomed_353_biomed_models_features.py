import unittest

from feature_service.feature_set.feature_cache import FeatureCache
from text2phenotype.ccda.section import Aspect


class TestBiomed353(unittest.TestCase):
    def setUp(self) -> None:
        self.feature_cache: FeatureCache = FeatureCache()

    def assertSize(self, expected_num: int, actual_collection):
        self.assertEqual(expected_num, len(actual_collection))

    def test_aspect(self):
        """
        12 aspect types
        688 section headers mapped to aspects
        """
        self.assertSize(12, Aspect.get_active_aspects())
        self.assertSize(988, self.feature_cache.aspect_map())

    def test_person_names(self):
        """
        85045 person names
        """
        self.assertSize(85046, self.feature_cache.person_names())

    def test_locations_zipcodes(self):
        """
        42523 US Zip Codes
        """
        self.assertSize(42523, self.feature_cache.zip_codes_dict())

    def test_tf_locations_usa(self):
        self.assertSize(18759, self.feature_cache.tf_usa_cities())
        # TODO: JIRA/BIOMED-358
        self.assertSize(63, self.feature_cache.tf_usa_states())

    def test_tf_patient_names(self):
        """
        TF patient names (more first names than last names?)
        """
        self.assertSize(322272, self.feature_cache.tf_patients_last_name())
        self.assertSize(77208, self.feature_cache.tf_patients_first_name())

    def test_tf_corpus(self):
        """
        Term Frequency of various corpus
        :return:
        """
        self.assertSize(36410, self.feature_cache.tf_i2b2())
        self.assertSize(5383, self.feature_cache.tf_ccda())
        self.assertSize(28102, self.feature_cache.tf_mtsamples())

    def test_tf_npi(self):
        """
        NPI National Provider ID file
        """
        self.assertSize(18810, self.feature_cache.tf_npi_city())
        self.assertSize(177793, self.feature_cache.tf_npi_first_name())
        self.assertSize(290625, self.feature_cache.tf_npi_address())
        self.assertSize(543118, self.feature_cache.tf_npi_last_name())
        self.assertSize(3306191, self.feature_cache.tf_npi_phone())

    def test_tf_umls_concepts(self):
        """
        2+ million umls concept strings
        """
        self.assertSize(2664494, self.feature_cache.tf_mrconso())
