import unittest
import os
from feature_service.tests.experiment.docont import loinc_sections
from feature_service.tests.experiment.docont import loinc_bsv

TEST_OUTPUT = os.environ.get('TEST_OUTPUT', False)

def jira_filename(aspect_label, filetype):
    return f"./out/BIOMED-1431.loinc.sections.{aspect_label}.{filetype}"

def simplify(loinc_sections_slice: dict) -> dict:
    merged = dict()
    for code, synonyms in loinc_sections_slice.items():
        merged[code] = dict()
        for syn in synonyms:
            if not isinstance(syn, dict):
                syn = {'head': syn}
            head = syn['head']
            del syn['head']
            merged[code][head] = syn
    return merged

def write_loinc_json(loinc_sections_slice: dict, aspect_label:str) -> None:
    merged_json = simplify(loinc_sections_slice)

    if TEST_OUTPUT:
        print(f'write_loinc_json {aspect_label}')
        loinc_bsv.write_json(merged_json, jira_filename(aspect_label, 'json'))

def write_loinc_tsv(loinc_sections_slice: dict, aspect_label:str) -> None:
    merged_tsv = json_to_table(loinc_sections_slice)

    if TEST_OUTPUT:
        print(f'write_loinc_tsv {aspect_label}')
        loinc_bsv.write_text(merged_tsv, f'./out/{aspect_label}.tsv')

def json_to_table(loinc_sections_merged: dict, tab='\t'):
    group_visit = ['visit', 'encounter', 'demographics', 'social']
    group_drug  = ['drug', 'med','allergy', 'immunization']
    group_proc  = ['procedure', 'device', 'operate','pathology']
    group_prob  = ['problem', 'diagnosis', 'symptom']
    group_measure=['measure', 'lab', 'finding', 'vital', 'imaging', 'objective']
    group_exam  = ['physical', 'ros']
    aspect = set(group_visit +group_drug +group_proc +group_prob +group_measure + group_exam)

    out = list()
    current = None

    for code, synonyms in loinc_sections_merged.items():
        if code != current:
            out.append('\n#')
            current = code

        for syn in synonyms:

            row = [code]

            semantics = aspect.intersection(syn)
            if len(semantics) > 1:
                raise Exception(f'{syn}')

            semantics = list(semantics).pop()

            row.append(str(semantics))
            row.append(syn.get(str(semantics)))

            row.append(syn.get('who', '???'))
            row.append(syn.get('where', '*'))
            row.append(syn.get('when', '*'))
            row.append(syn.get('why', '*'))

            row.append(syn.get('impress', '*'))
            row.append(syn.get('instruct', '*'))

            row.append(syn.get('style', '?'))
            row.append(syn.get('match', '??'))

            row.append('common' if 'common' in syn else '*')
            row.append('multi' if 'multi' in syn else '*')

            row.append(syn.get('rank', '*'))
            row.append(syn.get('head', '!!!INVALID'))
            #row.append(syn.get('pref', '@'))

            out.append(str(tab.join(row)))
    return '\n'.join(out)

class TestBiomed1431_SectionizerMap(unittest.TestCase):

    def test_table(self):

        # visit
        write_loinc_tsv(loinc_sections.make_coversheet(), 'coversheet')
        write_loinc_tsv(loinc_sections.make_encounter(), 'encounter')
        write_loinc_tsv(loinc_sections.make_demographics(), 'demographics')
        write_loinc_tsv(loinc_sections.make_social(), 'social')

        # problem
        write_loinc_tsv(loinc_sections.make_problem(), 'problem')
        write_loinc_tsv(loinc_sections.make_diagnosis(), 'diagnosis')
        write_loinc_tsv(loinc_sections.make_symptom(), 'symptoms')

        # drug
        write_loinc_tsv(loinc_sections.make_medication(), 'medication')
        write_loinc_tsv(loinc_sections.make_allergy(), 'allergy')
        write_loinc_tsv(loinc_sections.make_immunization(), 'immunization')

        # procedure
        write_loinc_tsv(loinc_sections.make_procedure(), 'procedure')
        write_loinc_tsv(loinc_sections.make_surgery(), 'surgery')
        write_loinc_tsv(loinc_sections.make_device(), 'device')
        write_loinc_tsv(loinc_sections.make_pathology(), 'pathology')
        write_loinc_tsv(loinc_sections.make_imaging(), 'imaging')

        # measure
        write_loinc_tsv(loinc_sections.make_finding(), 'finding')
        write_loinc_tsv(loinc_sections.make_vital(), 'vital')
        write_loinc_tsv(loinc_sections.make_physical(), 'physical')
        write_loinc_tsv(loinc_sections.make_lab(), 'lab')

    def test_make(self):
        write_loinc_json(loinc_sections.make(), 'merged')
        #write_loinc_tsv(loinc_sections.make(), 'merged')

    def test_visit(self):
        write_loinc_json(loinc_sections.make_encounter(), 'encounter')
        write_loinc_json(loinc_sections.make_demographics(), 'demographics')
        write_loinc_json(loinc_sections.make_social(), 'social')


    def test_measure(self):
        write_loinc_json(loinc_sections.make_lab(), 'lab')
        write_loinc_json(loinc_sections.make_vital(), 'vitals')
        write_loinc_json(loinc_sections.make_physical(), 'physical_exam')

    def test_drug(self):
        write_loinc_json(loinc_sections.make_medication(), 'medication')
        write_loinc_json(loinc_sections.make_immunization(), 'immunization')
        write_loinc_json(loinc_sections.make_allergy(), 'allergy')

    def test_problem(self):
        write_loinc_json(loinc_sections.make_problem(), 'problem')
        write_loinc_json(loinc_sections.make_diagnosis(), 'diagnosis')
        write_loinc_json(loinc_sections.make_symptom(), 'symptom')

    def test_procedure(self):
        write_loinc_json(loinc_sections.make_procedure(), 'procedure')
        write_loinc_json(loinc_sections.make_imaging(), 'procedure_imaging')
        write_loinc_json(loinc_sections.make_surgery(), 'procedure_operation')
        write_loinc_json(loinc_sections.make_device(), 'procedure_device')

    def test_instructions(self):
        write_loinc_json(loinc_sections.make_instructions(), 'instructions')
        write_loinc_json(loinc_sections.make_coversheet(), 'coversheet')

    def test_pathology(self):
        write_loinc_json(loinc_sections.make_pathology(), 'pathology')
