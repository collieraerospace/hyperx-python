from enum import Enum

class MarginCode(Enum):
    Value = 1
    NA = 2
    NAMaterial = 3
    LPB = 4
    GeomPass = 5
    DataReqdInfo = 6
    Bounds = 7
    PosLoad = 8
    NegLoad = 9
    Skipped = 10
    HighInfo = 11
    LowInfo = 12
    Unknown = 13
    LowFailure = 14
    DataReqdFail = 15
    GeomFail = 16
    Failed = 17
    NoData = 18
