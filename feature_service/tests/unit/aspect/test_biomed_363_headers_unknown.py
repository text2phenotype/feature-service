from enum import Enum
import unittest

from text2phenotype.common import common
from text2phenotype.ccda.section import Aspect

from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.resources import ASPECT_EXPERT_HEADERS_UNKNOWN


class OutputStyle(Enum):
    silent = 0  # quiet
    console = 1  # print to screen
    file_rank = 2  # write file output with rank of {header:term_frequency}
    file_aspect = 3  # write file output with aspect of {header:aspect}


# Optionally output results during the test for human review
OUTPUT_SETTING = OutputStyle.console


class TestBiomed365(unittest.TestCase):
    def setUp(self) -> None:
        self.aspect_map = FeatureCache().aspect_map()
        self.headers_unknown = common.read_json(ASPECT_EXPERT_HEADERS_UNKNOWN)

    def assertHeaderAspect(self, headers_expected, aspect_expected):
        for header in headers_expected:
            self.assertEqual(self.aspect_map[header], str(aspect_expected))

    def review(self, match_list, aspect_expected, output=OUTPUT_SETTING):
        res = dict()

        for header, rank in self.headers_unknown.items():
            if header not in self.aspect_map:
                for match in match_list:
                    if match in header:
                        if output.value >= OutputStyle.console.value:
                            pass
                        if output.value == OutputStyle.file_rank.value:
                            res[header] = rank

                        if output.value == OutputStyle.file_aspect.value:
                            res[header] = aspect_expected
                        continue

    def test_new_headers(self):

        diagnosis = ['DIAGNOSIS']
        medications = ['HOME MEDICATIONS', 'DRUG HISTORY']
        procedures = ['OPERATIONS AND PROCEDURES', 'PRINCIPAL PROCEDURE']
        treatments = ['TO DO PLAN']

        labs = ['ADMISSION LABS', 'DISCHARGE LABS', 'LABORATORY', 'LABORATORY DATA ON ADMISSION', 'PREOPERATIVE LABS',
                'ADMIT LABS', 'LABORATORY VALUES', 'LABORATORY RESULTS']

        self.assertHeaderAspect(diagnosis, Aspect.diagnosis)
        self.assertHeaderAspect(procedures, Aspect.procedure)
        self.assertHeaderAspect(treatments, Aspect.treatment)
        self.assertHeaderAspect(medications, Aspect.medication)
        self.assertHeaderAspect(labs, Aspect.lab)

    def test_diagnosis(self):
        match_list = ['DIAGNOSIS', 'DIAGNOSES', 'DIAGNOSED', 'DX ', ' DX', 'DIAGNOSTIC']
        return self.review(match_list, Aspect.diagnosis)

    def test_problem(self):
        match_list = ['PROBLEM', 'PROB ', ' PROB', 'ILLNESS ', ' ILLNESS']
        return self.review(match_list, Aspect.problem)

    def test_lab(self):
        match_list = ['LABORATOR', 'LAB ', ' LAB', ' LABS', 'LABS', 'RESULTS']
        return self.review(match_list, Aspect.lab)

    def test_treatment_override(self):
        match_list = ['OVERRID', 'TREATMENT']
        return self.review(match_list, Aspect.treatment)

    def test_procedures(self):
        match_list = ['PROCEDURE', 'OPERATION', 'BIOPSY', 'CT ', ' CT', 'MRI ', ' MRI' ' XRAY', 'XRAY ']
        return self.review(match_list, Aspect.procedure)

    def test_medication(self):
        match_list = ['MEDICATION', 'DRUG', 'PRESCRI']
        return self.review(match_list, Aspect.medication)
