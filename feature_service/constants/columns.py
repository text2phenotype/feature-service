from enum import Enum
from typing import List, Dict


class README(Enum):
    cui = "UMLS concept unique identifier like 'C0007634'"
    tui = "UMLS semantic type unique ID, example: 'T047'"
    sty = "UMLS semantic type name, example: 'Disease or Syndrome'"
    txt = "Human readable string, such as umls.MRCONSO.STR or umls.MRCONSO.CODE"
    csv = "List of values labeled by physician experts, optionally separated by ','"
    sab = "Source abbreviation (UMLS Preferred Vocab, like RXNORM)"
    abbr = "UMLS abbreviation"
    vocab = "UMLS abbreviation (same as SAB)"
    grp = "group, such as UMLS Semantic Type Grouping"
    aspect_list = "Aspects optionally separated by ','"
    ispref = 'UMLS preferred text'
    stt = 'UMLS String Type'
    code = 'UMLS vocab asserted code'
    L1 = 'CCS hierarchy Level 1 code'
    L2 = 'CCS hierarchy Level 2 code'
    L3 = 'CCS hierarchy Level 3 code'
    L4 = 'CCS hierarchy Level 4 code'
    L1_label = 'CCS hierarchy Level 1 label'
    L2_label = 'CCS hierarchy Level 2 label'
    L3_label = 'CCS hierarchy Level 3 label'
    L4_label = 'CCS hierarchy Level 4 label'
    label = 'CCS preferred label (string)'


class Columns(Enum):
    concept_ctakes = 'cui|tui|code|vocab|text|preferred_text'
    concept_aspect = 'cui|tui|txt|aspect_list'
    semantic_aspect = 'tui|sab|sty|aspect_list'
    semantic_type = 'abbr|tui|sty'
    semantic_group = 'abbr|grp|tui|sty'
    vocab_pref_terms = 'cui|tui|sab|code|str|stt|ispref'
    ccs_tree = 'code|L1|L1_label|L2|L2_label|L3|L3_label|L4|L4_label|label|vocab'


def cols_to_list(columns: str) -> List:
    """
    :param columns: str list of columns
    :return: list of column strings
    """
    if isinstance(columns, Enum):
        columns = columns.value

    return list() if columns is None else columns.split('|')


def cols_to_list_unique(columns: str, keyname=None) -> List:
    """
    :param columns: str like 'cui|tui|txt|aspect_list'
    :param keyname: str like 'cui'
    :return: list of two lists, like [['tui', 'aspect_list', 'txt'], ['cui']]
    """
    cols = cols_to_list(columns)
    uniq = cols_to_list(keyname)

    return [list(set(cols) - set(uniq)), uniq]


def cols_to_dict(columns: str) -> Dict:
    """
    :param columns: column string like 'cui|tui|txt|aspect_list'
    :return: dict like {'cui': 0, 'tui': 1, 'txt': 2, 'aspect_list': 3}
    """
    return {col: idx for idx, col in enumerate(cols_to_list(columns))}


def cols_to_template(columns: str, keyname=None) -> Dict:
    """
    :param columns: column string like 'cui|tui|txt|aspect_list'
    :return: dict like {'cui': None, 'tui':list, 'txt':list, 'aspect_list':list}
    """
    template = dict()
    for col in cols_to_list(columns):
        template[col] = list()

    for unique in cols_to_list(keyname):
        template[unique] = None

    return template
