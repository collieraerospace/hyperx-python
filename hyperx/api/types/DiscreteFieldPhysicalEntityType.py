from enum import Enum

class DiscreteFieldPhysicalEntityType(Enum):
    Unknown = 0
    Element = 1
    Zone = 2
    Joint = 3
    Grid = 4
    SectionCut = 5
    Solid = 6
    Point = 7
