import unittest
import datetime
from typing import Dict

from text2phenotype.common.dates import parse_dates
from text2phenotype.entity.attributes import DocumentAttributes, Attributes
from text2phenotype.entity.results import ResultType, Result
from text2phenotype.entity.concept import ConceptList
from feature_service.nlp.nlp_reader import DrugReader, ClinicalReader, LabReader
from text2phenotype.entity.entity import LabEntity

from feature_service.nlp import autocode


class TestBiomed471(unittest.TestCase):

    ###############################################################################
    #
    # DocMeta
    #
    # cTAKES CAS Types (Common Annotation System)
    #
    ###############################################################################

    def assertDocMeta(self, res: Dict):
        """
        Assert the DocMeta has some minimal meta information
        :param res: cTAKES autocoder response
        """
        meta = DocumentAttributes(res)
        self.assertLess(0, len(parse_dates(meta.date)))
        self.assertIn('BIOMED/versions/', meta.jira)

    def test_docmeta(self):
        text = 'heart attack'
        self.assertDocMeta(autocode.clinical(text))
        self.assertDocMeta(autocode.lab_value(text))
        self.assertDocMeta(autocode.drug_ner(text))
        self.assertDocMeta(autocode.smoking(text))
        self.assertDocMeta(autocode.temporal(text))

    def assertDocMetaDOB(self, text, expected):
        """
        :param text: 'DOB: 01/02/1993'
        :param expected: '01/02/1993'
        """
        meta = DocumentAttributes(autocode.clinical(text))
        self.assertEqual(expected, meta.dob)

    def test_docmeta_dob_date_of_birth(self):
        """
        Test DOB
        """
        self.assertDocMetaDOB('DOB: 01/02/1993', '01/02/1993')
        self.assertDocMetaDOB('BIRTH: 01/02/1993', '01/02/1993')
        self.assertDocMetaDOB('DATE OF BIRTH: 01/02/1993', '01/02/1993')

    def test_docmeta_serialiable(self):
        res = autocode.clinical('heart attack')

        del res['result']

        meta = DocumentAttributes(res)

        self.assertEqual(res, meta.to_json())

    ###############################################################################
    #
    # Attributes
    #
    ###############################################################################
    def assertAttributesPolarity(self, result: Dict, polarity='positive'):
        attr = Attributes(result.get('attributes'))
        self.assertEqual(attr.polarity, polarity)

    def test_attributes_polarity_positive(self):
        text = 'heart attack'
        positive = 'positive'

        for result in autocode.clinical(text).get(ResultType.clinical):
            self.assertAttributesPolarity(result, positive)

        for result in autocode.lab_value(text).get(ResultType.lab_value):
            self.assertAttributesPolarity(result, positive)

        # for result in ctakes.drug_ner(text).get(ResultType.drug_ner):
        #    self.assertAttributesPolarity(result, positive)

        for result in autocode.hepc_clinical(text).get(ResultType.clinical):
            self.assertAttributesPolarity(result, positive)

        for result in autocode.hepc_lab_value(text).get(ResultType.lab_value):
            self.assertAttributesPolarity(result, positive)

        for result in autocode.hepc_drug_ner(text).get(ResultType.drug_ner):
            self.assertAttributesPolarity(result, positive)

    def test_attributes_polarity_negative(self):
        text = 'No evidence of COPD'
        negative = 'negative'
        positive = 'positive'

        for result in autocode.clinical(text).get(ResultType.clinical):
            exp_polarity = negative if result['text'][0] == 'COPD' else positive

            self.assertAttributesPolarity(result, exp_polarity)

        for result in autocode.lab_value(text).get(ResultType.lab_value):
            self.assertAttributesPolarity(result, negative)

        # TODO: JIRA/BIOMED-968
        # for result in ctakes.drug_ner(text).get(ResultType.drug_ner):
        #    self.assertAttributesPolarity(result, negative)

        for result in autocode.hepc_clinical(text).get(ResultType.clinical):
            self.assertAttributesPolarity(result, negative)

        for result in autocode.hepc_lab_value(text).get(ResultType.lab_value):
            self.assertAttributesPolarity(result, negative)

        for result in autocode.hepc_drug_ner(text).get(ResultType.drug_ner):
            self.assertAttributesPolarity(result, negative)

    def test_attributes_polarity_serializable(self):
        text = 'heart attack'
        autocode_res = autocode.clinical(text).get(ResultType.clinical)

        self.assertTrue(len(autocode_res) > 0)

        for result in autocode_res:
            expected = result['attributes']
            actual = Attributes(expected).to_json()
            self.assertEqual(expected, actual, f"attributes did not match {expected} VS {actual} ")

    ###############################################################################
    #
    # clinical
    #
    ###############################################################################
    def test_clinical_reader(self):
        expected = autocode.clinical('heart attack')
        actual = ClinicalReader(expected).to_json()
        self.assertEqual(expected, actual, f"result did not match {actual}")

    def test_clinical_result_serializable(self):
        for result in autocode.clinical('heart attack').get(ResultType.clinical):
            actual = Result(result)
            self.assertEqual(result, actual.to_json(), f"result did not match {actual.to_json()}")

    ###############################################################################
    #
    # drug_ner
    #
    ###############################################################################
    def test_drugner_reader(self):

        expected = autocode.drug_ner('Aspirin 50 mg')
        actual = DrugReader(expected).to_json()

        self.assertEqual(expected, actual, f"result did not match {actual}")

    @unittest.skip('JIRA/BIOMED-968')
    def test_biomed_968_medication_polarity(self):
        for result in autocode.drug_ner('patient is NOT taking aspirin').get(ResultType.drug_ner):
            self.assertAttributesPolarity(result, 'negative')

    ###############################################################################
    #
    # lab_value
    #
    ###############################################################################
    def test_lab_value_reader(self):

        expected = autocode.lab_value('Hemoglobin A1c 5%')
        actual = LabReader(expected).to_json()

        self.assertEqual(expected, actual, f"result did not match {actual}")

    def test_equality_concept_list(self):
        expected = [{'code': 'C64849', 'codingScheme': 'NCI',
                     'cui': 'C0202054', 'preferredText': 'Glucohemoglobin measurement', 'tui': None},
                    {'code': '40402000', 'codingScheme': 'SNOMEDCT_US',
                     'cui': 'C0202054', 'preferredText': 'Glucohemoglobin measurement', 'tui': None}]

        c1 = ConceptList(expected)
        c2 = ConceptList(expected)

        self.assertEqual(c1, c2, f"not equal {c1.to_json()} != {c2.to_json()}")

    def test_equality_lab_entity(self):

        foo = LabEntity(text='HBA1C', polarity='positive')
        bar = LabEntity(text='HBA1C', polarity='positive')

        self.assertEqual(foo, bar)

        foo = LabEntity(text='HBA1C', value='9.0', units='%')
        bar = LabEntity(text='HBA1C', value='9.0', units='%')

        self.assertEqual(foo, bar)
