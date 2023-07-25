from enum import Enum


class SmokingStatus(Enum):
    UNKNOWN = 0
    PAST_SMOKER = 1
    CURRENT_SMOKER = 2
    SMOKER = 3
    NON_SMOKER = 4
