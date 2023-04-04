from enum import Enum

class ToolingSelectionType(Enum):
    Unknown = 0
    AnyValue = 1
    SpecifiedValue = 2
    SpecifiedLimitOrRange = 3
