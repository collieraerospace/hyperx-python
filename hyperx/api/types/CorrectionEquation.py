from enum import Enum

class CorrectionEquation(Enum):
    Constant = 1
    Linear_Percent_Ply = 2
    Quadratic_Percent_Ply_and_Temperature = 3
    Cubic_AML = 4
    Biquadratic_Thickness = 5
    Quadratic_Diameter_and_Thickness = 6
