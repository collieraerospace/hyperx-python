from enum import Enum

class JointObject(Enum):
    EntireJoint = 0
    Fastener = 1
    Sheet1 = 2
    Sheet2 = 3
    Sheet3 = 4
    Sheet4 = 5
    FaceSheetEndCap = 6
    EndCap = 7
    UpperAdhesive = 8
    LowerAdhesive = 9
    UpperDoubler = 10
    LowerDoubler = 11
    EdgeAllowableSheet = 12
    Rivet = 13
