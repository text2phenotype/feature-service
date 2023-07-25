from enum import Enum
from text2phenotype.ccda.document import CCD
from text2phenotype.ccda.document import DischargeSummary
from text2phenotype.ccda.document import ProgressNote, HistoryAndPhysical, ConsultNote
from text2phenotype.ccda.document import ProcedureNote, DiagnosticImagingStudy, SurgicalOperationNote
from feature_service.tests.experiment.docont import loinc_sections

################################################################
#
# Make

def make():
    merged = dict()
    merged.update(make_ccda(ProgressNote))
    merged.update(make_ccda(HistoryAndPhysical))
    merged.update(make_ccda(DiagnosticImagingStudy))
    merged.update(make_ccda(ProcedureNote))
    merged.update(make_ccda(SurgicalOperationNote))
    merged.update(make_ccda(ConsultNote))
    merged.update(make_ccda(DischargeSummary))
    merged.update(make_ccda(CCD)) # README: CCD is the all encompassing "summary" can be any type of document

    merged.update(make_pathology())
    merged.update(make_lab_external())
    merged.update(make_coversheet())
    return merged

################################################################
#
# CCDA generic helper method

def make_ccda(ccda_doc_type:Enum):
    sections = dict()
    for e in ccda_doc_type:
        sections[e.value] = e.name

    return {ccda_doc_type.__document_type__.name:
                {'document': ccda_doc_type.__document_type__.value,
                 'sections':sections}}

################################################################
#
# Pathology Report

def make_pathology():
    return {'pathology_report':
                {'document': '49143-1',
                 'sections': pref_labels(loinc_sections.make_pathology())}}

################################################################
#
# Lab Report from external "send out" facilty LabCorp or Quest,
# NOT inline results within a discharge summary, progress note, etc.

def make_lab_external():
    return {'lab_external':
                {'document': '11502-2',
                 'sections': None}}


################################################################
#
# Coversheet

def make_coversheet():
    return {'coversheet':
                {'document': '64289-2',
                 'sections': pref_labels(loinc_sections.make_coversheet())}}


################################################################
#
# Prefer label

def pref_labels(codes_values:dict):
    pref = dict()

    for code, values in codes_values.items():
        if len(values) > 0:
            pref[code] = values[0]['head'].lower().replace(' ', '_')

    return pref