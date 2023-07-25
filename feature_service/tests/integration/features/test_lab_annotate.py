
from feature_service.features.lab import LabHepc, LabLoinc
from feature_service.tests.integration.features.annotate_tests import AnnotateTestsBase


class LabAnnotateTests(AnnotateTestsBase):
    def test_lab_annotate_hepc(self):

        target = LabHepc()

        actual = target.annotate(self.TEST_INPUT_CAROLYN)

        self.assertEqual(len(actual), 9)

        # these codes should exist
        self.assertTrue(self.lab_code_exists('77068002', actual))
        self.assertTrue(self.lab_code_exists('59573005', actual))
        self.assertTrue(self.lab_code_exists('84520', actual))

        # test attributes exist
        self.attributes_in_annotatino(actual)

    def test_lab_annotate_loinc(self):

        target = LabLoinc()

        actual = target.annotate(self.TEST_INPUT_CAROLYN)

        self.assertEqual(len(actual), 20)

        # these codes should exist
        self.assertTrue(self.lab_name_exists('Cholesterol', actual))
        self.assertTrue(self.lab_name_exists('Potassium', actual))
        self.assertTrue(self.lab_name_exists('hydrALAZINE', actual))
        self.assertTrue(self.lab_name_exists('Ibuprofen', actual))
        self.assertTrue(self.lab_name_exists('Blood', actual))
        self.assertTrue(self.lab_name_exists('Creatinine', actual))
        self.assertTrue(self.lab_name_exists('Age', actual))
        self.assertTrue(self.lab_name_exists('Diuretics', actual))
        # test attributes exist
        self.attributes_in_annotatino(actual)

    @classmethod
    def lab_code_exists(cls, lab_code: str, items: list) -> bool:
        return cls.lab_exists(lab_code, 'code', items)

    def attributes_in_annotatino(self, items: list):
        for item in items:
            dictionary = item[1][0]
            if 'Lab' in dictionary:
                self.assertIn('attributes', dictionary)

    @classmethod
    def lab_name_exists(cls, lab_name: str, items: list) -> bool:
        return cls.lab_exists(lab_name, 'preferredText', items)

    @staticmethod
    def lab_exists(lab_value: str, lab_key: str, items: list) -> bool:
        for item in items:
            dictionary = item[1][0]

            if 'Lab' in dictionary:
                if dictionary['Lab'][0][lab_key] == lab_value:
                    return True

        return False


if __name__ == '__main__':
    import unittest
    unittest.main()
