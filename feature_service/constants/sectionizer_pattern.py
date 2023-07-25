from enum import IntEnum


class SectionizerPattern(IntEnum):
    HEADER = 0
    HEADER_UPPER = 1
    HEADER_TITLE = 2
    HEADER_COLON = 3
    SUBHEADER_COLON = 4
    PAGE_HEADER = 5
    LIST_HEADER = 6
    LIST_FIRST = 7
    KEYVAL_COLON = 8
    KEYVAL_COLON_STRICT = 9
    LIST = 10
    URL = 11
