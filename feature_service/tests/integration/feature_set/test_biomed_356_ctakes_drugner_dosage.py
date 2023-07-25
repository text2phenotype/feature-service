import unittest

from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.annotation import annotate_text


class TestMedDosage(unittest.TestCase):

    def assertMedDosage(self, text, dosage_term, expected=True):
        """
        this is the assert that the dosage is correctly caught from Ctakes into the featureset annotation
        :param text: clinical text
        :param dosage_term: expected token for dosage
        :param expected: True/False whether this token in this text is a dosage or not
        :return:
        """
        found = False
        machine_annotation = annotate_text(text, feature_types=[FeatureType.drug_rxnorm])
        for t in range(len(machine_annotation)):
            if machine_annotation.tokens[t] == dosage_term:
                annotation = machine_annotation['drug_rxnorm', t]
                if annotation is not None:
                    for i in annotation:
                        if i and 'medDosage' in i:
                            found = True
        self.assertEqual(found, expected)

    # JIRA/BIOMED-356
    def test_biomed_356(self):
        self.assertMedDosage('aspirin 20 mg twice a day', '20')
        self.assertMedDosage('the patient weight 180 pound', '180', False)
        self.assertMedDosage('aspirin 1,360 gram', '1,')
        self.assertMedDosage('aspirin 1,360 gram', '360')
