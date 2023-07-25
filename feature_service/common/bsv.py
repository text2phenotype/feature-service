from typing import Dict

from text2phenotype.common import common
from text2phenotype.ccda.section import Aspect
from text2phenotype.common.log import operations_logger

from feature_service.constants.columns import Columns, cols_to_dict, cols_to_list, cols_to_list_unique, cols_to_template
from feature_service.common.latin import Latin
from feature_service.resources import (CUI_RULE_BSV, HEPC_BLACKLIST_BSV, PUBMED_BSV, CCDA_CODES_BSV, CCDA_SECTIONS_BSV,
                                       NLP_CONSTANTS_BSV)


def parse_bsv_list(filename: str, columns, keyname=None) -> list:
    """
    :param filename: bsv filename to parse
    :param columns: see "bsv.Columns" and "bsv.README"
    :param keyname: columns that are "unique", meaning only one, not a list. Usually the key, like CUI or TUI
    :return: List of dict
    """
    if not isinstance(columns, Dict):
        columns = cols_to_dict(columns)

    text = common.read_text(filename)
    lines = text.splitlines()
    res = list()

    for line in list(filter(None, lines)):

        if line.startswith('#'):
            operations_logger.info(f'{line}')
        else:
            tokens = line.split('|')
            entry = {}

            for col in list(columns):
                col_num = int(columns[col])
                col_val = tokens[col_num]

                if col.endswith('_list'):
                    entry[col] = list(filter(None, col_val.split(',')))
                else:
                    if col in cols_to_list(keyname):
                        entry[col] = col_val
                    else:
                        entry[col] = [col_val]
            res.append(entry)
    return res


def parse_bsv_dict(filename: str, columns, keyname) -> Dict:
    """
    :param filename: str in biomed-models/expert/summary
    :param columns: map or enum of columns
    :param keyname: str for indexing
    :return: dict having entry[keyname]={column_name, column_value}
    """
    res = dict()
    cols_list, cols_keys = cols_to_list_unique(columns, keyname)

    for entry in parse_bsv_list(filename, columns, keyname):
        index = entry.get(keyname, None)

        if res.get(index, None) is None:
            res[index] = cols_to_template(columns, keyname)
            res[index][keyname] = index

        for col in cols_list:
            unique_list = list(set(res[index][col] + entry[col]))
            res[index][col] = unique_list

    return res


def get_concept_aspect_dict(filename, columns=Columns.concept_aspect, keyname='cui') -> Dict:
    """
    :param filename: bsv file, such as CUI_RULE_BSV
    :param columns: str 'cui|tui|txt|aspect_list'
    :param keyname: str 'cui' concept unique identifier
    :return: dict of concept:aspect mappings, having entry[cui]= {tui:list, txt:list, aspect_list:list}
    """
    return parse_bsv_dict(filename, columns, keyname)


def get_semantic_aspect_dict(filename, columns=Columns.semantic_aspect, keyname='tui') -> Dict:
    """
    :param filename: str semantic type mapping rules bsv file
    :param columns: 'tui|sab|sty|aspect_list'
    :param keyname: semantic type unique identifier
    :return: dict of semantic:aspect mappings, having entry[tui]={tui:sty, sab:list, aspect_list:list}
    """
    return parse_bsv_dict(filename, columns, keyname)


CUI_RULE_FILES = [
    CUI_RULE_BSV,  # file containing ccda codes like 'Active'
    HEPC_BLACKLIST_BSV,  # HEPC blacklist curated for ECHO use case
    PUBMED_BSV,  # Physician Expert Curated dict of concepts mapped to aspects from 30k frequent concepts from PubMed
    CCDA_CODES_BSV,  # file containing ccda codes like 'Active'
    CCDA_SECTIONS_BSV,  # ccda sections that are sometimes confused with NLP concepts
    NLP_CONSTANTS_BSV  # nlp constants -- very old filter rules
]


def parse_bsv_concept_aspect(filename, columns=Columns.concept_aspect, key_name='cui') -> Dict:
    """
    :param filename: bsv file, such as CUI_RULE_BSV
    :param columns: str 'cui|tui|txt|aspect_list'
    :param key_name: str 'cui' concept unique identifier
    :return: dict of concept:aspect mappings, having entry[cui]= {tui:list, txt:list, aspect_list:list}
    """
    return parse_bsv_dict(filename, columns, key_name)


def parse_bsv_semantic_aspect(filename, columns=Columns.semantic_aspect, key_name='tui') -> Dict:
    """
    :param filename: str semantic type mapping rules bsv file
    :param columns: 'tui|sab|sty|aspect_list'
    :param key_name: semantic type unique identifier
    :return: dict of semantic:aspect mappings, having entry[tui]={tui:sty, sab:list, aspect_list:list}
    """
    return parse_bsv_dict(filename, columns, key_name)


def union_cui_entry(expert1: dict, expert2: dict) -> dict:
    """
    :param expert1: first expert's review of the CUI aspect, 'cui|tui|txt|aspect_list'
    :param expert2: second expert's review of the CUI aspect, 'cui|tui|txt|aspect_list'
    :return:
    """
    if expert1['cui'] != expert2['cui']:
        raise Exception(f'CUI did not agree for expert1/expert2, entries are {expert1} != {expert2}')

    merged = {'cui': expert1['cui'],
              'tui': list(set(expert1['tui'] + expert2['tui'])),
              'txt': list(set(expert1['txt'] + expert2['txt'])),
              'aspect_list': list(set(expert1['aspect_list'] + expert2['aspect_list']))}

    return merged


def merge_cui_files() -> dict:
    """
    :return: merge all the concept:aspect_list mapping files
    """
    single = dict()
    merged = dict()

    for f in CUI_RULE_FILES:
        single[f] = parse_bsv_concept_aspect(f)

        for cui in single[f].keys():
            if merged.get(cui, None) is None:
                merged[cui] = single[f][cui]
            else:
                merged[cui] = union_cui_entry(merged[cui], single[f][cui])
    return merged


def parse_bsv_concept_aspect_pubmed(filename=PUBMED_BSV) -> dict:
    """
    Physician Expert Curated dictionary of concepts mapped to aspects from 30k frequent concepts from PubMed
    JIRA/BIOMED-240

    :param filename: bsv from pubmed abstract results
    :return: Dict having keys and values defined by Columns.concept_aspect
    """
    return parse_bsv_concept_aspect(filename)


def read_curated(tsv_file):
    """
    JIRA/BIOMED-240

    Parse (read) human expert annotations
    Return (write) BSV files and Aspect Mappings

    :param tsv_file: Spreadsheet (tab delimited)
    :return: [str bsv file text, dict mapping of aspect:concepts]
             bsv is separated file, CUI|TUI|Text|aspect_name,aspect_name,
              mappings are same as bsv, indexed by aspect_name
    """
    operations_logger.info(f"Reading human expert annotations from {tsv_file}")

    bsv_list = list()
    mapping = dict()

    for line in common.read_text(tsv_file).splitlines():
        cols = line.split('\t')

        if len(cols) >= 5:

            tf = cols[0]
            cui = cols[1]
            tui = cols[2]
            sty = cols[3]
            text = cols[4]
            ignore = cols[5]

            if (len(cui) == 8) and cui.startswith('C'):
                entry = f"{cui + '|' + tui + '|' + text + '|'}"

                if ignore == '1':
                    ignore = 'IGNORE'

                    if not mapping.get(ignore, None):
                        mapping[ignore] = list()

                    bsv_list.append(entry)
                    mapping[ignore].append(entry)

                else:
                    if len(cols) == 19:
                        for c in range(6, 19):
                            if cols[c] == '1':
                                cursor = c - 6
                                aspect_name = Aspect(cursor).name

                                entry += aspect_name + ','

                                if mapping.get(aspect_name) is None:
                                    mapping[aspect_name] = list()

                                bsv_list.append(entry)
                                mapping[aspect_name].append(entry)

    operations_logger.info(f"Human annotation summary, num Concepts {len(bsv_list)} , Aspects {mapping.keys()}")

    return ['\n'.join(bsv_list), mapping]


def read_curated_write_bsv(tsv_file):
    """
    same as read_annotations, also write BSV and Mappings
    :param tsv_file:
    :return:
    """
    bsv_text, mapping = read_curated(tsv_file)

    return [common.write_text(bsv_text, f"{tsv_file}.bsv"),
            common.write_json(mapping, f"{tsv_file}.mapping.json")]


def parse_bsv_latin_resource(file_name: str):
    file_text = common.read_text(file_name)
    expert = list()
    for entry in [line.split('|') for line in file_text.strip().splitlines()]:

        clean = [e.strip() for e in entry]

        _ftr, _eng, _pre, _suf, _test, _desc = clean

        if '/' in _pre:
            for variant in list(_pre.split('/')):
                term = Latin(ftr=_ftr, eng=_eng, pre=variant, suf=_suf, test=_test, desc=_desc)
                if term.is_valid():
                    expert.append(term)
        elif '/' in _suf:
            for variant in list(_suf.split('/')):
                term = Latin(ftr=_ftr, eng=_eng, pre=_pre, suf=variant, test=_test, desc=_desc)
                if term.is_valid():
                    expert.append(term)
        else:
            term = Latin(ftr=_ftr, eng=_eng, pre=_pre, suf=_suf, test=_test, desc=_desc)

            if term.is_valid():
                expert.append(term)
    return expert
