from enum import Enum

class LoadSubCaseFactor(Enum):
    none = 0
    LimitOnly = 1
    UltimateOnly = 2
    LimitWithThermalHelp = 3
    LimitWithThermalHurt = 4
    UltimateWithThermalHelp = 5
    UltimateWithThermalHurt = 6
    Unfactored = 7
