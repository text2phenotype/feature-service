import unittest

from text2phenotype.constants.features.feature_type import FeatureType
from feature_service.feature_set.annotation import annotate_text
from feature_service.feature_set.vectorization import vectorize_from_annotations
from feature_service.features.imaging_regex import ImagingRegex


class TestImagingRegex(unittest.TestCase):
    TXT = 'XR, CXR, x-ray, echocardiogram, blah, EKG, ECG, MRI, TTE, TEE, CT, ultrasound'

    def test_annotate_vectorize(self):
        annotation = annotate_text(self.TXT, feature_types=[FeatureType.imaging_regex])
        expected_annotation = {0: [{'$XRAY': 'XR'}], 2: [{'$XRAY': 'CXR'}], 4: [{'$XRAY': 'x-ray'}],
                               10: [{'$EKG': 'EKG'}], 12: [{'$EKG': 'ECG'}], 14: [{'$MRI': 'MRI'}],
                               6: [{'$ECHO': 'echocardiogram'}], 16: [{'$ECHO_ABBREV': 'TTE'}],
                               18: [{'$ECHO_ABBREV': 'TEE'}], 20: [{'$CT': 'CT'}], 22: [{'$ultrasound': 'ultrasound'}]}

        vectorization = vectorize_from_annotations(tokens=annotation, feature_types=[FeatureType.imaging_regex])
        expected_vectors = {0: [0, 0, 0, 0, 0, 0, 1, 0], 2: [0, 0, 0, 0, 0, 0, 1, 0], 4: [0, 0, 0, 0, 0, 0, 1, 0],
                            10: [0, 0, 0, 1, 0, 0, 0, 0], 12: [0, 0, 0, 1, 0, 0, 0, 0], 14: [0, 0, 0, 0, 0, 1, 0, 0],
                            6: [0, 1, 0, 0, 0, 0, 0, 0], 16: [0, 0, 1, 0, 0, 0, 0, 0], 18: [0, 0, 1, 0, 0, 0, 0, 0],
                            20: [1, 0, 0, 0, 0, 0, 0, 0], 22: [0, 0, 0, 0, 0, 0, 0, 1]}

        self.assertDictEqual(annotation[FeatureType.imaging_regex].to_dict(), expected_annotation)
        self.assertDictEqual(vectorization[FeatureType.imaging_regex].to_dict(), expected_vectors)