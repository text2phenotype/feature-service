from enum import Enum

from text2phenotype.constants.umls import Vocab


###############################################################################
#
# Common
#
###############################################################################
def vectorize(umls_iterable) -> list:
    return [1 if match else 0 for match in umls_iterable]


def vectorize_passthrough() -> list:
    """
    In some cases, vectorizing a vocab list is not informative.
    For example, if the ClinicalReader endpoint has only one dictionary, or only ONE semantic type in a lab result.
    This method is for method signature compliance.

    :return: list with no elements
    """
    return list()


def intersect_ordered(expected, actual):
    return [item if item in set(actual) else None for item in expected]


def list_enum_names(umls_enum) -> list:
    return [item.name for item in umls_enum]


def list_enum_values(allowed_tui) -> list:
    return [item.value for item in allowed_tui]


###############################################################################
#
# TUI Semantic Type Functions
#
# https://metamap.nlm.nih.gov/SemanticTypesAndGroups.shtml
#
###############################################################################
def list_tui(tui_iterable) -> list:
    """
    list umls tui (name) identifiers from TUI collection
    """
    return list_enum_names(tui_iterable)


def match_tui(tui_dict: dict, tui_iterable: list = None) -> list:
    return intersect_ordered(list_tui(tui_dict), tui_iterable)


###############################################################################
#
# SAB Source Vocabulary Functions
#
# https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html
#
###############################################################################
def list_vocab(vocab_iter: Vocab) -> list:
    """
    list umls sab (name) source abbveviations from a vocab collection
    """
    return list_enum_names(vocab_iter)


def match_vocab(full_vocab_set: list,  vocab_iter: list) -> list:
    return intersect_ordered(list_enum_names(full_vocab_set), vocab_iter)

###############################################################################
#
# TTY Term TYpe in Source UMLS
#
# https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html#TTY
#
###############################################################################
def list_termtype(tty_iter) -> list:
    if isinstance(tty_iter, list):
        res = tty_iter
    else:
        res = list_enum_names(tty_iter)
    return res

def match_termtype(tty: Enum, tty_iter) -> list:
    return intersect_ordered(list_termtype(tty), tty_iter)
