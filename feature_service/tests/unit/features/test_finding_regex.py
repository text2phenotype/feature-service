import unittest

from text2phenotype.constants.features.feature_type import FeatureType

from feature_service.feature_set.annotation import annotate_text
from feature_service.feature_set.vectorization import vectorize_from_annotations

class TestRegexFinding(unittest.TestCase):
    TXT = 'Diffuse hazy infiltrates\nAtelectasis \nGround glass opacities \nPleural effusion\nPleural thickening' \
          '\nInterstitial edema \nInterstitial infiltrate \nInterstitial opacities \nEffusion\nPatchy densities \n' \
          'Parenchymal opacities \nAirspace opacities \nDiffuse pulmonary infiltrates\nWidened mediastinum \nNarro' \
          'wed trachea\nDiffuse interstitial airspace densities \nInterstitial markings \nAlveolar interstitial ' \
          'infiltrates \nPatchy consolidative foci \nReticular densities \nFocal consolidation\nPericardial effusion' \
          '\nInterstitial opacification\nAlveolar densities\nFibrosis\n'

    EXPECTED_ANNOT = {2: [{'$common_finding_type': 'infiltrate'}], 6: [{'$common_finding_type': 'opacit'}],
                      8: [{'$common_finding_type': 'effusion'}], 14: [{'$common_finding_type': 'infiltrate'}],
                      16: [{'$common_finding_type': 'opacit'}], 17: [{'$common_finding_type': 'Effusion'}],
                      19: [{'$common_finding_type': 'densit'}], 21: [{'$common_finding_type': 'opacit'}],
                      23: [{'$common_finding_type': 'opacit'}], 26: [{'$common_finding_type': 'infiltrate'}],
                      34: [{'$common_finding_type': 'densit'}], 39: [{'$common_finding_type': 'infiltrate'}],
                      44: [{'$common_finding_type': 'densit'}], 48: [{'$common_finding_type': 'effusion'}],
                      50: [{'$common_finding_type': 'opacif'}], 52: [{'$common_finding_type': 'densit'}],
                      3: [{'$other_specific': 'Atelectasis'}], 53: [{'$other_specific': 'Fibrosis'}],
                      7: [{'$pleural': 'Pleural'}], 9: [{'$pleural': 'Pleural'}], 11: [{'$interstitial': 'Interstitial'}],
                      13: [{'$interstitial': 'Interstitial'}], 15: [{'$interstitial': 'Interstitial'}],
                      32: [{'$interstitial': 'interstitial'}], 35: [{'$interstitial': 'Interstitial'}], 38: [{'$interstitial': 'interstitial'}], 49: [{'$interstitial': 'Interstitial'}], 0: [{'$description': 'Diffuse'}], 1: [{'$description': 'hazy'}], 10: [{'$description': 'thick'}], 18: [{'$description': 'Patchy'}], 24: [{'$description': 'Diffuse'}], 27: [{'$description': 'Wide'}], 29: [{'$description': 'Narrow'}], 31: [{'$description': 'Diffuse'}], 40: [{'$description': 'Patchy'}]}

    EXPECTED_VECT = {
        2: [1, 0, 0, 0, 0], 6: [1, 0, 0, 0, 0], 8: [1, 0, 0, 0, 0], 14: [1, 0, 0, 0, 0], 16: [1, 0, 0, 0, 0],
        17: [1, 0, 0, 0, 0], 19: [1, 0, 0, 0, 0], 21: [1, 0, 0, 0, 0], 23: [1, 0, 0, 0, 0], 26: [1, 0, 0, 0, 0],
        34: [1, 0, 0, 0, 0], 39: [1, 0, 0, 0, 0], 44: [1, 0, 0, 0, 0], 48: [1, 0, 0, 0, 0], 50: [1, 0, 0, 0, 0],
        52: [1, 0, 0, 0, 0], 3: [0, 0, 0, 1, 0], 53: [0, 0, 0, 1, 0], 7: [0, 0, 0, 0, 1], 9: [0, 0, 0, 0, 1],
        11: [0, 0, 1, 0, 0], 13: [0, 0, 1, 0, 0], 15: [0, 0, 1, 0, 0], 32: [0, 0, 1, 0, 0], 35: [0, 0, 1, 0, 0],
        38: [0, 0, 1, 0, 0], 49: [0, 0, 1, 0, 0], 0: [0, 1, 0, 0, 0], 1: [0, 1, 0, 0, 0],
        10: [0, 1, 0, 0, 0], 18: [0, 1, 0, 0, 0], 24: [0, 1, 0, 0, 0], 27: [0, 1, 0, 0, 0],
        29: [0, 1, 0, 0, 0], 31: [0, 1, 0, 0, 0], 40: [0, 1, 0, 0, 0]}


    def test_regex_finding_annotate_vectorize(self):
        annot = annotate_text(self.TXT, feature_types={FeatureType.finding_regex})
        vectors = vectorize_from_annotations(annot, feature_types={FeatureType.finding_regex})
        self.assertDictEqual(annot[FeatureType.finding_regex].to_dict(), self.EXPECTED_ANNOT)
        self.assertDictEqual(vectors[FeatureType.finding_regex].to_dict(), self.EXPECTED_VECT)
