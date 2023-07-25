from enum import Enum

from typing import Dict, List

# https://svn.apache.org/repos/asf/ctakes/sandbox/ctakes-scrubber-deid/
# https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-13-112


class PartOfSpeechBin(Enum):
    unknown = ['NULL', ',', '.', ':', '$', '(', ')', '"', "'", "''", '``', '#', 'POS']
    com_dep_wd = ['CC', 'CT', 'DT', 'EX', 'IN', 'MD', 'PDT', 'RP', 'TO', 'UH', 'WDT']
    FW_Symb = ['FW', 'SYM']
    Adjectives = ['JJ', 'JJR', 'JJS']
    Nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    Adverbs = ['WRB', 'RB', 'RBR', 'RBS']
    Verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    Pronouns = ['PRP', 'PRP$', 'WP', 'WP$']
    Numbers = ['CD', 'LS']

    @classmethod
    def get_pos_bin_dict(cls) -> Dict[str, List[str]]:
        """
        :return: dict having entries['pos']='bin'
        """
        lookup = dict()
        for bins, mappings in cls.__members__.items():
            for pos in mappings.value:
                lookup[pos] = bins
        return lookup
