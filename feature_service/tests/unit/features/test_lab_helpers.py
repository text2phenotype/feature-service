import unittest
from typing import List
from feature_service.feature_set import annotation, vectorization
from feature_service.features import LabValuePhrases, LabUnitProbable
from text2phenotype.constants.features import FeatureType


class TestLabUnit(unittest.TestCase):
    feature = LabUnitProbable()

    def assert_lab_value(self, input_text: str, lab_unit_tokens: List[str]):
        machine_annotation = annotation.annotate_text(input_text, feature_types=[FeatureType.lab_unit_probable])
        vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[FeatureType.lab_unit_probable])
        expected_idx = [i for i in range(len(machine_annotation)) if machine_annotation.tokens[i] in lab_unit_tokens]
        for idx in expected_idx:
            self.assertListEqual(vectors[FeatureType.lab_unit_probable, idx], [1])
        self.assertEqual(len(vectors[FeatureType.lab_unit_probable]), len(expected_idx))

    def test_lab_units(self):
        self.assert_lab_value('100 mg', ['mg'])
        self.assert_lab_value('Femtoliters.', ['Femtoliters'])
        self.assert_lab_value('Grams (g).', ['Grams', 'g'])
        self.assert_lab_value('Grams per deciliter (g/dL).', ['Grams', 'deciliter', 'g/dL'])
        self.assert_lab_value('Grams per liter (g/L).', ['Grams', 'liter', 'g/L'])
        self.assert_lab_value('International units per liter (IU/L).', ['units', 'IU/L', 'liter'])
        self.assert_lab_value('International units per milliliter (IU/mL).', ['units', 'IU/mL', 'milliliter'])
        self.assert_lab_value('Micrograms (mcg).', ['Micrograms', 'mcg'])
        self.assert_lab_value('Micrograms per deciliter (mcg/dL).', ['mcg/dL', 'Micrograms', 'deciliter'])
        self.assert_lab_value('Micrograms per liter (mcg/L).', ['Micrograms', 'liter', 'mcg/L'])
        self.assert_lab_value('Microkatals per liter (mckat/L).', ['mckat/L', 'liter'])
        self.assert_lab_value('Microliters (mcL).', ['Microliters'])
        self.assert_lab_value('Micromoles per liter (mcmol/L).', ['Micromoles', 'liter', 'mcmol/L'])
        self.assert_lab_value('Milliequivalents (mEq).', ['mEq', 'Milliequivalents'])
        self.assert_lab_value('Milliequivalents per liter (mEq/L).', ['liter', 'mEq/L', 'Milliequivalents'])
        self.assert_lab_value('Milligrams (mg).', ['Milligrams', 'mg'])
        self.assert_lab_value('Milligrams per deciliter (mg/dL).', ['Milligrams', 'deciliter', 'mg/dL'])
        self.assert_lab_value('Milligrams per liter (mg/L).', ['Milligrams', 'liter', 'mg/L'])
        self.assert_lab_value('Milli-international units per liter (mIU/L).', ['Milli-international','units', 'liter', 'mIU/L'])
        self.assert_lab_value('Milliliters (mL).', ['Milliliters', 'mL'])
        self.assert_lab_value('Millimeters (mm).', ['Millimeters', 'mm'])
        self.assert_lab_value('Millimeters of mercury (mm Hg).', ['Millimeters', 'mm'])
        self.assert_lab_value('Millimoles (mmol).', ['Millimoles', 'mmol'])
        self.assert_lab_value('Millimoles per liter (mmol/L).', ['Millimoles', 'liter', 'mmol/L'])
        self.assert_lab_value('Milliosmoles per kilogram of water (mOsm/kg water).',
                              ['Milliosmoles', 'kilogram', 'mOsm/kg'])
        self.assert_lab_value('Milliunits per gram (mU/g).', ['Milliunits', 'gram', 'mU/g'])
        self.assert_lab_value('Milliunits per liter (mU/L).', ['Milliunits', 'liter', 'mU/L'])
        self.assert_lab_value('Nanograms per deciliter (ng/dL).', ['Nanograms', 'deciliter', 'ng/dL', 'nanograms'])
        self.assert_lab_value('Nanograms per liter (ng/L).', ['Nanograms', 'liter', 'ng/L'])
        self.assert_lab_value('Nanograms per milliliter (ng/mL).', ['Nanograms', 'milliliter', 'ng/mL'])
        self.assert_lab_value('Nanograms per milliliter per hour (ng/mL/hr).',
                              ['Nanograms', 'milliliter', 'hr', 'ng/mL/hr'])
        self.assert_lab_value('Nanomoles (nmol).', ['Nanomoles', 'nmol'])
        self.assert_lab_value('Nanomoles per liter (nmol/L).', ['Nanomoles', 'liter', 'nmol/L'])
        self.assert_lab_value('Picograms (pg).', ['Picograms'])
        self.assert_lab_value('Picograms per milliliter (pg/mL).', ['Picograms', 'milliliter', 'pg/mL'])
        self.assert_lab_value('Picomoles per liter (pmol/L).', ['Picomoles', 'liter', 'pmol/L'])
        self.assert_lab_value('Units per liter (U/L).', ['Units', 'liter', 'U/L'])
        self.assert_lab_value('Units per milliliter (U/mL).', ['Units','milliliter', 'U/mL'])


class TestLabPhrases(unittest.TestCase):
    feature = LabValuePhrases()

    def assert_lab_phrase(self, input_text, expected_vectorization):
        machine_annotation = annotation.annotate_text(input_text,
                                                      feature_types=[FeatureType.lab_value_phrases])
        vectors = vectorization.vectorize_from_annotations(machine_annotation,
                                                           feature_types=[FeatureType.lab_value_phrases])

        for idx in expected_vectorization:
            self.assertListEqual(vectors[FeatureType.lab_value_phrases, idx], expected_vectorization[idx])
        self.assertEqual(len(vectors[FeatureType.lab_value_phrases]), len(expected_vectorization))

    def test_lab_phrase(self):
        self.assert_lab_phrase('WBC results inconclusive', [])
        self.assert_lab_phrase('Flu Swab: negative', {3: [0, 0, 0, 1, 0, 0], 1: [1, 0, 0, 0, 0, 0]})
        self.assert_lab_phrase('Gene panel: reactive',  {3: [0, 0, 0, 0, 0, 1], 1: [1, 0, 0, 0, 0, 0]})

