import unittest

from feature_service.features import LoincTitle

class TestLoincSectionVectorize(unittest.TestCase):

    EXAMPLE_TOKEN_ANNOTATION = [{'attributes': {'polarity': 'positive', 'relTime': ''},
            'umlsConcept': [{'code': '34745-0',
            'cui': 'C0801840',
            'preferredText': 'Physician Hospital Discharge summary',
            'codingScheme': 'LNC',
            'tty': 'strict',
            'tui': 'T102'},
            {'code': '28655-9',
            'cui': 'C0801840',
            'preferredText': 'Physician Hospital Discharge summary',
            'codingScheme': 'LNC',
            'tty': 'strict',
            'tui': 'T102'},
            {'code': '11490-0',
            'cui': 'C0801840',
            'preferredText': 'Physician Hospital Discharge summary',
            'codingScheme': 'LNC',
            'tty': 'strict',
            'tui': 'T102'},
            {'code': '18842-5',
            'cui': 'C0801840',
            'preferredText': 'Physician Hospital Discharge summary',
            'codingScheme': 'LNC',
            'tty': 'strict',
            'tui': 'T102'},
            {'code': '34106-5',
            'cui': 'C0801840',
            'preferredText': 'Physician Hospital Discharge summary',
            'codingScheme': 'LNC',
            'tty': 'strict',
            'tui': 'T102'},
            {'code': '34105-7',
            'cui': 'C0801840',
            'preferredText': 'Physician Hospital Discharge summary',
            'codingScheme': 'LNC',
            'tty': 'strict',
            'tui': 'T102'},
            {'code': '29761-4',
            'cui': 'C0801840',
            'preferredText': 'Physician Hospital Discharge summary',
            'codingScheme': 'LNC',
            'tty': 'strict',
            'tui': 'T102'}]}]

    expected_vector = [1]

    def test_loinc_section_vectorize(self):

        feature = LoincTitle()

        actual_vector = feature.vectorize_token(self.EXAMPLE_TOKEN_ANNOTATION)

        self.assertListEqual(actual_vector, self.expected_vector)




