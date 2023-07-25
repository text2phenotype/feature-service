import unittest

from text2phenotype.common.feature_data_parsing import from_bag_of_words

from feature_service.common.bsv import (
    parse_bsv_concept_aspect,
    parse_bsv_concept_aspect_pubmed,
)
from feature_service.resources import (
    CCDA_CODES_BSV,
    CCDA_SECTIONS_BSV,
    CUI_RULE_BSV,
    HEPC_BLACKLIST_BSV,
    NLP_CONSTANTS_BSV,
    PUBMED_BSV,
)


CUI_FILES = [CUI_RULE_BSV,
             HEPC_BLACKLIST_BSV,
             PUBMED_BSV,
             CCDA_CODES_BSV,
             CCDA_SECTIONS_BSV,
             NLP_CONSTANTS_BSV]


class TestBiomed258(unittest.TestCase):

    def test_concept_aspect_bsv(self):

        # parse ruleset from expert curated CUI_RULE file
        curated = parse_bsv_concept_aspect(CUI_RULE_BSV)

        # spot checking that "page" (as in page 1 of 2) is blacklisted -- meaning no aspects are allowed
        aspect_list_page_number = curated['C0013862']['aspect_list']

        self.assertEqual(0, len(aspect_list_page_number))
        self.assertEqual(84, len(curated))

    def test_ccda_sections_bsv(self):
        curated = parse_bsv_concept_aspect(CCDA_SECTIONS_BSV)

        self.assertEqual(139, len(curated))

    def test_pubmed_bsv(self):
        ruleset = parse_bsv_concept_aspect_pubmed()
        self.assertEqual(809, len(ruleset))

        aspect_list_septicemia = ruleset['C0243026']['aspect_list']

        self.assertEqual(len(aspect_list_septicemia), 2)
        self.assertIn('diagnosis', aspect_list_septicemia)
        self.assertIn('problem', aspect_list_septicemia)

    def assertAspectList(self, actual, expected):
        s1, s2 = set(actual), set(expected)

        self.assertEqual(len(s1), len(s2))
        self.assertEqual(len(s1), len(s1 & s2))

    def test_check_duplicates_concept_aspect_list_expert_labled(self):
        """
        :return:
        """
        parsed = dict()
        merged = dict()
        cuilist = list()

        for f in CUI_FILES:
            parsed[f] = parse_bsv_concept_aspect(f)

            for cui in parsed[f].keys():
                cuilist.append(str(cui))

                if merged.get(cui, None) is None:
                    merged[cui] = parsed[f][cui]
                else:
                    self.assertAspectList(merged[cui]['aspect_list'], parsed[f][cui]['aspect_list'])

        from_bag_of_words(list(cuilist))

    def test_nlp_constants_bsv(self):

        curated = parse_bsv_concept_aspect(NLP_CONSTANTS_BSV)

        ccda_sections = [
            'C0275723',  # oid (object identifier)
            'C0012634',  # Disease
            'C0011900',  # Diagnosis
            'C0039082',  # Syndrome
            'C1509143',  # Physical assessment findings
            'C0489531',  # History of allergies
            'C0455458',  # past medical history
            'C3841837',  # Hospitalization
            'C0239966',  # Hospital patient (finding)
            'C3840745',  # Hospital emergency department
            'C0559546',  # Adverse Reactions
            'C1628992',  # Admission Diagnosis
            'C1627937',  # Medications on Admission
            'C0042196',  # Vaccination
        ]
        for cui in ccda_sections:
            self.assertIn(cui, curated, cui)
