from enum import Enum

class UdiscCsvTypes(Enum):
    """Different csv file types"""
    UNKNOWN = 0
    SCORECARD_OLD = 1
    SCORECARD = 2
    COMPETITION = 3
