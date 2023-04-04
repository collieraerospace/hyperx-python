from enum import Enum

class FamilyConceptUID(Enum):
    Unknown = 0
    One_Stack_Unstiffened = 1
    Two_Stack_Unstiffened = 2
    Three_Stack_Unstiffened = 3
    Honeycomb_Sandwich = 4
    Foam_Sandwich = 5
    Bonded_Trusscore_Sandwich = 6
    Fastened_Trusscore_Sandwich = 7
    Bonded_Hat = 8
    Fastened_Hat = 9
    Bonded_Twosheet_Hat = 10
    Fastened_Twosheet_Hat = 11
    Bonded_I = 15
    Bonded_T = 16
    Bonded_Z = 17
    Bonded_J = 18
    Bonded_C = 19
    Bonded_Angle = 20
    Bonded_I_Continuous_Flange = 21
    Bonded_T_Continuous_Flange = 22
    Bonded_J_Continuous_Flange = 23
    Bonded_Sandwich_I = 24
    Integral_Sandwich_Blade = 25
    Fastened_I = 26
    Fastened_T = 27
    Fastened_Z = 28
    Fastened_Angle = 29
    Integral_Blade = 30
    Integral_Inverted_T = 31
    Integral_Inverted_AngleL = 32
    I_Beam = 33
    T_Beam = 34
    C_Beam = 35
    L_Beam = 36
    Z_Beam = 37
    J_Beam = 38
    Cap_Beam = 39
    Web_Beam = 40
    Circular_Tube = 41
    Grid0 = 62
    Grid90 = 63
    OrthoGrid = 64
    WaffleGrid = 65
    IsoGrid = 66
    AngleGrid = 67
    GeneralGrid = 68
    OrthoGrid_Sandwich = 69
    AngleGrid_Sandwich = 70
    Elliptical_Tube = 71
    Rectangular_Beam = 72
    Reinforce_Core_Sandwich = 73
    Pultruded_Rod_Stiffened_Panel = 74
    Tapered_Circular_Tube = 75
    C_Channel_Fastened = 220
    I_Frame_Fastened = 221
    Shear_Clip_Frame_Fastened = 222
    Cruciform = 223
