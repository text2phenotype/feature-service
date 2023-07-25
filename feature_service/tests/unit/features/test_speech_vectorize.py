import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.constants.features import FeatureType

from feature_service.constants import PartOfSpeechBin
from feature_service.features import Speech


class SpeechVectorizeTests(unittest.TestCase):

    def test_speech_vectorize_vector_length(self):
        """ Test Speech vector length """

        input_token = {'speech': ['UNKNOWN'], 'token': [1]}

        target = Speech()

        # verify length
        self.assertEqual(len(target.default_vector), len(PartOfSpeechBin.get_pos_bin_dict().keys()))

    def test_speech_vectorize_invalid_part_of_speech(self):
        """ Test Speech invalid part of speech """

        input_token = MachineAnnotation(json_dict_input={'speech': ['this is not valid'], 'token': [1]})

        target = Speech()

        actual = target.vectorize(input_token)

        self.assertFalse(0 in actual)


    def test_speech_vectorize_noun_flag(self):
        """ Test Speech noun flag """

        input_token = MachineAnnotation(json_dict_input={'speech': ['NN'], 'token': [1]})

        target = Speech()

        actual = target.vectorize(input_token)[0]

        pos_bin_lookup_keys_sorted = sorted(PartOfSpeechBin.get_pos_bin_dict().keys())

        # verify that the noun flag is set
        self.assertEqual(actual[pos_bin_lookup_keys_sorted.index('NN')], 1)

