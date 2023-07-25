from collections import defaultdict
import re
from typing import (
    Any,
    Dict,
    List,
    Union,
)

from text2phenotype.ccda.section import (
    Aspect,
    Person,
    RelTime,
)
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.features import FeatureType

from feature_service.constants import (
    HeaderStyle,
    SectionizerPattern,
)
from feature_service.feature_set.feature_cache import FeatureCache
from feature_service.features.feature import Feature


class Sectionizer(Feature):
    feature_type = FeatureType.sectionizer
    vector_length = (1 + len(SectionizerPattern.__members__) + len(HeaderStyle.__members__) + len(Person.__members__) +
                     len(RelTime.__members__) + len(Aspect.get_active_aspects()))

    def __init__(self):
        super().__init__()
        self.default_vector[0] = 1

    def annotate(self, text: str, **kwargs):
        matches = defaultdict(list)
        responses = self.match_sectionizer(text)
        for item in responses:
            for key in item:
                if key not in SectionizerPattern.__members__:
                    continue
                if isinstance(item[key], list):
                    match_text = item[key][0]
                    index = (item[key][1], item[key][2])
                elif isinstance(item[key], dict):
                    match_text = item[key]['match'][0]
                    index = (item[key]['match'][1], item[key]['match'][2])
                if text[min(index): max(index)].lower() != match_text.lower():
                    operations_logger.error('incorrect span for the text')
                    continue
                matches[index].append(item)
        return matches.items()

    def vectorize_token(self, token: dict, **kwargs):

        """
         encode the sectionizer header to feature vector feature include what kind of section pattern hit it is what
        kind of person type the header indicate what kind of RelTime it indicate
        :param **kwargs: """

        vector = self.zero_vector.copy()
        for item in token:
            if isinstance(list(item.values())[0], list):
                vector[1 + SectionizerPattern[str(list(item.keys())[0])].value] = 1
            elif isinstance(list(item.values())[0], dict):
                vector[1 + SectionizerPattern[str(list(item.keys())[0])].value] = 1
                # style of a header detail could be null
                if list(item.values())[0].get('section', {}).get('style'):
                    style = list(item.values())[0].get('section', {})['style'][10:]
                else:
                    style = None
                if list(item.values())[0].get('section', {}).get('person'):
                    person = list(item.values())[0].get('section', {})['person'][7:]
                else:
                    person = None
                if list(item.values())[0].get('section', {}).get('reltime'):
                    reltime = list(item.values())[0].get('section', {})['reltime'][8:]
                else:
                    reltime = None
                if list(item.values())[0].get('section', {}).get('aspect'):
                    header_aspect = list(item.values())[0].get('section', {}).get('aspect')[7:]
                    if header_aspect ==  'other':
                        header_aspect = None
                else:
                    header_aspect = None
                if style:
                    vector[1 + len(SectionizerPattern.__members__) + HeaderStyle[style].value] = 1
                if person:
                    vector[1 + len(SectionizerPattern.__members__) + len(HeaderStyle.__members__) + Person[
                        person].value] = 1
                if reltime:
                    vector[1 + len(SectionizerPattern.__members__) +
                              len(HeaderStyle.__members__) +
                              len(Person.__members__) +
                              RelTime[reltime].value] = 1
                if header_aspect:
                    vector[1 + len(SectionizerPattern.__members__) +
                              len(HeaderStyle.__members__) +
                              len(Person.__members__) +
                              len(RelTime.__members__) +
                              Aspect[header_aspect].value] = 1
        return vector

    @staticmethod
    def match_pattern(text: str, pattern: str) -> List[Dict[str, List[Union[str, Any]]]]:
        """
        :param text: original input text
        :param pattern: defined by sectionizer grammar
        :return: list of text matches the pattern e.g [{'pattern_name': ['text_matched', position_x, position_y]}]
        """
        vertical_tab = '\x0b'
        form_feed = '\x0c'

        space = f'[ {vertical_tab}{form_feed}]'

        tab = f'\t|{space}{{4}}'
        pad = f'(?:{tab}|{space}{{0,4}})'
        digit_list = '(?:[1-9][0-9]?[.])'

        text_word = r'[a-zA-Z0-9/:-]+'

        text_word_max10 = f'(?:(?:{text_word}{space}){{0,9}}{text_word})'

        newline = r'\n|\A'

        begin = f'^{pad}?'

        separator = fr'[\s|{tab}|{space}]'

        proposal = '(?:of|for|on)'
        special_word = '(?:ID|SSN|info)'

        upper_word = '[A-Z]+'
        title_word = f'[A-Z][a-z]+'

        upper_word_delimiters = rf"(?:[A-Z/'()][A-Z/_.',()]+(?:{space}[0-9&#])?)"
        upper_word_delimiters_greedy = rf"(?:[A-Z0-9/_.',()]*(?:{space}[0-9&#])?)"
        title_word_proposal = f'[A-Z][a-z]+(?:{space}{proposal})?'

        upper_word_many = f'(?:{upper_word}{space}?)+'
        title_word_many = f'(?:{title_word}{space}?)+'
        upper_word_max3 = f'(?:(?:{upper_word_delimiters}{space}){{0,2}}{upper_word})'
        upper_word_max3_delimiters = f'(?:(?:{upper_word_delimiters_greedy}{space}{{1,2}}){{0,2}}{upper_word_delimiters})'

        title_word_max3 = f'(?:(?:{title_word_proposal}{space}){{0,2}}{title_word})'
        title_word_max3_proposal = f'(?:(?:{title_word_proposal}{space}){{0,2}}{title_word_proposal})'

        upper_word_max10 = rf'(?:(?:[A-Z]|\([A-Z])(?:{upper_word_delimiters_greedy}{space}{{1,2}}){{0,9}}{upper_word_delimiters})'
        title_word_max10 = f'(?:(?:{title_word_max3_proposal}{space}){{0,3}}(?:{title_word}|{special_word}))'

        upper_word_colon = f'(?:{upper_word}{space}?:)'
        title_word_colon = f'(?:{title_word}{space}?:)'

        upper_word_colon_max3 = rf'(?:(?:[A-Z]|\([A-Z]){upper_word_max3_delimiters}?{space}?:)'
        title_word_colon_max3 = f'(?:{title_word_max3}{space}?:)'

        header_upper = f'{begin}{upper_word_max10}{space}?(?::|(?={newline}))'
        header_title = f'{begin}{title_word_max10}{space}?(?::|(?={newline}))'
        header_colon = f'{begin}(?:{upper_word_max10}|{title_word_max10}){space}?:'

        keyval_word = r'[a-zA-Z0-9/.,-]+'
        keyval_word_max3 = f'(?:(?:{keyval_word}{space}){{0,2}}{keyval_word})'

        subheader_colon = f'(?:{upper_word_colon_max3}|{title_word_colon_max3})'
        subheader_colon_strict = f'{begin}{subheader_colon}'

        keyval_colon = f'{subheader_colon}(?={space}?{keyval_word}(?!:)(?={separator}|$))'

        keyval_colon_strict = f'{subheader_colon_strict}(?={space}?{keyval_word_max3}(?: {{2}}|[\n\t\r$]))'

        page_header = f'(?:page|Page|PAGE) [1-9]{{1,2}}(?: (?:of|Of|OF) [1-9]{{1,2}})?'

        header = f'(?P<PAGE_HEADER>{page_header})' \
                 f'|(?P<HEADER_COLON>{header_colon})' \
                 f'|(?P<HEADER_UPPER>{header_upper})' \
                 f'|(?P<HEADER_TITLE>{header_title})' \
                 f'|(?P<SUBHEADER_COLON>{subheader_colon})'

        list_header = f'{begin}(?:{upper_word_max10}|{title_word_max10}){pad}(?:{digit_list})\n'
        list_first = f'{begin}1{space}?[.]'
        lst = f'(?:[(]?{digit_list}[)])|(?:(?:{list_first}|(?:{begin}|{space})){digit_list})'

        hint = f'(?P<LIST_FIRST>{list_first})' \
               f'|(?P<LIST>{lst})' \
               f'|(?P<LIST_HEADER>{list_header})' \
               f'|(?P<UPPER_WORD_COLON>{upper_word_colon})' \
               f'|(?P<TITLE_WORD_COLON>{title_word_colon})' \
               f'|(?P<TITLE_WORD>{title_word})' \
               f'|(?P<UPPER_WORD>{upper_word})' \
               f'|(?P<BLANKLINE>^\n)' \
               f'|(?P<NEWLINE>{newline})' \
               f'|(?P<BEGIN>{begin})' \
               f'|(?P<COLON>:)'

        ul = '\u00a1-\uffff'  # unicode letters range

        # IP patterns
        ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
        ipv6_re = r'\[[0-9a-f:\.]+\]'

        hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'

        domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
        tld_re = (
                r'\.'
                r'(?!-)'
                r'(?:[a-z' + ul + '-]{2,63}'
                                  r'|xn--[a-z0-9]{1,59})'
                                  r'(?<!-)'
                                  r'\.?'
        )

        host_re = '(?:' + hostname_re + domain_re + tld_re + '|localhost)'

        url = (
                r'(?:(?:[a-z0-9\.\-\+]*)://)?'  # scheme
                r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'  # user:pass authentication
                r'(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')'
                                                                   r'(?::\d{2,5})?'  # port
                                                                   r'(?:[/?#][^\s]*)?'  # resource path
        )
        email = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|" \
                r"\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f]| )*\")" \
                r"@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|" \
                r"\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|" \
                r"[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:" \
                r"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

        email_url = f'(?P<EMAIL>{email})' \
                    f'|(?P<URL>{url})'

        keyval = f'(?P<KEYVAL_COLON_STRICT>{keyval_colon_strict})' \
                 f'|(?P<KEYVAL_COLON>{keyval_colon})'

        pattern_map = {
            'HEADER': header,
            'HINT': hint,
            'KEYVAL': keyval,
            'PAGE_HEADER': f'(?P<PAGE_HEADER>{page_header})',
            'HEADER_UPPER': f'(?P<HEADER_UPPER>{header_upper})',
            'HEADER_TITLE': f'(?P<HEADER_TITLE>{header_title})',
            'HEADER_COLON': f'(?P<HEADER_COLON>{header_colon})',
            'SUBHEADER_COLON': f'(?P<SUBHEADER_COLON>{subheader_colon})',
            'TEXT_WORD_MAX10': f'(?P<TEXT_WORD_MAX10>{text_word_max10})',
            'URL': f'(?P<URL>{url})',
            'EMAIL': f'(?P<URL>{email})',
            'EMAIL_URL': email_url
        }

        try:
            pattern = pattern_map[pattern]
        except KeyError:
            raise Exception(f'Unknown pattern:{pattern}')

        matches = list()
        for m in re.finditer(pattern, text, re.MULTILINE):
            if m:
                matches.append({m.lastgroup: [m.group(), *m.span()]})

        return matches

    def match_sectionizer(self, text: str) -> List[Dict[str, List[Union[str, Any]]]]:
        """
        :param text: original input text
        :return: list of text matches the pattern e.g [{'pattern_name': ['text_matched', position_x, position_y]}]
        and if fond HEADER_UPPER contained in the file with headers detail, they will be added to result like this:
        [{'pattern_name': {'match': ['text_matched', pos_x, pos_y], 'section': {dict with details from json file}}]
        """
        header_patterns = ['HEADER', 'HEADER_UPPER', 'HEADER_TITLE', 'LIST_HEADER', 'HEADER_COLON', 'SUBHEADER_COLON']
        header_matches = self.match_pattern(text, 'HEADER')
        header_detail = FeatureCache().expert_sectionizer()

        for m in header_matches:
            pattern, values = next(iter(m.items()))

            header_value = values[0].replace(':', '').replace('.', '')  # strip colon or dot
            header_value = header_value.strip().upper()  # uppercase no spaces

            if pattern in ['HEADER_COLON', 'SUBHEADER_COLON'] and values[0][-1] == ':':
                values[0] = values[0][:-1]
                values[2] -= 1

            if pattern in header_patterns and header_value in header_detail.keys():
                header_detail[header_value].pop('umls', None)
                m[pattern] = {'match': values,
                              'section': header_detail[header_value]}

        hint_matches = self.match_pattern(text, 'HINT')

        keyval_matches = self.match_pattern(text, 'KEYVAL')

        return header_matches + hint_matches + keyval_matches
