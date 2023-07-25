from typing import Dict

from feature_service.resources import SEMANTIC_TYPE_BSV, SEMANTIC_GROUP_BSV
from feature_service.common import bsv
from feature_service.constants import Columns


def get_semantic_type_map(key_name: str = 'tui') -> Dict:
    """
    :param key_name: 'tui' is default, can also use 'sty' to get human readable version
    :return: dict having entries like
    'T047': {'abbr': ['dsyn'], 'sty': ['Disease or Syndrome'], 'tui': 'T047'}
    """
    return bsv.parse_bsv_dict(SEMANTIC_TYPE_BSV, Columns.semantic_type, key_name)


def get_semantic_group_map(key_name: str = 'tui') -> Dict:
    """
    :param key_name: 'tui' is default, can also use 'grp' to get grouped index
    :return: dict having entries like
    'T047': {'abbr': ['dsyn'], 'sty': ['Disease or Syndrome'], 'tui': 'T047'}
    """
    return bsv.parse_bsv_dict(SEMANTIC_GROUP_BSV, Columns.semantic_group, key_name)
