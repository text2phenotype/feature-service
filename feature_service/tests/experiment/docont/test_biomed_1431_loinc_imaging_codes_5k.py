import unittest
import os
from feature_service.tests.experiment.docont import loinc_bsv
from feature_service.tests.experiment.docont.loinc_title import title_imaging_codes_5k

TEST_OUTPUT = os.environ.get('TEST_OUTPUT', True)

class TestBiomed1341_Imaging(unittest.TestCase):

    def relax_title(self, title:str)->str:

        title = title.replace('Guidance for', 'Guided')
        title = title.replace('Guidance.stereotactic', 'stereotactic')

        for clean in ['Administration of', ' - ', '.', ' of ', ' into ', ' for ', ' and ']:
            title = title.replace(clean, ' ')

        return title.strip()

    def test_loinc_imaging_codes_5k(self):

        out_strict = list()
        out_relax  = list()

        cui = loinc_bsv.HeaderCUI.diagnostic_imaging_study.value

        for line in title_imaging_codes_5k.code_strict.splitlines():
            if '|' in line:
                code, text = line.split('|')

                out_strict.append(
                    loinc_bsv.bsv_doc_title(cui=cui, code=code, text=text, relax=False).to_bsv())

                out_relax.append(
                    loinc_bsv.bsv_doc_title(cui=cui, code=code, text=self.relax_title(text), relax=True).to_bsv())

        if TEST_OUTPUT:
            loinc_bsv.write_bsv(out_strict, './out/loinc_imaging_codes_5k.strict.bsv')
            loinc_bsv.write_bsv(out_relax, './out/loinc_imaging_codes_5k.relax.bsv')
