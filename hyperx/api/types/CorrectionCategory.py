from enum import Enum

class CorrectionCategory(Enum):
    ElasticStiffness = 1
    StressAllowables = 2
    StrainAllowables = 3
    LaminateStrainAllowables = 4
    BoltedJointParameters = 5
    BoltedJointStressAllowables = 6
