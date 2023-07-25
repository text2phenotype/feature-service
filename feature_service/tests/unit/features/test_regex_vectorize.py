import unittest
from feature_service.features.regex import DateRegEx, AllergyRegex
from text2phenotype.common.featureset_annotations import MachineAnnotation


class RegExVectorizeTests(unittest.TestCase):

    def test_date_regex_vectorize_vector_length(self):
        """ Test DateRegEx vector length and last flag """

        input_token = MachineAnnotation(json_dict_input={'regex_dates': {0:[
            {
               '$DATE1': '7/21/2017'
            }]},'token': ['a']})

        target = DateRegEx()

        actual = target.vectorize(input_token)[0]

        # verify length
        self.assertEqual(len(actual), len(target.rules.keys()) + target.extra_feature_count)
        # last flag should be set for dates
        self.assertEqual(actual[-1], 1)

    def test_date_regex_vectorize_invalid_token(self):
        """ Test DateRegEx vector length and last flag """

        target = DateRegEx()

        actual = target.vectorize(self.no_response_token)

        # last flag should not be set
        self.assertFalse(0 in actual)

    def test_date_regex_vectorize_date2_format(self):
        """ Test DateRegEx vector length and last flag """

        input_token = MachineAnnotation(json_dict_input={'regex_dates': {0:[
            {
               '$DATE2': '7/21'
            }]},'token': ['a']})

        target = DateRegEx()

        actual = target.vectorize(input_token)[0]

        rules_list = sorted(target.rules.keys())
        index = rules_list.index('$DATE2')

        # verify flag is set
        self.assertEqual(actual[index], 1)

    def test_allergy_regex(self):
        input_token = MachineAnnotation(json_dict_input={'allergy_regex': {0:[{'$ALLERG':'Allerg'}]}, 'token':['Allergy']})
        target = AllergyRegex()
        actual = target.vectorize(input_token)[0]
        self.assertListEqual(actual, [1, 0])

    def test_allergy_no_response(self):
        target = AllergyRegex()
        actual = target.vectorize(self.no_response_token)
        self.assertFalse(0 in actual)

    no_response_token = MachineAnnotation(json_dict_input={'token': ['Hello']})
