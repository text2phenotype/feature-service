from multiprocessing import Lock
import unittest

from feature_service.feature_set.annotation import annotate_text
from feature_service.features.loinc import LoincSectionAttributes, LoincSectionDocTypes

from text2phenotype.common.featureset_annotations import Vectorization, DocumentTypeAnnotation
from text2phenotype.constants.features import DocumentTypeLabel


class __LoincTestBase(unittest.TestCase):
    text = """Admit: 1/1/2020
Chief complaint: SOB
"""

    def _test(self, feature, expected):
        annotations = DocumentTypeAnnotation(annotate_text(self.text, {feature.feature_type}))

        v = Vectorization()
        feature.get_vectorization_workers(annotations, v, Lock())[0].run()

        self.assertListEqual(expected, v.output_dict[feature.feature_type][0])


class LoincSectionAttributesTest(__LoincTestBase):
    def test_vectorize(self):
        expected = [0, 0,
                    # ('match', {'strict': 0, 'abbr': 1, 'pref': 2, 'relax': 3}),
                    1, 0, 0, 0,
                    # ('impress', {'interpret': 0, 'first': 1, 'conclude': 2, 'notable': 3, 'ignore': 4, 'second': 5}),
                    0, 0, 0, 0, 0, 0,
                    # ('when', {'admit': 0, 'history': 1, 'present': 2, 'plan': 3, 'discharge': 4, 'transfer': 5}),
                    1, 0, 0, 0, 0, 0,
                    # ('who', {'patient': 0, 'family': 1, 'provider': 2, 'insurance': 3}),
                    1, 0, 0, 0,
                    # ('rank', {'high': 0, 'ignore': 1, 'first': 2, 'second': 3, 'low': 4}),
                    1, 0, 0, 0, 0,
                    # ('style', {'narrative': 0, 'subhead': 1, 'lists': 2, 'printer': 3, 'choice': 4, 'legal': 5, 'calendar': 6, 'unique': 7}),
                    0, 0, 0, 0, 0, 0, 0, 0,
                    # ('visit', {'encounter': 0, 'social': 1, 'demographics': 2}),
                    0, 0, 0,
                    # ('where', {'hosp': 0, 'home': 1, 'outpatient': 2, 'surgery': 3, 'consult': 4, 'department': 5, 'radiology': 6, 'pathology': 7, 'emergency': 8, 'clinic': 9}),
                    1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    # ('instruct', {'care': 0, 'cover': 1}),
                    0, 0,
                    # ('drug', {'med': 0, 'immunization': 1, 'allergy': 2}),
                    0, 0, 0,
                    # ('measure', {'finding': 0, 'lab': 1, 'imaging': 2, 'objective': 3, 'vital': 4}),
                    0, 0, 0, 0, 0,
                    # ('why', {'complaint': 0, 'indication': 1, 'reason': 2}),
                    1, 0, 0,
                    # ('exam', {'physical': 0, 'ros': 1}),
                    0, 0,
                    # ('problem', {'symptom': 0, 'problem': 1, 'diagnosis': 2}),
                    1, 0, 0,
                    # ('procedure', {'operate': 0, 'procedure': 1, 'device': 2})
                    0, 0, 0]

        self._test(LoincSectionAttributes(), expected)


class LoincSectionDocTypesTest(__LoincTestBase):
    def test_vectorize(self):
        feature = LoincSectionDocTypes()

        expected = [0] * feature.vector_length
        expected[DocumentTypeLabel.progress_notes.value.column_index - 1] = 1
        expected[DocumentTypeLabel.history_and_physical.value.column_index - 1] = 1
        expected[DocumentTypeLabel.procedure_note.value.column_index - 1] = 1
        expected[DocumentTypeLabel.consult_note.value.column_index - 1] = 1
        expected[DocumentTypeLabel.discharge_summary.value.column_index - 1] = 1

        self._test(feature, expected)


if __name__ == '__main__':
    unittest.main()
