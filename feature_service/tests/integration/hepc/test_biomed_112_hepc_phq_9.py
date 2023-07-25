import unittest

from feature_service.nlp.nlp_reader import HepcLabReader


class TestBiomed112(unittest.TestCase):

    def test_hepc_phq_patient_health_questions_number_9(self):

        reader = HepcLabReader('PHQ-9 interpretation 16')

        first = reader.first_lab()

        self.assertEqual('PHQ-9 interpretation', first.text)
        self.assertEqual(16, int(first.value))
        self.assertEqual(None, first.units)
