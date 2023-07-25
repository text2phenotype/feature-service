from typing import List, Dict
import re


###############################################################################
#
# LVG : Lexical variant generation
#
###############################################################################

def match_hint(text: str, curated: list) -> Dict:
    matches = dict()

    for candidate in curated:

        # pattern must use word boundary
        pattern = (r'\b%s\b' % candidate)

        # headers are Uppercase
        for match in re.finditer(pattern, text, flags=re.MULTILINE):

            index = range(match.start(), match.end())
            token = text[match.start():match.end()]

            if index not in matches:
                matches[index] = list()

            matches[index].append({candidate: token})
    return matches


###############################################################################
#
# LVG : Lexical variant generation
#
###############################################################################

def lvg(curated: list) -> List:
    """
    LVG -- "Title Case" and "UPPERCASE"
    :param curated: list of strings (expert curated)
    :return: list str
    """
    _upper = [utterance.upper() for utterance in curated]
    _diff = list(set(curated) - set(_upper))

    _title = [utterance.upper() for utterance in _diff]
    _sentence = sentencecase(_diff)

    return list(set(_upper + _title + _sentence))


def uppercase(curated: list) -> List:
    """
    LVG -- "UPPERCASE"
    :param curated: list of strings (expert curated)
    :return: list str
    """
    return list(set(curated + [utterance.upper() for utterance in curated]))


def titlecase(curated: list) -> List:
    """
    LVG -- "Title Case"
    :param curated: list of strings (expert curated)
    :return: list containing curated, "Title Case"
    """
    return list(set(curated + [utterance.title() for utterance in curated]))


def sentencecase(curated: list) -> List:
    """
    LVG -- "Sentenece case only the first word capitalized"
    :param curated: list of strings (expert curated)
    :return: list containing curated, "Title Case", and "UPPERCASE"
    """
    variants = list()
    for utterance in curated:

        tokens = utterance.split()

        if len(tokens) == 1:
            variants.append(tokens[0].title())
        else:
            first = tokens[0].title()
            rest = ' '.join(tokens[1:])
            variants.append(first + ' ' + rest)

    return list(set(curated + variants))
