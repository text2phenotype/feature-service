import os, unittest
from text2phenotype.common import common
from text2phenotype.ccda.document import DischargeSummary, PhysicianDischargeSummary
from feature_service.tests.experiment.docont import loinc_doc

TEST_OUTPUT = os.environ.get('TEST_OUTPUT', True)

class TestBiomed1431_DocType(unittest.TestCase):

    def test_make(self):
        compiled = loinc_doc.make()

        if TEST_OUTPUT:
            common.write_json(compiled, f'./out/document.sections.json')

    def test_physician_discharge_summary(self):
        generic = [e.value for e in DischargeSummary]
        physician = [e.value for e in PhysicianDischargeSummary]

        diff = set(physician).difference(set(generic))

        self.assertEqual(0, len(diff), f"{diff}")

