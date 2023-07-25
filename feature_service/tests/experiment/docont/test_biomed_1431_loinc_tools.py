import unittest
import os
from feature_service.tests.experiment.docont import loinc_bsv
from feature_service.tests.experiment.docont.loinc_bsv import bsv_doc_title_strict, bsv_doc_title_relax
from feature_service.tests.experiment.docont.loinc_title import loinc_title
from feature_service.tests.experiment.docont import loinc_sections

TEST_OUTPUT = os.environ.get('TEST_OUTPUT', True)

class TestBiomed1431_LoincTools(unittest.TestCase):

    def test_bsv_doc_title(self):
        out = list()

        # Consult
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.consult_note.value, loinc_title.title_consult.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.consult_note.value, loinc_title.title_consult.code_relax)

        # Discharge
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.discharge_summary.value, loinc_title.title_discharge.code_strict)

        # H&P
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.history_and_physical_note.value, loinc_title.title_history_and_physical.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.history_and_physical_note.value, loinc_title.title_history_and_physical.code_relax)

        # Pathology
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.pathology.value, loinc_title.title_pathology.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.pathology.value, loinc_title.title_pathology.code_relax)

        # Procedure
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.procedure_note.value, loinc_title.title_procedure.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.procedure_note.value, loinc_title.title_procedure.code_relax)

        # Progress
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.progress_note.value, loinc_title.title_progress.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.progress_note.value, loinc_title.title_progress.code_relax)

        # Referral
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.referral.value, loinc_title.title_referral.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.referral.value, loinc_title.title_referral.code_relax)

        # Surgical
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.surgical_operation_note.value, loinc_title.title_surgical.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.surgical_operation_note.value, loinc_title.title_surgical.code_relax)

        # Transfer
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.transfer.value, loinc_title.title_transfer.code_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.transfer.value, loinc_title.title_transfer.code_relax)

        # FHIR
        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.fhir_type_document.value, loinc_title.fhir_classcodes.fhir_classcodes_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.fhir_type_document.value, loinc_title.fhir_classcodes.fhir_classcodes_relax)

        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.fhir_type_subtype.value, loinc_title.fhir_typecodes.fhir_typecodes_strict)

        out += bsv_doc_title_strict(
            loinc_bsv.HeaderCUI.fhir_type_facility.value, loinc_title.fhir_facility.fhir_facility_snomed_strict)

        out += bsv_doc_title_relax(
            loinc_bsv.HeaderCUI.fhir_type_facility.value, loinc_title.fhir_facility.fhir_facility_snomed_relax)

        out = [line.to_bsv() for line in out]

        if TEST_OUTPUT:
            loinc_bsv.write_bsv(out, './out/loinc_title.bsv')

    def test_bsv_compile_from_make(self):
        compiled = list()

        for code, synonyms in loinc_sections.make().items():
            for syn in synonyms:
                syn['code'] = code
                row = loinc_bsv.bsv_section(syn)
                compiled.append(row.to_bsv())

        if TEST_OUTPUT:
            loinc_bsv.write_bsv(compiled, './out/loinc_sections.bsv')

    def test_loinc_code_to_cui(self):
        """
        call log('loinc_cui', 'refresh');
        drop table if exists loinc_cui;

        create table loinc_cui
        select distinct CUI, CODE, TTY,STR from umls.MRCONSO where SAB='LNC' and CODE in
        ('48765-2', '11369-6', '11366-2', '29762-2', '61144-2', '42344-2', '42348-3', '47420-5', '30954-2', '664-3',
        '11493-4', '61149-1', '18723-7', '56846-9', '18729-4', '18720-3', '18728-6', '56874-1', '18725-2', '56847-7',
        '10160-0', '29549-3', '42346-7', '10183-2', '75311-1', '10154-3', '46239-0', '29299-5', '42349-1', '59768-2',
        '11450-4', '61133-5', '51898-5', '10157-6', '10164-2', '61150-9', '10184-0', '59776-5', '55112-7', '18834-2',
        '51848-0', '55108-5', '55109-3', '11329-0', '42347-5', '78375-3', '46241-6', '11535-2', '54531-9', '54545-9',
        '51847-2', '55110-1', '11348-0', '10219-4', '10218-6', '59769-0', '18785-6', '19005-8', '18782-3', '18783-1',
        '22029-3', '10210-3', '8716-3', '10187-3', '10190-7', '29545-1', '11384-5', '46062-6', '8648-8', '8653-8',
        '69730-0', '62387-6', '18776-5', '79191-3', '45392-8', '45394-4', '87226-7', '72143-1', '21112-8', '81954-0',
        '21612-7', '80977-2', '80978-0', '54899-0', '42078-6', '76458-9', '92634-5', '56799-0', '42077-8', '68997-6',
        '46499-0', '45401-7', '87721-7', '66477-1', '81365-9', '85658-3', '46106-1', '45396-9', '76435-7', '89061-6',
        '76437-3', '52455-3', '92707-9', '18770-8', '52525-3', '76696-4', '18841-7', '78033-8', '48768-6', '22028-5',
        '75519-9', '56816-2', '44951-2', '11347-2', '11337-3', '11293-8', '85647-6', '19826-7', '39289-4', '76427-4',
        '30947-6', '67162-8', '71727-2', '46240-8', '55111-9', '47519-4', '59772-4', '55114-3', '29554-3', '59775-7',
        '59773-2', '55115-0', '59774-0', '8724-7', '59770-8', '8690-0', '11537-8', '59771-6', '10216-0', '10223-6',
        '22637-3', '33746-9', '83321-0', '22634-0', '22635-7', '33732-9', '21859-4', '21939-4', '42186-7', '66746-9',
        '90041-5', '67203-0', '92833-3', '75621-3', '90947-3', '75321-0', '55752-0', '55107-7', '91582-7', '48766-0');

        call create_index('loinc_cui', 'CUI');

        call log('loinc_cui', 'done');
        """
        codes = loinc_sections.make().keys()

        if TEST_OUTPUT:
            print(codes)
