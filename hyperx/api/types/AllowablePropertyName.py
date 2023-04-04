from enum import Enum

class AllowablePropertyName(Enum):
    Strain_Tension_Pristine = 1
    Strain_Compression_Pristine = 2
    Strain_Shear_Pristine = 3
    Strain_Tension_OHT = 4
    Strain_Compression_OHC = 5
    Stress_Bearing = 6
    Strain_Compression_CAI = 9
    Strain_Compression_FHC = 10
    Strain_Compression_BVID = 11
    Strain_Tension_TAI = 12
    Strain_Tension_FHT = 13
    Strain_Shear_SAI = 14
    Stress_PullThrough = 15
    Stress_Bearing_Bypass = 16
    Stress_Bypass = 17
