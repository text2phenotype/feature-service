import unittest

from text2phenotype.constants.features import FeatureType

from feature_service.feature_set.annotation import annotate_text
from feature_service.features.form import Form


class TestForm(unittest.TestCase):
    def test_vectorize(self):
        form = Form()
        text = 'Pt has history of seizures.  Tested positive for HIV.'
        machine_annotation = annotate_text(text, feature_types=[FeatureType.form])

        na_vector = [1] + ([0] * 49)
        actual = form.vectorize(machine_annotation)
        for i in range(len(machine_annotation)):
            if machine_annotation.tokens[i] == 'seizures':
                exp_vector = [0] * 50
                exp_vector[20] = 1
            elif machine_annotation.tokens[i] == 'HIV':
                exp_vector = [0] * 50
                exp_vector[16] = 1
            else:
                exp_vector = na_vector
            if i in actual:
                self.assertEqual(exp_vector, actual[i])
            else:
                self.assertEqual(exp_vector, form.default_vector)
