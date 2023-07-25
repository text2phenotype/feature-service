import unittest

from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.annotation import annotate_text


REGEX_BP = '$BLOOD_PRESSURE_CHART'


class TestBiomed64(unittest.TestCase):

    def assertBloodPressure(self, text, bp_value, expected=True):
        """
        :param text: clinical text containing BP
        :param bp_value: expected token containing BP
        :param expected: True/False do you expect a match for the BP reading
        """
        found = False
        machine_annotation = annotate_text(text, feature_types=[FeatureType.blood_pressure])
        for t in range(len(machine_annotation.tokens)):
            if machine_annotation.tokens[t] == bp_value:
                if machine_annotation[FeatureType.blood_pressure.name, t]:
                    for match in machine_annotation[FeatureType.blood_pressure.name, t]:
                        if REGEX_BP in match.keys():
                            if match[REGEX_BP].strip() == bp_value:
                                found = True

        self.assertEqual(found, expected)

    def test_regex_blood_pressure(self):
        self.assertBloodPressure('Blood Pressure 150/70 ', '150/70')
        self.assertBloodPressure('Blood Pressure 100/40 ', '100/40')
        self.assertBloodPressure('Blood Pressure was taken on 11/20', '11/20', False)

    def test_biomed_274_hytest_biomed_274_hypotension(self):
        self.assertBloodPressure('Blood Pressure 98/40 ', '98/40')
