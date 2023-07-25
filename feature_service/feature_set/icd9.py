from typing import List, Dict
import re
from text2phenotype.common.log import operations_logger

###############################################################################
#
# EXAMPLES
#
###############################################################################

ICD9_CODE_EXAMPLES = ['084', '017.9', '008.00', '077.3', '01.11', '410', '410.9', '410.90', 'V27', 'V19.5', 'V76.89',
                      'E951', 'E874.0']


###############################################################################
#
# PARSE
#
###############################################################################
def parse_codes(text, icd_regex_pattern, icd_version_heading) -> List:  # TODO
    candidates = re.findall(icd_regex_pattern, text)
    matchset = set()

    for c in candidates:
        # print(c +':'+text)
        matchset.add(c.replace(icd_version_heading, ''))

    return list(matchset)


def parse_candidate(code: str) -> str:
    return code


###############################################################################
#
# FEATURESET
#
###############################################################################

def vectorize(code: str) -> List:
    """
    :param code:
    :return: list of attributes, ordered
    """
    major, minor = split_major_minor(code)
    return [
        is_0code(code),
        is_2digit(code),
        is_3digit(code),
        is_4digit(code),
        is_5digit(code),
        is_normal(code),
        is_special(code),
        is_vcode(code),
        is_ecode(code),
        has_dot(code),
        has_dash(code),
        major,
        minor]


def attributes(code: str) -> Dict:
    """
    :param code: string token, see ICD9_CODE_EXAMPLES
    :return: dict with attributes for each ICD9 feature
    """
    major, minor = split_major_minor(code)
    operations_logger.debug(f"{code}|{major}|{minor}")

    return {
        'is_0code': is_0code(code),
        'is_2digit': is_2digit(code),
        'is_3digit': is_3digit(code),
        'is_4digit': is_4digit(code),
        'is_5digit': is_5digit(code),
        'is_normal': is_normal(code),
        'is_special': is_special(code),
        'is_vcode': is_vcode(code),
        'is_ecode': is_ecode(code),
        'has_dot': has_dot(code),
        'has_dash': has_dash(code),
        'is_integer': is_integer(code),
        'is_letters': is_letters(code),
        'major': major,
        'minor': minor}


###############################################################################
#
# NORMAL
#
###############################################################################
def is_normal(code: str) -> bool:
    """
    :param code: str like ICD9_CODE_EXAMPLES
    :return: true if code is normal (not E/V code) and follows the digit format given the len(code)
    """
    if len(code) > 6 or is_special(code):
        return False

    if len(code) == 6:
        if not has_dot(code):
            operations_logger.warn(f'6 digit code does not contain dot(.) character {code}')
            return False
        else:
            return is_5digit(code)

    elif len(code) == 5:
        if not has_dot(code):
            return is_5digit(code)
        else:
            return is_3dot1(code) or is_2dot2(code)

    elif len(code) == 4:
        if not has_dot(code):
            return is_4digit(code)
        else:
            return is_3dot1(code)

    elif len(code) == 3:
        return is_3digit(code)

    elif len(code) == 2:
        return is_2digit(code)

    operations_logger.warn('no match case found for ICD9|{code}')
    return False


def split_major_minor(code: str) -> List:
    """
    :param code:
    :return:
    """
    if is_special(code):
        return [code, None]

    if has_dot(code):
        major, minor = code.split('.')
        return [int(strip_zero(major)), int(strip_zero(minor))]
    else:
        return [int(strip_zero(code)), None]


def is_5digit(code: str) -> bool:
    """
    :param code: str like [008.00, 00800, 410.90, 41001]
    :return: bool if format like 12345 or 123.45
    """
    if is_3dot2(code):
        return True
    else:
        return 5 == len(code) and is_integer(code)


def is_4digit(code: str) -> bool:
    """
    :param code: str like [410.9, 01.02, 07.01, 231.9,  21.86]
    :return: bool true if format like ###.# or ##.##
    """
    if is_3dot1(code) or is_2dot2(code):
        return True
    else:
        return 4 == len(code) and is_integer(code)


def is_3digit(code: str) -> bool:
    """
    :param code: str like [06.7, 1.06, 410]
    :return: bool if code format is ##.# or #.## or ###
    """
    if is_len_dot_len(code, 2, 1, is_integer, is_integer):
        return True

    if not has_dot(code) and 3 == len(code) and is_integer(code):
        return True

    return False


def is_2digit(code: str) -> bool:
    """
    :param code: [00, 01, 99]
    :return: bool if format is ##
    """
    if has_dot(code):
        return False
    return 2 == len(code) and is_integer(code)


###############################################################################
#
# HELPER
#
###############################################################################
def has_dot(code: str) -> bool:
    """
    :param code: str like [410.9, 410.90,  V19.5, V76.89, E874.0]
    :return: bool if format is true
    """
    return '.' in code


def has_dash(code: str) -> bool:
    """
    DASH (-) character sometimes used in code spanning start/stop range
    :param code: str like ['17-17.99']
    :return: bool format is true
    """
    return '-' in code


def strip_zero(code: str) -> str:
    """
    :param code: str like [001.1, 008.02, 010.83, 079.82]
    :return:     str like [1.1,   8.02,    10.83,  79.82]
    """
    if is_0code(code):
        return strip_zero(code[1:])
    else:
        return code


def is_integer(text: str, text2=None):
    """
    :param text: str like the first 3 digits
    :param text2: str like the last 2 digits (or None)
    :return: true if not special and texts are numbers without periods
    """
    if is_special(text):
        return False

    if text2 is None:
        return re.search(r'^\d+$', text) is not None
    else:
        return is_integer(text) and is_integer(text2)


def is_letters(text: str) -> bool:
    """
    :param text: like ['E', 'e', 'V', 'v', ...]
    :return: true if text is letters
    """
    return re.search(r'^[a-zA-Z]+$', text) is not None


def unique(code_list: list) -> List:
    """
    :param code_list: list str of codes like ICD9_CODE_EXAMPLES
    :return: sorted unique list
    """
    return sorted(list(set(code_list)))


###############################################################################
#
# SPECIAL
#
###############################################################################

def is_special(code: str):
    """
    https://en.wikipedia.org/wiki/List_of_ICD-9_codes_E_and_V_codes:_external_causes_of_injury_and_supplemental_classification
    :param code: str like ICD9_CODE_EXAMPLES
    :return: true if starts with "V" or "E" or is special range with dash (-) character
    """
    return is_vcode(code) or is_ecode(code) or has_dash(code)


def is_vcode(code: str) -> bool:
    """
    :param code: str like [ V19.5, E951]
    :return: bool code starts with V or v and is known VCODE length [3,5,6]
    """
    return code.startswith('V') or code.startswith('v') and len(code) in [3, 5, 6]


def is_ecode(code: str) -> bool:
    """
    :param code: str like [ E874.0 ]
    :return: true if code starts with E and is known ECODE length [5,6]
    """
    return code.startswith('E') or code.startswith('e') and len(code) in [5, 6]


###############################################################################
#
# HIERARCHY
#
###############################################################################
def is_0code(code: str, pos=0) -> bool:
    """
    :param code: str like ['084', '017.9', '008.00', '077.3', '01.11']
    :param pos: default 0, "starts with" zero is default behaviour
    :return: true if code at position is 0 and ZERO ICD9 code is known length [2:6, 8]
    """
    return code[pos] == '0' and len(code) in [2, 3, 4, 5, 6, 8]


def in_range(code: str, code_min: str, code_max: str) -> bool:
    """
    :param code: str like [001.1, 008.02, 010.83, 079.82]
    :param code_min: str like '00'
    :param code_max: str like '99.99'
    :return: bool true if both major and minor parts are in range of code_min, code_max
    """
    code = split_major_minor(code)
    code_min = split_major_minor(code_min)
    code_max = split_major_minor(code_max)

    major, minor = 0, 1

    if code[major] < code_min[major]:
        return False

    if code[major] > code_max[major]:
        return False

    if code[minor] is not None:  # minor check
        if code_min[minor] is not None:
            if code[minor] < code_min[minor]:  # code_min[minor]
                return False

        if code_max[minor] is not None:
            if code[minor] > code_max[minor]:  # code_max[minor]
                return False

    # all checks passed
    return True


def in_range_procedure(code: str) -> bool:
    """
    :param  code: str like
    :return: bool if code is less than 100 --
    TODO: note this does not guarantee an ICD9 procedure code!
    """
    return in_range(code, '00', '99.99')


def is_len_dot_len(code: str, len1, len2, major_type=is_integer, minor_type=is_integer) -> bool:
    """
    :param code: ICD9_CODE_EXAMPLES
    :param len1: major part length (before the dot)
    :param len2: minor part length (after the dot)
    :param major_type: function pointer, default is_integer()
    :param minor_type: function pointer, default is_integer()
    :return: boolean if code matches format
    """
    if has_dot(code):
        major, minor = code.split('.')
        if len1 == len(major) and len2 == len(minor):
            return major_type(major) and minor_type(minor)
    return False


def is_3dot2(code: str) -> bool:
    """
    :param code: str like [ 410.90 ]
    :return: bool if format is ###.##
    """
    return is_len_dot_len(code, 3, 2)


def is_3dot1(code: str) -> bool:
    """
    :param code: str like [ 410.9, 090.0 ]
    :return: bool if format is ###.#
    """
    return is_len_dot_len(code, 3, 1)


def is_2dot2(code: str) -> bool:
    """
    :param code: str like [ 66.32 ]
    :return: bool if format ##.##
    """
    return is_len_dot_len(code, 2, 2)


def is_2dot1(code: str) -> bool:
    """
    :param code: str like [ 06.1, 07.4, 17.4 ]
    :return: bool if format like ##.#
    """
    return is_len_dot_len(code, 2, 1)


def is_1dot2(code: str) -> bool:
    """
    :param code: str like '9.22' which is really '09.22' but sometimes written as just '9.22'
    :return: bool if format like 1.23
    """
    return is_len_dot_len(code, 1, 2)


def is_1dot1(text: str) -> bool:
    """
    :param text: text : NOTICE : this is NOT a valid ICD9 code.
    :return:
    """
    return is_len_dot_len(text, 1, 1)


###############################################################################
#
# HIERARCHY
#
###############################################################################

def lvg_code(code: str) -> List:
    """
    Lexical Variant Generation -- AKA -- Synonyms
    :param  code: str ICD9_CODE_EXAMPLES
    :return: list string synonyms
    """
    dot = has_dot(code)

    if is_special(code):
        return [code]  # TODO: no LVG support for Ecodes and Vcodes

    if len(code) == 6:
        if not dot:
            raise Exception(f'6 digit code does not contain dot(.) character {code}')
        return lvg_5digit(code)

    elif len(code) == 5:
        return lvg_5digit(code) if not dot else lvg_4digit(code)

    elif len(code) == 4:
        return lvg_4digit(code) if not dot else lvg_3digit(code)

    elif len(code) == 3:
        return lvg_3digit(code) if not dot else [code]

    elif len(code) == 2:
        return [code]

    return list()


def lvg_5digit(code: str) -> List:
    """
    LVG 5 digit codes
    :param code: str like [008.00, 00800, 410.90, 41001]
    :return: list of LVG synonyms
    """
    synonyms = list()

    if not is_5digit(code):
        raise Exception(f'is_5digit({code})')

    if not has_dot(code):
        synonyms.append(code)
        synonyms.append(f"{code[0:3]}.{code[3:5]}")
    else:
        major, minor = code.split('.')
        synonyms.append(code)
        synonyms.append(f"{major}{minor}")

    return unique(synonyms)


def lvg_4digit(code: str) -> List:
    """
    :param code: str like [410.9 , 4109]
    :return: list str synonyms
    """
    synonyms = list()

    if not is_4digit(code):
        raise Exception(f'is_4digit({code})')

    if not has_dot(code):
        raise Exception(f'lvg_4digit cannot determine if {code} is format ###.# or ##.##')

    major, minor = code.split('.')

    if is_3dot1(code):
        synonyms.append(code)
        synonyms.append(f"{major}.{minor}0")  # pad 0 like '###.#0'

    if is_2dot2(code):
        synonyms.append(code)
        synonyms.append(f"{major}.{minor}")  # pad 0 like '##.##'

    return unique(synonyms)


def lvg_3digit(code: str) -> List:
    """
    :param code: str like [06.7, 1.06, 410]
    :return: list string synonyms
    """
    synonyms = [code]

    if not is_3digit(code):
        raise Exception(f'is_3digit({code})')

    if has_dot(code):
        major, minor = code.split('.')

        if is_2dot1(code):
            synonyms.append(f"{major}.{minor}0")  # pad 0 like '##.#0'

        if is_1dot2(code):
            operations_logger.warning(f'is_1dot2({code})')
            synonyms.append(f"0{major}.{minor}")  # pad 0 like '0#.##'
    else:
        synonyms.append(f"{code[0:3]}.00")
        synonyms.append(f"{code[0:3]}.0")

    return unique(synonyms)
