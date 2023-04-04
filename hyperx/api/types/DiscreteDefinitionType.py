from enum import Enum

class DiscreteDefinitionType(Enum):
    none = 0
    LeftOpenSpanShell = 1
    RightOpenSpanShell = 2
    StiffenerFullBeam = 3
    WebShell = 4
    FootBeam = 5
    CapBeam = 6
    LeftFootSkinComboShell = 7
    RightFootSkinComboShell = 8
    LeftCapShell = 9
    RightCapShell = 10
    StiffenerPartialNoAttachedFlange = 11
    LeftWebOfHatShell = 12
    RightWebOfHatShell = 13
    CrownShell = 14
    ClosedSpanShell = 15
    LeftSkinOverFootShell = 16
    RightSkinOverFootShell = 17
    HatCombinedFootBeam = 18
    HatCombinedWebShell = 19
    CrownBeam = 20
    LeftFootShell = 21
    RightFootShell = 22
    WebFootShell = 23
    StiffenerMidBeam = 24
    WebCapShell = 25
    WebCruciformLower = 26
    WebCruciformUpper = 27
