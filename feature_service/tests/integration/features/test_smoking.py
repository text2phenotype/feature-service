from typing import List
import unittest

from text2phenotype.constants.features import FeatureType

from feature_service.feature_set import annotation, vectorization
from feature_service.feature_set.annotation import annotate_text
from feature_service.features.smoking import Smoking, SmokingStatus, SmokingKeywords, SmokingRegex
from feature_service.tests.integration.features.annotate_tests import MatchHintVectorizeBase


class TestSmoking(unittest.TestCase):
    __EXP_STATUS = SmokingStatus.CURRENT_SMOKER
    __EXP_ANNOTATIONS = [((0, 29), [__EXP_STATUS.name])]

    def test_annotate_nonsense(self):
        observed = Smoking().annotate('Dogs are a mans best friend')

        self.assertEqual([((0, 27), [SmokingStatus.UNKNOWN.name])], observed)

    def test_annotate(self):
        observed = Smoking().annotate('Patient smokes 1 pack per day')

        self.assertEqual(self.__EXP_ANNOTATIONS, observed)

    def test_aggregate(self):
        machine_annotation = annotate_text('Patient smokes 1 pack per day',  feature_types=[FeatureType.smoking])

        for t in range(len(machine_annotation.tokens)):
            self.assertEqual([self.__EXP_STATUS.name], machine_annotation[FeatureType.smoking.name, t])

    def test_vectorize_all(self):
        feature = Smoking()

        text_map = {SmokingStatus.PAST_SMOKER: "Pt is former smoker.",
                    SmokingStatus.UNKNOWN: "No info available.",
                    SmokingStatus.CURRENT_SMOKER: "Pt smokes.",
                    SmokingStatus.NON_SMOKER: "Pt does not smoke."
                    }

        for status in SmokingStatus:
            if status == SmokingStatus.SMOKER:
                continue

            machine_annotation = annotation.annotate_text(text_map[status], feature_types=[feature.feature_type])

            vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[feature.feature_type])

            expected = [0] * feature.vector_length
            expected[status.value] = 1
            self.assertListEqual(expected, vectors.output_dict[feature.feature_type][0],
                                 msg=f'Vectorization failed for {status}')

    def test_smoking_vectorize_invalid_token(self):
        """ Test Smoking invalid token """
        feature = Smoking()

        machine_annotation = annotation.annotate_text('asdf', feature_types=[feature.feature_type])

        vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[feature.feature_type])

        expected = [0] * feature.vector_length
        expected[SmokingStatus.UNKNOWN.value] = 1
        self.assertListEqual(expected, vectors.output_dict[feature.feature_type][0])


class TestSmokingKeywords(MatchHintVectorizeBase):
    def test_annotate_cigarette(self):
        expected = [((11, 20), ['CIGARETTE'])]

        self.__test_annotate('Pt has h/o cigarette use. We should not annotate acigarette.', expected)

    def test_annotate_smoker(self):
        expected = [((15, 21), ['SMOKER'])]

        self.__test_annotate('Pt is longtime smoker. We should not annotate asmoker.', expected)

    def test_annotate_smoking(self):
        expected = [((0, 7), ['SMOKING'])]

        self.__test_annotate('SMOKING: NO', expected)

    def test_annotate_tobacco(self):
        expected = [((10, 17), ['TOBACCO'])]

        self.__test_annotate('Pt. loves tobacco!', expected)

    def __test_annotate(self, text: str, expected: List):
        annotations = SmokingKeywords().annotate(text)

        self.assertListEqual(expected, annotations)

    def test_vectorize_no_match(self):
        self._test_vectorize_no_match(SmokingKeywords())

    def test_vectorize_all(self):
        self._test_vectorize_all_definitions(SmokingKeywords(), exclusions={'AMOUNT'})

    def test_vectorize_amount(self):
        feature = SmokingKeywords()

        self._test_vectorize(feature.DEFINITIONS['AMOUNT'][0], feature,
                             [feature.CONST_KEYS['AMOUNT'], feature.CONST_KEYS['DURATION']])


class TestSmokingRegex(unittest.TestCase):
    def test_annotate_cigarette(self):
        expected = [((11, 14), [{'$CIG': 'cig'}])]

        self.__test_annotate('Pt has h/o cigarette use. We should not annotate acigarette.', expected)

    def test_annotate_smoker(self):
        expected = [((15, 19), [{'$SMOK': 'smok'}])]

        self.__test_annotate('Pt is longtime smoker. We should not annotate asmoker.', expected)

    def test_annotate_smoking(self):
        expected = [((0, 4), [{'$SMOK': 'SMOK'}])]

        self.__test_annotate('SMOKING: NO', expected)

    def test_annotate_tobacco(self):
        expected = [((10, 15), [{'$TOBAC': 'tobac'}])]

        self.__test_annotate('Pt. loves tobacco!', expected)

    def test_annotate_non_smoker(self):
        expected = [((8, 16), [{'$NONSMOKER': 'non-smok'}]),
                    ((12, 16), [{'$SMOK': 'smok'}])]

        self.__test_annotate('Pt is a non-smoker. We should not annotate anonsmoker.', expected)

    def __test_annotate(self, text: str, expected: List):
        annotations = SmokingRegex().annotate(text)

        self.assertListEqual(expected, sorted(list(annotations)))

    def test_vectorize_cigarette(self):
        expected = [0, 1, 0, 0, 0, 0, 0]

        self.__test_vectorize('cigarette', expected)

    def test_vectorize_smoker(self):
        expected = [0, 0, 0, 0, 0, 1, 0]

        self.__test_vectorize('smoker', expected)

    def test_vectorize_smoking(self):
        expected = [0, 0, 0, 0, 0, 1, 0]

        self.__test_vectorize('SMOKING', expected)

    def test_vectorize_tobacco(self):
        expected = [0, 0, 0, 0, 0, 0, 1]

        self.__test_vectorize('tobacco', expected)

    def test_vectorize_non_smoker(self):
        expected = [0, 0, 0, 0, 1, 1, 0]

        self.__test_vectorize('non-smoker', expected)

    def test_former_smoker(self):
        expected = [0, 0, 1, 0, 0, 1, 0]

        self.__test_vectorize('ex-smoker', expected)

    def test_negations(self):
        expected = [0, 0, 0, 1, 0, 0, 0]

        self.__test_vectorize('quit', expected)

    def test_amount(self):
        expected = [1, 0, 0, 0, 0, 0, 0]

        self.__test_vectorize('2ppd', expected)

    def __test_vectorize(self, token: str, expected: List):
        feature = SmokingRegex()

        machine_annotation = annotation.annotate_text(token, feature_types=[feature.feature_type])
        vectors = vectorization.vectorize_from_annotations(machine_annotation, feature_types=[feature.feature_type])
        observed = vectors.output_dict[feature.feature_type][0]

        # $AMOUNT, $CIG, $FORMER_SMOKER, $NEGATIONS, $NONSMOKER, $SMOK, $TOBAC

        self.assertListEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
