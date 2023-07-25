import unittest

from feature_service.features import I2B2, CCDA, MTSample, MRConSo, NPICity, NPIAddress, NPIPhone, PatientFirstName, \
    PatientLastName, NPIFirstName, NPILastName, Cities, States, Disorder, Finding, Procedure
from text2phenotype.common.featureset_annotations import MachineAnnotation


class TermFrequencyVectorizeTests(unittest.TestCase):

    # I2B2
    def test_tf_i2b2_vectorize_vector_length(self):
        """ Test I2B2 vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = I2B2()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 11, "TF I2B2 vector length is not 11")

    def test_tf_i2b2_vectorize_search_hit_in_corpus(self):
        """ Test I2B2 search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['Record']})

        target = I2B2()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[10], 1, "TF I2B2 vector position [10] was not set")

    def test_tf_i2b2_vectorize_search_no_hit_in_corpus(self):
        """ Test I2B2 search no hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['not found term']})

        target = I2B2()

        actual = target.vectorize(input_token, feature_name='token')

        # verify length
        self.assertFalse(0 in actual)

    def test_tf_ccda_vectorize_vector_length(self):
        """ Test CCDA vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = CCDA()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 11, "TF CCDA vector length is not 11")

    def test_tf_ccda_vectorize_search_hit_in_corpus(self):
        """ Test CCDA search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['Diagnostic']})

        target = CCDA()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[2], 1, "TF CCDA vector position [2] was not set for found term 'Diagnostic'")

    def test_tf_ccda_vectorize_search_no_hit_in_corpus(self):
        """ Test CCDA search no hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['not found term']})

        target = CCDA()

        actual = target.vectorize(input_token)

        # verify length
        self.assertFalse(0 in actual)

    # MTSample

    def test_tf_mtsample_vectorize_vector_length(self):
        """ Test MTSample vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = MTSample()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 11, "TF MTSample vector length is not 11")

    def test_tf_mtsample_vectorize_search_hit_in_corpus(self):
        """ Test MTSample search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['problems']})

        target = MTSample()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[5], 1, "TF MTSample vector position [5] was not set for found term 'problems'")

    def test_tf_mtsample_vectorize_search_no_hit_in_corpus(self):
        """ Test MTSample search no hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['not found term']})

        target = MTSample()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_mrconso_vectorize_vector_length(self):
        """ Test MRConSo vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['problems']})

        target = MRConSo()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 11, "TF MRConSo vector length is not 11")

    def test_tf_mrconso_vectorize_search_hit_in_corpus(self):
        """ Test MRConSo search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['problems']})

        target = MRConSo()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[1], 1, "TF MRConSo vector position [1] was not set for found term 'problems'")

    def test_tf_mrconso_vectorize_search_no_hit_in_corpus(self):
        """ Test MRConSo search no hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['not found term']})

        target = MRConSo()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_npicity_vectorize_vector_length(self):
        """ Test NPICity vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = NPICity()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_npicity_vectorize_search_hit_in_corpus(self):
        """ Test NPICity search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['BEACH']})

        target = NPICity()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF NPICity vector position [0] was not set for found term 'BEACH'")

    def test_tf_npicity_vectorize_search_no_hit_in_corpus(self):
        """ Test NPICity search no hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['not found term']})

        target = NPICity()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_npiaddress_vectorize_vector_length(self):
        """ Test NPIAddress vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = NPIAddress()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 1,
                         "TF NPIAddress vector length is not 1.  Vectorize uses feature_tf_corpus_binary. ")

    def test_tf_npiaddress_vectorize_search_hit_in_corpus(self):
        """ Test NPIAddress search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['SUITE']})

        target = NPIAddress()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF NPIAddress vector position [0] was not set for found term 'SUITE'")

    def test_tf_npiaddress_vectorize_search_no_hit_in_corpus(self):
        """ Test NPIAddress search no hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['not found term']})

        target = NPIAddress()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_npiphone_vectorize_vector_length(self):
        """ Test NPIPhone vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['2167850922']})

        target = NPIPhone()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 1,
                         "TF NPIPhone vector length is not 1.  Vectorize uses feature_tf_corpus_binary. ")

    def test_tf_npiphone_vectorize_search_hit_in_corpus(self):
        """ Test NPIPhone search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['2167850922']})

        target = NPIPhone()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF NPIPhone vector position [0] was not set for found term '2167850922'")

    def test_tf_npiphone_vectorize_search_no_hit_in_corpus(self):
        """ Test NPIPhone search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = NPIPhone()

        actual = target.vectorize(input_token, feature_name='token')
        self.assertFalse(0 in actual)

    def test_tf_patient_first_name_vectorize_vector_length(self):
        """ Test PatientFirstName vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = PatientFirstName()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_patient_first_name_vectorize_search_hit_in_corpus(self):
        """ Test PatientFirstName search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['SYLVESTER']})

        target = PatientFirstName()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF PatientFirstName vector position [0] was not set for found term 'SYLVESTER'")

    def test_tf_patient_first_name_vectorize_search_no_hit_in_corpus(self):
        """ Test PatientFirstName search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = PatientFirstName()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)


    def test_tf_patient_last_name_vectorize_vector_length(self):
        """ Test PatientLastName vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = PatientLastName()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 1,
                         "TF PatientLastName vector length is not 1.  Vectorize uses feature_tf_corpus_binary. ")

    def test_tf_patient_last_name_vectorize_search_hit_in_corpus(self):
        """ Test PatientLastName search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['STEVENS']})

        target = PatientLastName()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF PatientLastName vector position [0] was not set for found term 'STEVENS'")

    def test_tf_patient_last_name_vectorize_search_no_hit_in_corpus(self):
        """ Test PatientLastName search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = PatientLastName()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_npi_first_name_vectorize_vector_length(self):
        """ Test NPIFirstName vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = NPIFirstName()

        actual = target.vectorize(input_token, feature_name='token')

        # verify length
        self.assertFalse(0 in actual)

    def test_tf_npi_first_name_vectorize_search_hit_in_corpus(self):
        """ Test NPIFirstName search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['JENNIFER']})

        target = NPIFirstName()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF NPIFirstName vector position [0] was not set for found term 'STEVENS'")

    def test_tf_npi_first_name_vectorize_search_no_hit_in_corpus(self):
        """ Test NPIFirstName search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = NPIFirstName()

        actual = target.vectorize(input_token, feature_name='token')

        # verify item does not exist
        self.assertFalse(0 in actual)

    def test_tf_npi_last_name_vectorize_vector_length(self):
        """ Test NPILastName vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = NPILastName()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify length
        self.assertEqual(len(actual), 1,
                         "TF NPILastName vector length is not 1.  Vectorize uses feature_tf_corpus_binary. ")

    def test_tf_npi_last_name_vectorize_search_hit_in_corpus(self):
        """ Test NPILastName search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['SMITH']})

        target = NPILastName()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF NPILastName vector position [0] was not set for found term 'SMITH'")

    def test_tf_npi_last_name_vectorize_search_no_hit_in_corpus(self):
        """ Test NPILastName search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = NPILastName()

        actual = target.vectorize(input_token, feature_name='token')

        # verify item does not exist
        self.assertFalse(0 in actual)

    def test_tf_cities_vectorize_vector_length(self):
        """ Test Cities vector length """

        input_token = MachineAnnotation(json_dict_input={'token': ['test']})

        target = Cities()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_cities_vectorize_search_hit_in_corpus(self):
        """ Test Cities search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['HOUSTON']})

        target = Cities()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF Cities vector position [0] was not set for found term 'HOUSTON'")

    def test_tf_cities_vectorize_search_no_hit_in_corpus(self):
        """ Test Cities search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = Cities()

        actual = target.vectorize(input_token, feature_name='token')
        self.assertFalse(0 in actual)

    def test_tf_states_vectorize_search_hit_in_corpus(self):
        """ Test States search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['FL']})

        target = States()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF States vector position [0] was not set for found term 'FL'")

    def test_tf_states_vectorize_search_no_hit_in_corpus(self):
        """ Test States search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = States()

        actual = target.vectorize(input_token, feature_name='token')

        # verify item does not exist
        self.assertFalse(0 in actual)

    def test_tf_disorder_vectorize_vector_length(self):
        """ Test Disorder vector length """

        input_token = MachineAnnotation(json_dict_input={'token': 'test'})

        target = Disorder()

        actual = target.vectorize(input_token, feature_name='token')

        self.assertFalse(0 in actual)

    def test_tf_disorder_vectorize_search_hit_in_corpus(self):
        """ Test Disorder search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['CHRONIC']})

        target = Disorder()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF Disorder vector position [0] was not set for found term 'CHRONIC'")

    def test_tf_disorder_vectorize_search_no_hit_in_corpus(self):
        """ Test Disorder search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = Disorder()

        actual = target.vectorize(input_token, feature_name='token')

        # verify item does not exist
        self.assertFalse(0 in actual)

    def test_tf_finding_vectorize_vector_length(self):
        """ Test Finding vector length """

        input_token = MachineAnnotation(json_dict_input={'token': 'test'})

        target = Finding()

        actual = target.vectorize(input_token, feature_name='token')

        # verify length
        self.assertFalse(0 in actual)

    def test_tf_finding_vectorize_search_hit_in_corpus(self):
        """ Test Finding search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['LEG']})

        target = Finding()

        actual = target.vectorize(input_token, feature_name='token')[0]

        # verify item exists
        self.assertEqual(actual[0], 1, "TF Finding vector position [0] was not set for found term 'LEG'")

    def test_tf_finding_vectorize_search_no_hit_in_corpus(self):
        """ Test Finding search no hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['not found term']})

        target = Finding()

        actual = target.vectorize(input_token, feature_name='token')

        # verify item does not exist
        self.assertFalse(0 in actual)

    def test_tf_procedure_vectorize_vector_length(self):
        """ Test Procedure vector length """

        input_token = MachineAnnotation(json_dict_input={'token': 'test'})

        target = Procedure()

        actual = target.vectorize(input_token, feature_name='token')
        self.assertFalse(0 in actual)


    def test_tf_procedure_vectorize_search_hit_in_corpus(self):
        """ Test Procedure search hit """

        input_token = MachineAnnotation(json_dict_input={'token': ['TRANSPLANT']})

        target = Procedure()

        actual = target.vectorize(input_token, feature_name='token')[0]
        # verify item exists
        self.assertEqual(actual[0], 1, "TF Procedure vector position [0] was not set for found term 'TRANSPLANT'")

    def test_tf_procedure_vectorize_search_no_hit_in_corpus(self):
        """ Test Procedure search no hit """

        input_token = MachineAnnotation(json_dict_input={'token':['not found term']})

        target = Procedure()

        actual = target.vectorize(input_token, feature_name='token')
        self.assertFalse(0 in actual)

