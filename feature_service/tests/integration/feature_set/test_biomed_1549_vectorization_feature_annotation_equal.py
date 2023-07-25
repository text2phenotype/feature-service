import unittest
from text2phenotype.constants.features.feature_type import FeatureType
from feature_service.feature_set.annotation import annotate_text


class TestBiomed1549(unittest.TestCase):
    TEXT = "Hematocrit level 100, White Blood Cell Count 2"
    ANNOTATED_LAB_HEPC = annotate_text(text=TEXT, feature_types={FeatureType.lab_hepc})

    def test_lab_hepc_equivalence(self):
        actual_annotation = annotate_text(text=self.TEXT, feature_types={FeatureType.lab_hepc_attributes})
        self.assertDictEqual(self.ANNOTATED_LAB_HEPC.to_dict(), actual_annotation.to_dict())

    def test_both_feat_annotation_equal(self):
        actual_annotation = annotate_text(text=self.TEXT, feature_types={FeatureType.lab_hepc_attributes,
                                                                         FeatureType.lab_hepc})
        self.assertDictEqual(self.ANNOTATED_LAB_HEPC.to_dict(), actual_annotation.to_dict())





