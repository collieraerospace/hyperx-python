from enum import Enum

class UserConstantDataType(Enum):
    Invalid = 0
    FloatingPoint = 1
    OptionalFloatingPoint = 2
    Integer = 3
    OptionalInteger = 4
    Boolean = 5
    Selection = 6
    Text = 7
