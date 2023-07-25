import unittest

from text2phenotype.ccda.section import (
    Aspect,
    Person,
    RelTime,
)
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.constants import (
    HeaderStyle,
    SectionizerPattern,
)
from feature_service.feature_set.annotation import annotate_text
from feature_service.features import Sectionizer


class SectionizerVectorizeTests(unittest.TestCase):
    TEST_TEXT = "DIAGNOSIS: \n PATIENT NAME:"
    expected_annotation = MachineAnnotation(json_dict_input={'sectionizer': {0: [{'HEADER_COLON': {'match': ['DIAGNOSIS', 0, 9], 'section': {'header': 'DIAGNOSIS', 'aspect': 'Aspect.diagnosis', 'style': 'StyleType.narrative', 'person': 'Person.patient', 'reltime': 'RelTime.present', 'doctype': [None], 'loinc': []}}}], 2: [{'HEADER_COLON': {'match': [' PATIENT NAME', 12, 25], 'section': {'header': 'PATIENT NAME', 'aspect': 'Aspect.demographics', 'style': 'StyleType.unique', 'person': 'Person.patient', 'reltime': 'RelTime.present', 'doctype': [None], 'loinc': []}}}], 3: [{'HEADER_COLON': {'match': [' PATIENT NAME', 12, 25], 'section': {'header': 'PATIENT NAME', 'aspect': 'Aspect.demographics', 'style': 'StyleType.unique', 'person': 'Person.patient', 'reltime': 'RelTime.present', 'doctype': [None], 'loinc': []}}}]}, 'token': ['DIAGNOSIS', ':', 'PATIENT', 'NAME', ':'], 'len': [9, 1, 7, 4, 1], 'speech': ['NN', ':', 'JJ', 'NN', ':'], 'speech_bin': ['Nouns', 'unknown', 'Adjectives', 'Nouns', 'unknown'], 'range': [[0, 9], [9, 10], [13, 20], [21, 25], [25, 26]]})

    def test_sectionizer_annotate(self):
        actual = annotate_text(self.TEST_TEXT, feature_types=[FeatureType.sectionizer])

        self.assertEqual(actual[FeatureType.sectionizer].to_dict(), self.expected_annotation[FeatureType.sectionizer.name].to_dict())

    def test_sectionizer_vectorize_vector_length(self):
        """ Test Sectionizer vector length """
        target = Sectionizer()

        actual = target.vectorize(self.expected_annotation)

        expected_vector_length = 1 + len(SectionizerPattern.__members__) + \
                                 len(HeaderStyle.__members__) + \
                                 len(Person.__members__) + \
                                 len(RelTime.__members__) + \
                                 len(Aspect.get_active_aspects())

        # verify length
        self.assertEqual(len(actual[0]), expected_vector_length)
        # first flag should be set header loinc_title
        self.assertEqual(actual[0][1 + SectionizerPattern['HEADER_COLON'].value], 1)
        # aspect encounter flag should be set in above test data
        self.assertEqual(actual[0][1 + len(SectionizerPattern.__members__) +
                                len(HeaderStyle.__members__) +
                                len(Person.__members__) +
                                len(RelTime.__members__) +
                                Aspect.diagnosis.value], 1)
        self.assertEqual(actual[0][1 + len(SectionizerPattern.__members__) + HeaderStyle.narrative.value], 1) # check header style gets flagged

        # test patient
        self.assertEqual(actual[0][1 + len(SectionizerPattern.__members__) +
                                len(HeaderStyle.__members__) +
                                Person.patient.value], 1)
        self.assertEqual(actual[0][1 + len(SectionizerPattern.__members__) +
                                len(HeaderStyle.__members__) +
                                len(Person.__members__) +
                                RelTime.present.value], 1)

    def test_sectionizer_vectorize_invalid_token(self):
        """ Test Sectionizer invalid token """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = Sectionizer()

        actual = target.vectorize(input_token)

        self.assertFalse(0 in actual)
