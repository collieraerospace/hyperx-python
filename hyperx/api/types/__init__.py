from enum import Enum

class AnalysisId(Enum):
	UNKNOWN = 0
	PanelBucklingFlatSimpleBCSymmetricUniaxialorBiaxial = 1
	PanelBucklingFlatSimpleBCUniaxialorBiaxial = 2
	PanelBucklingFlatSimpleBCShear = 3
	PanelBucklingFlatSimpleBCSymmUniaxialorBiaxialwShearInteraction = 4
	PanelBucklingFlatSimpleBCUniaxialorBiaxialwShearInteraction = 5
	PanelBucklingFlatSimpleBCSymmUniaxialorBiaxialwTSFtransverseshearflexibility = 6
	PanelBucklingFlatSimpleBCUniaxialorBiaxialwTSF = 7
	PanelBucklingFlatSimpleBCShearwTSFTransverseShearFlexibility = 8
	PanelBucklingFlatSimpleBCUniaxialorBiaxialwTSFShearInteraction = 9
	PanelBucklingSandwichwTSF = 10
	PanelBucklingCurvedorFlatAllBC = 11
	PanelBucklingCurvedorFlatAllBCwTSFTransverseShearFlexibility = 12
	PanelBucklingFlatSimpleBCLColumnwTransverseShearFlexibility = 13
	PanelBucklingFlatSimpleBCTColumnonTranslationalSprings = 14
	StiffenerBucklingHatScissor = 15
	StiffenerBucklingFlexuralTorsionalArgyris = 16
	StiffenerBucklingFlexuralTorsionalLevy = 17
	PanelBucklingCurvedorFlatNASASP8007Method = 18
	PanelBucklingUserDefined1 = 23
	PanelBucklingUserDefined2 = 24
	BeamBucklingColumnPlane1I1 = 25
	BeamBucklingColumnPlane1wTSFI1 = 26
	BeamBucklingColumnPlane2I2 = 27
	BeamBucklingColumnPlaneMinImin = 28
	BeamBucklingLateral = 30
	BeamBucklingLateralTorsional = 31
	BeamBucklingCylindricalAxialandBendingRayleighRitz = 33
	BeamBucklingCylindricalAxialandBendingNASASP8007 = 34
	BeamBucklingUserDefined1 = 38
	BeamBucklingUserDefined2 = 39
	LocalBucklingLongitudinalDirection = 40
	LocalBucklingShearDirection = 42
	LocalBucklingInteraction = 43
	LocalBucklingInterrivet = 44
	LocalBucklingCripplingInteraction = 45
	LocalBucklingSpacingSpanSkinBiaxialwInteraction = 46
	LocalBucklingShearPermanentDeformation = 47
	CripplingIsotropicmethodNiuformedandextrudedsections = 50
	CripplingIsotropicmethodLTVformedandextrudedsections = 51
	CripplingCompositemethodMilHdbk173EincludingDij = 52
	CripplingBucklinginteractionJohnsonEuler = 53
	CripplingForcedDiagonalTension = 54
	CripplingForcedCompressionCripplingInteraction = 55
	CripplingUserDefined1 = 58
	CripplingUserDefined2 = 59
	StrainLimit = 60
	CurvatureLimit = 61
	CenterDeflectionLimit = 62
	StiffnessRequirementMembrane = 63
	StiffnessRequirementBending = 64
	FrequencyLimitPanelorBeam = 65
	FrequencyLimitObjectlocal = 66
	GeometryRule1StiffenerFlangeWidthtoFlangeThicknessRatioMin = 67
	GeometryRule2StiffenerFlangeWidthtoStiffenerHeightRatioMin = 68
	GeometryRule3StiffenerWebThicknesstoFlangeThicknessRatioMin = 69
	GeometryRule4StiffenerWebHeighttoWebThicknessRatioMax = 70
	GeometryRule5PanelHeightMax = 71
	GeometryRule40PanelWidthtoStiffenerSpacingMinofstiffeners = 72
	GeometryRule41StiffenertoSkinAreaRatioMinMax = 73
	GeometryRule42StiffenerEISlendernessRatioMin = 74
	ThermalProtectionSystemStructureTemperatureLimit = 75
	ThermalProtectionSystemMaterialSingleUseTemperatureLimit = 76
	ThermalProtectionSystemMaterialMultipleUseTemperatureLimit = 77
	ThermalProtectionSystemCryogenicLowerTemperatureLimit = 78
	WrinklingEqn1IsotropicorHoneycombCoreXYInteraction = 90
	WrinklingEqn2HoneycombCoreXYInteraction = 91
	WrinklingVinsonHoneycombXYInteraction = 92
	IntracellDimplingXYInteraction = 94
	SandwichFaceUserDefined1 = 99
	CrushingConcentratedLoad = 100
	CrushingFlexuralBendingLoad = 101
	CrushingJointSupportLoad = 102
	SandwichFlatwiseTension = 103
	SandwichFlatwiseTensionwInterlaminarShearInteraction = 104
	ShearCrimpingMinXYHexcel = 105
	ShearCrimpingMinPrincipalStressHexcel = 106
	ShearStrengthXLongitudinaldirectionHexcel = 107
	ShearStrengthYTransversedirectionHexcel = 108
	ShearStrengthInteractionQuadraticBasic = 109
	IsotropicStrengthLongitudinalDirection = 110
	IsotropicStrengthTransverseDirection = 111
	IsotropicStrengthShearDirection = 112
	IsotropicStrengthVonMisesHillInteractionYieldCriterion = 113
	IsotropicStrengthMaxShearCriterion = 114
	IsotropicStrengthMaxPrincipalStressCriterion = 115
	IsotropicStrengthNaca2661MaxShearStress = 116
	MicromechanicsMaxStress1stSubcell = 120
	MicromechanicsMaxStrain1stSubcell = 121
	MicromechanicsTsaiHill1stSubcell = 122
	MicromechanicsSIFT1stSubcell = 123
	MicromechanicsMaxStressAverageUnitCell = 124
	MicromechanicsMaxStrainAverageUnitCell = 125
	MicromechanicsTsaiHillAverageUnitCell = 126
	MicromechanicsSIFTAverageUnitCell = 127
	MicromechanicsMaxStressAllUnitCell = 128
	MicromechanicsMaxStrainAllUnitCell = 129
	MicromechanicsTsaiHillInteractionAllUnitCell = 130
	MicromechanicsSIFTAllUnitCell = 131
	CompositeStrengthMaxStrain1Direction = 135
	CompositeStrengthMaxStrain2Direction = 136
	CompositeStrengthMaxStrain12Direction = 137
	CompositeStrengthMaxStress1Direction = 138
	CompositeStrengthMaxStress2Direction = 139
	CompositeStrengthMaxStress12Direction = 140
	CompositeStrengthTsaiHillInteraction = 141
	CompositeStrengthTsaiWuInteraction = 142
	CompositeStrengthTsaiHahnInteraction = 143
	CompositeStrengthHoffmanInteraction = 144
	CompositeStrengthHashinMatrixCracking = 145
	CompositeStrengthHashinFiberFailure = 146
	CompositeStrengthLaRC03MatrixCracking = 147
	CompositeStrengthLaRC03FiberFailure = 148
	CompositeStrengthTsaiWuStrainPlyAllowables = 149
	CompositeStrengthTsaiWuStrainLaminateAllowables = 150
	CompositeStrengthOpenHoleTensionOHTMaxStrain1Direction = 151
	CompositeStrengthOpenHoleCompressionOHCMaxStrain1Direction = 152
	CompositeStrengthInterlaminarShearKick = 153
	CompositeStrengthPuck2dInterFiberFracture = 154
	CompositeStrengthPuck2dFiberFracture = 155
	CompositeStrengthPuck3dInterFiberFracture = 156
	CompositeStrengthPuck3dFiberFracture = 157
	CompositeStrengthUserDefined1 = 158
	CompositeStrengthUserDefined2 = 159
	JointBondedEdgeDelaminationOnset = 160
	JointBondedEdgeDelamination = 161
	JointBondedFracturePrincipalTransverse = 162
	JointBondedFractureMaxStressorStrain1direction = 163
	JointBondedDelaminationPeelDominated = 164
	JointBondedDelaminationPeelandTransverseShear1 = 165
	JointBondedDelaminationPeelandTransverseShear2 = 166
	JointBondedDelaminationTongPeelTransverseShearAxial1 = 167
	JointBondedDelaminationTongPeelTransverseShearAxial2 = 168
	JointBondedDelaminationTongPeelTransverseShearAxial3 = 169
	JointBondedDelaminationTongPeelTransverseShearAxial4 = 170
	JointBondedDelaminationTongPeelTransverseShearAxial5 = 171
	JointBondedDelaminationTongPeelTransverseShearAxial6 = 172
	JointBondedDelaminationPeelLongitudinalTransverseShear = 173
	JointBondedDelaminationPeelLongitudinalTransverseShearAxialandTransverse = 174
	JointBondedAdhesivePeelDominated = 175
	JointBondedAdhesiveVonMisesStrain = 176
	JointBondedAdhesiveMaximumPrincipalStress = 177
	JointBondedAdhesivePeelLongitudinalTransverseShear = 178
	JointBondedAdhesiveLongitudinalTransverseShearStress = 179
	JointBondedAdhesiveLongitudinalTransverseShearStrain = 180
	JointBondedDelaminationPropagationModeI = 181
	JointBondedDelaminationPropagationModeII = 182
	JointBondedDelaminationPropogationPowerLaw = 183
	JointBondedDelaminationPropogationBKcriterion = 184
	JointBondedLimitsOfApplicability = 185
	JointBoltedSingleHoleBJSFMloadedandfarfield = 190
	JointBoltedSingleHoleBJSFMBearingOnly = 191
	JointBoltedSingleHoleBJSFMBypassOnly = 192
	JointBoltedSingleHoleBearingIsotropicAllowable = 193
	JointBoltedUserDefined1 = 198
	JointBoltedUserDefined2 = 199
	ProgressiveFailureInverseABDTraceMethod = 201
	ProgressiveFailureAlternativeMethod = 202
	CompositeStrengthInterlaminarShear = 203
	CompositeStrengthFlatwiseTension = 204
	SandwichCoreUserDefined1 = 208
	SandwichCoreUserDefined2 = 209
	JointWebNormalCompressionorPulloff = 210
	JointWebShear = 211
	JointWebInteraction = 212
	GeometryRule71StiffenerAllLaminatesThicknesstoHoleDiameterRatioMinMaxRepairAngle = 216
	GeometryRule72StiffenerWebRepairThicknesstoHoleDiameterRatioMaxRepairAngle = 217
	GeometryRule73StiffenerSkinFlangeRepairThicknesstoHoleRatioMaxRepairAngle = 218
	GeometryRule74StiffenerHeightMinRepairAngle = 219
	GeometryRule75StiffenerFlangeWidthMinRepairAngle = 220
	CompositeStrengthLaminateCompressionPristine = 221
	CompositeStrengthLaminateCompressionAfterImpactCAI = 222
	CompositeStrengthLaminateCompressionOpenHoleOHC = 223
	CompositeStrengthLaminateCompressionFilledHoleFHC = 224
	CompositeStrengthLaminateCompressionBVID = 225
	CompositeStrengthLaminateTensionPristine = 226
	CompositeStrengthLaminateTensionAfterImpactTAI = 227
	CompositeStrengthLaminateTensionOpenHoleOHT = 228
	CompositeStrengthLaminateTensionFilledHoleFHT = 229
	CompositeStrengthLaminateShearPristine = 230
	CompositeStrengthLaminateShearAfterImpactSAI = 231
	IsotropicStrengthUltimateMaxPrincipalStressCriterion = 315
	IsotropicStrengthVonMisesInteractionYieldCriterion = 316
	MStensionOnlyYield = 330
	MStensionOnlyUltimate = 331
	MSjointSeparation = 333
	MSjointSlipUltimate = 334
	MSshearOnlyYield = 335
	MSshearOnlyUltimate = 336
	MScombinedTSBlinear = 337
	MScombinedTSBplastic = 338
	MSnutThreadShearUltimate = 339
	MSinsertInternalThreadShearUltimate = 340
	MSinsertExternalThreadShearUltimate = 341
	MSbearingYield = 343
	MSbearingUltimate = 344
	MSshearoutUltimate = 345
	MShoopTensionYield = 346
	MShoopTensionUltimate = 347
	MSboltThreadShearUltimate = 348
	MSbendingOnlyLinear = 349
	StaticJointStrengthYield = 350
	StaticJointStrengthUltimate = 351
	RivetShearStrength = 352
	PreventRivetShearFailureYield = 353
	PreventRivetShearFailureUltimate = 354
	PreventTensionLoadUltimate = 355
	PreventTensionLoadLimit = 356
	BearingBypassUltimate = 357
	MSbendingOnlyPlastic = 358
	MScombinedTS = 359
	MScombinedTBLinear = 360
	MScombinedTBPlastic = 361
	BearingOnlyComposite = 362

class LimitUltimate(Enum):
	'''
	Limit vs Ultimate loads.
	'''
	Limit = 0
	Ultimate = 1

class MarginCode(Enum):
	Value = 1
	NA = 2
	NAMaterial = 3
	LPB = 4
	GeomPass = 5
	DataReqdInfo = 6
	Bounds = 7
	PosLoad = 8
	NegLoad = 9
	Skipped = 10
	HighInfo = 11
	LowInfo = 12
	Unknown = 13
	LowFailure = 14
	DataReqdFail = 15
	GeomFail = 16
	Failed = 17
	NoData = 18

class UserConstantDataType(Enum):
	Invalid = 0
	FloatingPoint = 1
	OptionalFloatingPoint = 2
	Integer = 3
	OptionalInteger = 4
	Boolean = 5
	Selection = 6
	Text = 7

class FamilyConceptUID(Enum):
	'''
	Values match UID of family_concept_definition table.
	'''
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

class ToolingSelectionType(Enum):
	'''
	Defines which selection a given tooling constraint is currently set to.
	'''
	Unknown = 0
	AnyValue = 1
	SpecifiedValue = 2
	SpecifiedLimitOrRange = 3

class DiscreteFieldDataType(Enum):
	'''
	Defines the type of data stored in a Discrete Field. Such as Vector, Scalar, String.
	'''
	Unknown = 0
	Vector = 1
	Scalar = 2
	String = 3

class DiscreteFieldPhysicalEntityType(Enum):
	'''
	Defines the type of physical entity that a Discrete Field applies to, such as zone, element, joint, etc.
	'''
	Unknown = 0
	Element = 1
	Zone = 2
	Joint = 3
	Grid = 4
	SectionCut = 5
	Solid = 6
	Point = 7

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

class FamilyCategory(Enum):
	'''
	Representative of the family_category table
	'''
	Unknown = 0
	Panel = 1
	Beam = 2
	Joint = 3
	Unspecified = 4

class FeaSolutionType(Enum):
	Static = 0
	Buckling = 1
	Frequency = 2

class DiscreteTechnique(Enum):
	'''
	FEM Modeling technique for a Zone
	'''
	none = 0
	Two = 2
	Three = 3
	Four = 4
	Five = 5

class FemType(Enum):
	none = 0
	Unknown = 1
	GRID = 2
	CBAR = 3
	CROD = 4
	CBEAM = 5
	CBUSH = 6
	CELAS2 = 7
	CELAS3 = 8
	CQUAD4 = 9
	CQUAD8 = 10
	CQUADR = 11
	CTRIA3 = 12
	CSHEAR = 13
	CSHELL = 14
	CHEXA = 15
	CPENTA = 16
	LOAD = 18
	MAT1 = 19
	MAT2 = 20
	MAT3 = 21
	MAT5 = 22
	MAT8 = 23
	MAT9 = 24
	MAT10 = 25
	MAT11 = 26
	PBARL = 27
	PBAR = 28
	PBEAM = 29
	PBEAML = 30
	PBUSH = 31
	PCOMP = 32
	PCOMPLS = 33
	PCOMPG = 34
	PROD = 35
	PSHELL = 36
	PSHEAR = 37
	PSOLID = 38
	FORCE = 39
	MOMENT = 40
	PLOAD2 = 41
	PLOAD4 = 42
	RBE2 = 43
	RBE3 = 44
	SPC = 45
	SPC1 = 46
	TEMP = 47
	TEMPD = 48
	TEMPP1 = 49
	TEMPRB = 50
	CORD1C = 51
	CORD1R = 52
	CORD1S = 53
	CORD2C = 54
	CORD2R = 55
	CORD2S = 56
	CORD3C = 57
	CORD3R = 58
	CORD3S = 59
	MATERIAL = 60
	NODE = 61
	B31 = 62
	B32 = 63
	STRI3 = 64
	S3 = 65
	S3R = 66
	STRI65 = 67
	S4 = 68
	S4R = 69
	S8R = 70
	C3D4 = 71
	C3D10 = 72
	C3D8 = 73
	C3D8I = 74
	C3D8R = 75
	C3D6 = 76
	C3D15 = 77
	C3D20 = 78
	C3D20R = 79
	CONN3D2 = 80
	ISOTROPIC = 81
	LAMINA = 82
	ENGINEERINGCONSTANTS = 83
	BEAM = 84
	BEAMSECTION = 85
	BEAMGENERALSECTION = 86
	CONNECTORSECTION = 87
	SHELLSECTION = 88
	SHELLGENERALSECTION = 89
	SOLIDSECTION = 90
	SOLIDGENERALSECTION = 91
	ELSET = 92
	COORD3D = 93
	DISTRIBUTION = 94
	GRIDSET = 95
	DISTRIBUTIONTABLE = 96
	Rectangular = 97
	Cylindrical = 98
	Spherical = 99
	Ply = 100
	MPC = 101

class LoadCaseType(Enum):
	Static = 1
	Fatigue = 2

class LoadSubCaseFactor(Enum):
	none = 0
	LimitOnly = 1
	UltimateOnly = 2
	LimitWithThermalHelp = 3
	LimitWithThermalHurt = 4
	UltimateWithThermalHelp = 5
	UltimateWithThermalHurt = 6
	Unfactored = 7

class TemperatureChoiceType(Enum):
	'''
	Load Case Setting selection for analysis and initial temperature.
	'''
	Analysis = 0
	Value = 1
	Subcase = 2

class AllowableMethodName(Enum):
	'''
	Method name for a laminate allowable.
	'''
	AML = 1
	Percent_0 = 2
	Percent_45 = 3
	BypassStress = 4
	Polynomial = 999

class AllowablePropertyName(Enum):
	'''
	Property name for a laminate allowable.
	'''
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

class CorrectionCategory(Enum):
	'''
	Correction property category.
	'''
	ElasticStiffness = 1
	StressAllowables = 2
	StrainAllowables = 3
	LaminateStrainAllowables = 4
	BoltedJointParameters = 5
	BoltedJointStressAllowables = 6

class CorrectionEquation(Enum):
	'''
	Equation for a correction factor.
	'''
	Constant = 1
	Linear_Percent_Ply = 2
	Quadratic_Percent_Ply_and_Temperature = 3
	Cubic_AML = 4
	Biquadratic_Thickness = 5
	Quadratic_Diameter_and_Thickness = 6

class CorrectionId(Enum):
	'''
	Correction ID for a correction factor. (Columns in HyperX)
	'''
	Correction1 = 1
	Correction2 = 2
	Correction3 = 3
	Correction4 = 4
	Correction5 = 5
	Correction6 = 6
	Correction7 = 7
	Correction8 = 8
	Correction9 = 9

class CorrectionIndependentDefinition(Enum):
	'''
	Defines the type of Correction Factor.
	'''
	Temperature = 1
	Percent0s = 2
	Percent45s = 3
	AML = 4
	IsCsk = 5
	Csk = 6
	e_over_D = 7
	S_over_D = 8
	Spacing = 9
	Diameter = 10
	Thickness = 11
	D_over_t = 12
	H_over_t = 13
	ShimThickness = 14
	PointIndex = 15
	CoreDensity = 16
	CoreThickness = 17
	Skin = 18

class CorrectionProperty(Enum):
	'''
	Property name for a correction factor. (Rows in HyperX)
	'''
	Et1 = 2
	Et2 = 3
	Ec1 = 5
	Ec2 = 6
	G12 = 8
	Ftu1 = 11
	Ftu2 = 12
	Fcu1 = 13
	Fcu2 = 14
	Fsu12 = 17
	Fsu13 = 18
	Fsu23 = 19
	etu1 = 32
	etu2 = 33
	ecu1 = 34
	ecu2 = 35
	eOHT = 36
	eOHC = 37
	esu12 = 38
	esu13 = 39
	esu23 = 40
	Ftu3 = 50
	D0_Tension = 82
	D0_Compression = 84
	Tension_Pristine = 1001
	Compression_Pristine = 1002
	Shear_Pristine = 1003
	Tension_OHT = 1004
	Compression_OHC = 1005
	Bearing = 1006
	Compression_CAI = 1009
	Compression_FHC = 1010
	Compression_BVID = 1011
	Tension_TAI = 1012
	Tension_FHT = 1013
	Shear_SAI = 1014
	PullThrough = 1015
	BearingBypass = 1016

class CorrectionValueType(Enum):
	'''
	Defines the type of the independent values on a tabular correction factor row.
	'''
	Double = 0
	Bool = 1
	Integer = 2

class EquationParameterId(Enum):
	'''
	Correction factor parameter names.
	'''
	Constant_Low_Value = 1001
	Constant_High_Value = 1002
	Constant_Constant = 1003
	LinearPly_Low_Value = 2001
	LinearPly_High_Value = 2002
	LinearPly_Constant = 2003
	LinearPly_Percent_0s = 2004
	LinearPly_Percent_45s = 2005
	LinearPly_Factor_Thickness = 2006
	QuadraticPlyTemp_Low_Value = 3001
	QuadraticPlyTemp_High_Value = 3002
	QuadraticPlyTemp_Constant = 3003
	QuadraticPlyTemp_Percent_0s = 3004
	QuadraticPlyTemp_Percent_45s = 3005
	QuadraticPlyTemp_Percent_0s_Squared = 3006
	QuadraticPlyTemp_Percent_45s_Squared = 3007
	QuadraticPlyTemp_P0s_Times_P45s = 3008
	QuadraticPlyTemp_Temperature = 3009
	QuadraticPlyTemp_Temperature_Squared = 3010
	QuadraticPlyTemp_T0 = 3011
	CubicAML_Low_Value = 4001
	CubicAML_High_Value = 4002
	CubicAML_Constant = 4003
	CubicAML_AML_Number = 4004
	CubicAML_AML_Number_Squared = 4005
	CubicAML_AML_Number_Cubed = 4006
	BiQuadThick_Low_Value = 5001
	BiQuadThick_High_Value = 5002
	BiQuadThick_Threshold = 5003
	BiQuadThick_Constant_1 = 5004
	BiQuadThick_Factor_Thickness_1 = 5005
	BiQuadThick_Constant_2 = 5006
	BiQuadThick_Factor_Thickness_2 = 5007
	BiQuadThick_Factor_Thickness_Squared_1 = 5008
	BiQuadThick_Factor_Thickness_Squared_2 = 5009
	QuadDiamThick_Low_Value = 6001
	QuadDiamThick_High_Value = 6002
	QuadDiamThick_Constant = 6003
	QuadDiamThick_Diameter = 6004
	QuadDiamThick_Diameter_Squared = 6005
	QuadDiamThick_Thickness_Over_D = 6006
	QuadDiamThick_Thickness_Over_D_Squared = 6007

class FamilyObjectUID(Enum):
	'''
	Values match UID of family_object_definition table.
	'''
	Default_Object = 0
	Top_Stack = 1
	Middle_Stack = 2
	Bottom_Stack = 3
	Top_Honeycomb_Face = 4
	Honeycomb_Core = 5
	Bottom_Honeycomb_Face = 6
	Top_Foam_Face = 7
	Foam_Core_Unstiffened = 8
	Bottom_Foam_Face = 9
	Corrugated_FwntTop_with_flange_Open_Span = 10
	Bwidth_Closed_Span = 11
	Wnt_face_only_Joint_Span_Corrugated = 12
	Wnt_Crown_Top_Crown_Top = 13
	Wnt_ComboTop_Bonded_Combo_Top = 14
	FwntAndWnt_ComboTop_Fastened_Flange_and_Face_Top = 15
	Bonded_FwntAndWnt_ComboTop_Bonded_Flange_and_Face_Top = 16
	B2_Web_Web_Corrugated = 17
	Wnb_Crown_bottom_Crown_Bottom = 18
	Wnb_Combo_bottom_Bonded_Combo = 19
	Wnb_face_only_Joint_Span_Corrugated = 20
	Sx_MinusOrDashIdk_Wnb_bottom_face_Bottom_Span = 21
	FwntAndWnt_Discontinuous_Spacing_Span_Corrugated = 22
	FwntTop_no_flange_Clear_Span = 25
	Wnt_face_only_Joint_Span_Uniaxial = 26
	Two_sided_Wnt_Top_Discontinuous_Flange_Top_Uniaxial = 27
	One_sided_Wnt_Top_Discontinuous_Flange_Top_Uniaxial = 28
	Two_sided_Wnt_ComboTop_Discontinuous_Bonded_Combo = 29
	One_sided_Wnt_ComboTop_Discontinuous_Bonded_Combo = 30
	Defunct_entire_span_FwntAndWnt_ComboTop_Continuous_Fastened_Flange_and_Face_Top = 31
	Entire_span_FwntAndWnt_ComboTop_Continuous_Bonded_Flange_and_Face_Top = 32
	B2_Web_Web_Uniaxial = 33
	Two_sided_Wnb_bottom_free_flange_Flange_Bottom_Uniaxial = 34
	One_sided_Wnb_bottom_free_flange_Flange_Bottom_Uniaxial = 35
	Two_sided_Wnb_Combo_bottom_Discontinuous_Bonded_Combo = 36
	Entire_span_FwnbAndWnb_ComboBot_Continuous_Bonded_Flange_and_Face_Bottom = 37
	Wnb_face_only_Joint_Span_Uniaxial = 38
	CleMinusOrDashIdkdash_Wnb_bottom_face_Bottom_Span = 39
	B2_Web_unsupported_Web = 40
	FwntAndWnt_Discontinuous_Spacing_Span_Uniaxial = 41
	Two_sided_Wnt_Top_Discontinuous_Flange_Top_OpenBeam = 43
	One_sided_Wnt_Top_Discontinuous_Flange_Top_OpenBeam = 44
	B2_Web_no_edges_free_Web = 45
	Two_sided_Wnb_bottom_free_flange_Flange_Bottom_OpenBeam = 46
	One_sided_Wnb_bottom_free_flange_Flange_Bottom_OpenBeam = 47
	B2_Web_one_edge_free_Web = 48
	TopFace_Zero_Grid = 49
	TopFace_Ninety_Grid = 50
	TopFace_OrthoGrid = 51
	BottomFace_OrthoGrid = 52
	TopFace_WaffleGrid = 53
	TopFace_AngleGrid = 54
	BottomFace_AngleGrid = 55
	TopFace_GeneralGrid = 56
	Web_Zero_Grid = 59
	Web_Ninety_Grid = 60
	Zero_Web = 61
	Ninety_Web = 62
	AngleWeb_Plus = 63
	AngleWeb_Minus = 64
	FwntTop_with_flange_Open_Span_Uniaxial = 65
	Curved_Wall = 66
	Foam_Core_Uniaxial = 67
	Open_Span = 68
	Frame_Web_Foam_Core_PRSEUS = 69
	Two_sided_Wnt_s_ComboTop_Discontinuous_Bonded_Combo = 70
	Two_sided_Wnt_f_ComboTop_Discontinuous_Bonded_Combo = 71
	B2_Web_Stringer_Web = 72
	Two_sided_Wnb_bottom_stringer_rod_and_laminate = 73
	B2_Web_Frame_Web = 74
	FwntAndWnt_Discontinuous_Spacing_Span_PRSEUS = 75
	Stringer_and_Frame_Bonded_Combo = 76
	Span_between_frames_for_rod_stiffened_panel = 77
	Web_upper = 233
	Web_lower = 234
	Mid_one_sided = 235
	SC_Foot = 236
	SC_Web = 237
	Rectangular_open_beam_Top_Wall = 843
	Rectangular_open_beam_Side_Wall = 845
	Rectangular_open_beam_Bottom_Wall = 846

class JointObject(Enum):
	'''
	Enum identifying the possible entities within a joint
	'''
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

class ProjectModelFormat(Enum):
	UNKNOWN = 0
	MscNastran = 1
	NeiNastran = 5
	NxNastran = 6
	Abaqus = 7
	Ansys = 8
	OptiStruct = 9

class SectionCutPropertyLocation(Enum):
	'''
	Centroid vs Origin
	'''
	Centroid = 0
	Origin = 1

