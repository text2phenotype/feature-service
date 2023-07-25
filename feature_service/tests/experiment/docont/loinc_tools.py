import unittest
from typing import List, Dict
from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.tests.experiment.docont import loinc_sections
from feature_service.tests.experiment.docont import loinc_bsv

################################################################
# Helper functions

def uniq(unsorted:List[str])->List[str]:
    """
    :param unsorted: list of header names
    :return: sorted list of unique header names
    """
    return sorted(list(set(unsorted)))

def dict_header_loinc()->Dict[str,str]:
    """
    :return: dict header:loinc
    """
    out = dict()

    for loinc, contexts in loinc_sections.make().items():
        for c in contexts:
            head = c['head']
            if head not in out.keys():
                out[head] = list()
            out[head].append(loinc)

    return out


def list_missing_headers(actual:List[str], expected=None) -> List[str]:
    actual = [h.upper() for h in actual]

    if expected is None:
        expected = list(dict_header_loinc().keys())

    return list(set(actual).difference(set(expected)))


