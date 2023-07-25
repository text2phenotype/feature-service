import unittest

from feature_service.feature_set.annotation import annotate_text
from feature_service.features.document_type import DocumentType

from text2phenotype.common import speech
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features.label_types import DocumentTypeLabel
from text2phenotype.constants.common import OCR_PAGE_SPLITTING_KEY

record_text = f"""Print header
Date: 2020-08-31
DOB: 2000-11-04
Patient Name: Jane Doe
{OCR_PAGE_SPLITTING_KEY[0]}
Pt. seen for follow up exam to lung cancer diagnosis
"""


class DocumentTypeTest(unittest.TestCase):
    def test_annotate_with_predictions(self):
        feature = DocumentType()

        annotations = feature.annotate(record_text)

        expected = [
            ((0, 69), [DocumentTypeLabel.other_clinical_doc.value.persistent_label]),
            ((70, 124), [DocumentTypeLabel.other_clinical_doc.value.persistent_label])
        ]

        self.assertListEqual(expected, annotations)

    def test_vectorize(self):
        feature = DocumentType()

        machine_annotation = annotate_text(record_text, {feature.feature_type})

        expected = {i: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(len(machine_annotation))}

        vectors = feature.vectorize(machine_annotation)

        self.assertDictEqual(expected, vectors)


if __name__ == '__main__':
    unittest.main()
