from collections import defaultdict
from enum import Enum
import re
import string

from feature_service.features.feature import Feature

from text2phenotype.constants.common import OCR_PAGE_SPLITTING_KEY
from text2phenotype.constants.features import FeatureType


class Spacing(Feature):
    feature_type = FeatureType.spacing
    vector_length = 3

    def annotate(self, text: str, **kwargs):
        patterns = [r'\n\s*?\w', r'((\t)|(\s{6,}?))\w', r'\n{2,}?\s*?\w']
        matches = defaultdict(list)
        for i in range(len(patterns)):
            for match in re.compile(patterns[i]).finditer(text):
                matches[(match.start(), match.end())].append(i)
        return matches.items()

    def vectorize_token(self, token, **kwargs):
        vector = self.default_vector.copy()
        for i in token:
            vector[i] = 1
        return vector


class PageBreak(Feature):
    class Position(Enum):
        AFTER = 0
        BEFORE = 1

    feature_type = FeatureType.page_break
    vector_length = len(Position)

    def annotate(self, text: str, **kwargs):
        token_chars = set(list(string.digits) + list(string.ascii_letters) + list(string.punctuation))

        matches = defaultdict(set)

        original_len = len(text)
        text = text.lstrip()
        offset = original_len - len(text)

        text = text.rstrip()
        for key in OCR_PAGE_SPLITTING_KEY:
            for match in re.finditer(key, text):
                if match.start() > 0:
                    end = match.end()
                    while end < len(text) and text[end] not in token_chars:
                        end += 1

                    matches[(end + offset, end + offset + 1)].add(self.Position.BEFORE.name)

                if match.end() < len(text):
                    start = match.start()
                    while start >= 0 and text[start] not in token_chars:
                        start -= 1

                    matches[(start + offset, start + offset + 1)].add(self.Position.AFTER.name)

        return matches.items()

    def vectorize_token(self, token, **kwargs):
        if not token:
            raise Exception()

        vector = self.default_vector.copy()
        for p in token:
            vector[self.Position[p].value] = 1

        return vector
