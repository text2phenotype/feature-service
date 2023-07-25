import os
import unittest

from text2phenotype.common.common import write_text
from text2phenotype.constants.features.label_types import (
    ProblemLabel,
    CancerLabel,
)

from feature_service.active.annotator_disagreement import AnnotatorDisagreement
from feature_service.jobs.job_metadata import JobMetadata


class TestAnnotatorDisagreement(unittest.TestCase):
    def test_parse_brat_to_positions(self):
        brat_text = """T1	grade 678 699	poorly differentiated
T2	grade 1817 1823;1824 1838	poorly differentiated
T3	morphology 1839 1848	carcinoma
T4	morphology 1921 1931	large cell
T5	topography_primary 1982 1991	sinonasal
T6	morphology 1992 2008;2019 2028	undifferentiated carcinoma
T7	diagnosis 3000 3004	diag
T8	problem 3010 3014	diag
"""
        brat_file = 'test_parse_brat_to_positions.ann'
        write_text(brat_text, brat_file)

        expected = [[(678, 684), "poorly", CancerLabel.grade.name],
                    [(685, 699), "differentiated", CancerLabel.grade.name],
                    [(1817, 1823), "poorly", CancerLabel.grade.name],
                    [(1824, 1838), "differentiated", CancerLabel.grade.name],
                    [(1839, 1848), "carcinoma", CancerLabel.morphology.name],
                    [(1921, 1926), "large", CancerLabel.morphology.name],
                    [(1927, 1931), "cell", CancerLabel.morphology.name],
                    [(1982, 1991), "sinonasal", CancerLabel.topography_primary.name],
                    [(1992, 2008), "undifferentiated", CancerLabel.morphology.name],
                    [(2019, 2028), "carcinoma", CancerLabel.morphology.name],
                    [(3000, 3004), "diag", ProblemLabel.diagnosis.name],
                    [(3010, 3014), "diag", ProblemLabel.diagnosis.name]]
        try:
            observed = AnnotatorDisagreement(None, JobMetadata()).parse_brat_to_positions(brat_file)
            self.assertEqual(len(expected), len(observed))

            for exp, obs in zip(expected, observed):
                self.assertListEqual(exp, obs)

        finally:
            os.remove(brat_file)


if __name__ == '__main__':
    unittest.main()
