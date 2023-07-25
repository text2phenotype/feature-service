from enum import Enum
from typing import List, Dict

from text2phenotype.constants import umls
from text2phenotype.ccda.document import DocumentType
from text2phenotype.ccda.section import Aspect
from text2phenotype.common import common
from text2phenotype.common.common import write_json, write_text

from feature_service.tests.experiment.docont import loinc_sections

#####################################################################
# Constants
#
# BSV Header constants for UMLS support in BSV format.
# CUI,TUI,TTY,SAB(vocab) definitions
#
######################################################################

class HeaderCUI(Enum):
    """
    left: document type or section
    right: CUI Concept Unique identifier for the header
    """
    consult_note = 'C0551559' # DocumentType.consult_note
    history_and_physical_note = 'C1316580' # DocumentType.history_and_physical_note
    discharge_summary = 'C0801840' # DocumentType.discharge_summary
    progress_note = 'C0551633' # DocumentType.procedure_note.value
    diagnostic_imaging_study = 'C0801762' # DocumentType.diagnostic_imaging_study
    surgical_operation_note = 'C0551628' # DocumentType.surgical_operation_note
    procedure_note = 'C3853717' # DocumentType.procedure_note.value
    pathology = 'C3483153' # '70949-3'
    referral = 'C2735498' # 57133-1
    nursing = 'C1316576' # '34113-1'
    section = 'C3699344' # '73983-9'
    transfer = 'C1316596' # 34133-9/Summary of episode
    fhir_type_document = 'C1547673' # hl7.org/fhir/valueset-document-classcodes.html
    fhir_type_facility = 'C1547726' # hl7.org/fhir/valueset-c80-facilitycodes.html
    fhir_type_subtype  = 'C2826012' # hl7.org/fhir/DSTU2/valueset-c80-doc-typecodes.html
    # C4484185 LOINC Document Ontology - Type of Service and Kind of Document
    # C5214701

class HeaderTUI(Enum):
    """
    left: document type, document title, or section
    right: TUI Semantic Type Identifier for the header
    """
    doc_type = 'T185' # Classification
    doc_title = 'T102' # Group Attribute
    section = 'T077' # Conceptual Entity

class MatchTypeTTY(Enum):
    """
    MatchType = TTY

    left: type of match
    right: TTY closest match in UMLS
    """
    strict = 'PT'  # Designated preferred term
    relax  = 'HS'  # Short or alternate version of hierarchical term
    multi  = 'CU'  # Common usage
    abbr   = 'RAB' # Root abbreviation
    body   = 'LLT' # Lower Level Term
    negate = 'NO'

    #RHT = 'Root hierarchical term'
    #LC  = 'Long common name'
    #OSN = 'Official short name'
    #LN = 'LOINC official fully specified name'
    #PT = 'PT Designated preferred name'


class HeaderBSV:
    """
    Headers are only partially output as BSV types.
    Note all metadata is loaded into BSV outputs (for cTAKES).

    cui HeaderCUI document type
    tui HeaderTUI document type or title or section
    tty MatchTypeTTY (hint to deep learning -- expected strength of the match
    code loinc code (NOTE roughly ~150 loinc codes for "loinc_sections" a VERY GOOD feature for LSTM)
    vocab LNC in nearly all cases, except SNOMEDCT for "fhir_facility"
    """
    def __init__(self, meta=None):

        self.cui = None
        self.tui = None
        self.tty = MatchTypeTTY.strict.name # Default
        self.code = None
        self.vocab = umls.Vocab.LNC.name # Default
        self.text = None
        self.pref = None
        self.source = None

        if meta:
            self.from_json(meta)

    def from_json(self, source: dict):
        self.cui = source.get('cui', None)
        self.tui = source.get('tui', None)
        self.tty = source.get('tty', None)
        self.code = source.get('code', None)
        self.vocab = source.get('vocab', umls.Vocab.LNC.name)
        self.text = source.get('text', source.get('head', None))
        self.pref = source.get('pref', None)

    def to_bsv(self):
        return f'{self.cui}|{self.tui}|{self.tty}|{self.code}|{self.vocab}|{self.text}|{self.pref}'

def get_tty_priority(meta:dict)->str:
    """
    Prioritize TTY Term Types from weakest to strongest
    Priority order is negation, abbreviation, body(anatomic site), multi, relax, strict
    :param meta: match_tags
    :return: str matching
    """
    negate = MatchTypeTTY.negate.name
    multi = MatchTypeTTY.multi.name
    relax = MatchTypeTTY.relax.name
    abbr = MatchTypeTTY.abbr.name
    body = MatchTypeTTY.body.name

    if meta.get(negate): return negate
    if meta.get(abbr): return abbr
    if meta.get(body): return body
    if meta.get(multi): return multi
    if meta.get(relax): return relax

    return MatchTypeTTY.strict.name

def bsv_doc_title(cui, code, text, relax=False) -> HeaderBSV:
    """
    HeaderBSV loinc coded title text for a known DocumentType

    :param cui: HeaderCUI (specifies DocumentType)
    :param code: str loinc code like 11488-4 ( https://loinc.org/11488-4 )
    :param text: str like "Consultation note"
    :param relax: True= MatchTypeTTY.relax, False=MatchTypeTTY.strict
    :return:
    """
    row = HeaderBSV({'cui':cui, 'code': code, 'text': text, 'pref': text, 'relax': relax, 'strict': (not relax)})
    row.tui = HeaderTUI.doc_title.value
    row.tty = get_tty_priority({'relax': relax})
    return row

def bsv_doc_title_list(cui, mappings:dict, relax=False) -> List[HeaderBSV]:
    """
    list processing
    :param cui: HeaderCUI (specifies DocumentType)
    :param mappings: dict with entries {code:title}
    :param relax: True= MatchTypeTTY.relax, False=MatchTypeTTY.strict
    :return:
    """
    out = list()
    for code,text in mappings.items():
        out.append(bsv_doc_title(cui=cui, code=code, text=text, relax= relax))
    return out

def bsv_doc_title_strict(cui, mappings:dict) -> List[HeaderBSV]:
    """
    (convenience functions)
    list processing for strict document title
    :param cui: HeaderCUI (specifies DocumentType)
    :param mappings: dict with entries {code:title}
    :return:
    """
    return bsv_doc_title_list(cui=cui, mappings=mappings, relax=False)

def bsv_doc_title_relax(cui, mappings:dict) -> List[HeaderBSV]:
    """
    (convenience functions)
    list processing for strict document title
    :param cui: HeaderCUI (specifies DocumentType)
    :param mappings: dict with entries {code:title}
    :return:
    """
    return bsv_doc_title_list(cui=cui, mappings=mappings, relax=True)

def bsv_section(meta:dict)->HeaderBSV:
    """
    Section header --> BSV row
    NOTICE: Lossy data transform. Note all section header information is needed by cTAKES (or FDL)

    cui  = HeaderCUI.section
    tui  = HeaderTUI.section
    tty  = MatchType
    code = LOINC section code (roughly 150 to 200 known sections)
    text = section heading like "FINAL DIAGNOSIS"
    pref = optional text of preferred term

    :param meta: dict optionally including match_tags
    :return:
    """
    row = HeaderBSV(meta)

    if not row.cui:
        row.cui = row.code
    if not row.tui:
        row.tui = HeaderTUI.section.value
    if not row.tty:
        row.tty = get_tty_priority(meta)
    if not row.code:
        row.code = HeaderCUI.section.value
    if not row.text:
        row.text = meta.get('head')
    if not row.pref:
        row.pref = row.text
    return row

def write_bsv(out:list, filename):
    """
    (convenience functions)
    """
    common.write_text('\n'.join(out), filename)

def get_aspect_sections() -> dict:
    """
    :return: dict having key:val { Aspect name : list { code: dict of match_tags} }
    """
    return { Aspect.allergy: loinc_sections.make_allergy(),
             Aspect.immunization: loinc_sections.make_immunization(),
             Aspect.social: loinc_sections.make_social(),
             Aspect.lab: loinc_sections.make_lab(),
             Aspect.medication: loinc_sections.make_medication(),
             Aspect.problem: loinc_sections.make_problem(),
             Aspect.diagnosis: loinc_sections.make_diagnosis(),
             Aspect.physical_exam: loinc_sections.make_physical(),
             Aspect.treatment: loinc_sections.make_instructions(),
             Aspect.demographics: loinc_sections.make_demographics(),
             Aspect.encounter: loinc_sections.make_encounter(),
             Aspect.procedure: loinc_sections.make_procedure(),
             'imaging': loinc_sections.make_imaging(),
             'operation': loinc_sections.make_surgery(),
             'pathology': loinc_sections.make_pathology()}

def parse(contents:str, col_key=0, col_value=1, col_separator='|')->Dict:
    """
    :param contents: str bsv contents
    :param col_key: int column for key loinc
    :param col_value: int column for value display
    :return: list [ {loinc1:display1}, {loinc2,display2} ]
    """
    out = dict()
    for line in contents.splitlines():
        if not line.startswith('#'):
            tokens = line.strip().split(col_separator)

            if len(tokens) > 1:
                code = tokens[col_key]
                desc = ' '.join(tokens[col_value:])
                out[code] = desc
    return out