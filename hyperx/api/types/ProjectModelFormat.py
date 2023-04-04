from enum import Enum

class ProjectModelFormat(Enum):
    UNKNOWN = 0
    MscNastran = 1
    NeiNastran = 5
    NxNastran = 6
    Abaqus = 7
    Ansys = 8
    OptiStruct = 9
