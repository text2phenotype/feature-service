import unittest

from text2phenotype.common.featureset_annotations import MachineAnnotation
from feature_service.features import SpeechBin
from text2phenotype.common.speech import PartOfSpeechBin


class SpeechBinVectorizeTests(unittest.TestCase):
    def test_speech_bin_vectorize_vector_length(self):
        """ Test SpeechBin vector length """

        input_token = MachineAnnotation(json_dict_input={'speech': ['SYM'], 'token': [1]})

        target = SpeechBin()

        actual = target.vectorize(input_token)[0]

        # verify length
        self.assertEqual(len(actual), len(PartOfSpeechBin.__members__))

    def test_speech_bin_vectorize_fw_symb_flag(self):
        """ Test SpeechBin FW_Symb flag """

        input_token = MachineAnnotation(json_dict_input={'speech': ['FW'], 'token': [1]})

        target = SpeechBin()

        actual = target.vectorize(input_token)[0]

        # verify FW_Symb is set
        self.assertEqual(actual[list(PartOfSpeechBin.__members__.keys()).index("FW_Symb")], 1)

    def test_speech_bin_vectorize_com_dep_wd_flag(self):
        """ Test SpeechBin com_dep_wd flag """

        input_token = MachineAnnotation(json_dict_input={'speech': ['CC'], 'token': [1]})

        target = SpeechBin()

        actual = target.vectorize(input_token)[0]

        # verify FW_Symb is set
        self.assertEqual(actual[list(PartOfSpeechBin.__members__.keys()).index("com_dep_wd")], 1)
