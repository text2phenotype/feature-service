from unittest import TestCase, skip

from feature_service.document_type_vocab.document_type_vocab import DocumentTypeVocab
from text2phenotype.constants.features.label_types import DocumentTypeLabel


@skip
class TestBiomed1158(TestCase):

    def test_biomed_1158(self):
        """
        this test serve is just a baseline test of document type model prediction
        """
        test_text = """
            TITLE:  Case Management Assessment
            The patient is an 38 year-old gentleman with a past medical history of
            CVA-I and resultant syndrome, recurrent aspiration PNA and
            UTIs who presented with fever, tachypnea, abdominal distension and
            suspected aspiration event.
            The patient is a long-term care resident at BRRHI.  He is on a
            10-day Medicaid
            Please call/page anytime for case management needs.
            Michael May, RN, BSN
            MICU Service Case Manager
            Phone:  2-17925/7-09306
            Page:  Room 45387
            """
        nn_dc = DocumentTypeVocab()
        result = nn_dc.predict(test_text)
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result.get('doc_type'), DocumentTypeLabel.case_management)
        self.assertTrue(isinstance(result.get('score'), float))
