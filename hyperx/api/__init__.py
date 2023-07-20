from ..library import _api, _types

from ..api import types
from typing import TypeVar, Generic, overload
from enum import Enum
from System.Collections.Generic import List, IEnumerable, Dictionary
from System.Threading.Tasks import Task
from System import Guid, DateTime

from abc import ABC, abstractmethod

T = TypeVar('T')

def MakeCSharpIntList(ints: list[int]) -> List[int]:
	intsList = List[int]()
	if ints is not None:
		for thing in ints:
			if thing is not None:
				intsList.Add(thing)
	
	return intsList

class AnalysisResultToReturn(Enum):
	'''
	Used to specify which analysis result to return.
	'''
	Limit = 1
	Ultimate = 2
	Minimum = 3

class CollectionModificationStatus(Enum):
	'''
	Indicates that whether a collection was manipulated successfully.
	'''
	Success = 1
	DuplicateIdFailure = 2
	EntityMissingAddFailure = 3
	EntityMissingRemovalFailure = 4
	FemConnectionFailure = 5

class CreateDatabaseStatus(Enum):
	Success = 1
	TemplateNotFound = 2
	ImproperExtension = 3

class MaterialCreationStatus(Enum):
	'''
	Indicates that whether a Material was created successfully. 
            If not, this indicates why the material was not created.
	'''
	Success = 1
	DuplicateNameFailure = 2
	DuplicateFemIdFailure = 3
	MissingMaterialToCopy = 4

class DbForceUnit(Enum):
	Pounds = 1
	Newtons = 2
	Dekanewtons = 4

class DbLengthUnit(Enum):
	Inches = 1
	Feet = 2
	Meters = 3
	Centimeters = 4
	Millimeters = 5

class DbMassUnit(Enum):
	Pounds = 1
	Kilograms = 2
	Slinches = 4
	Slugs = 5
	Megagrams = 6

class DbTemperatureUnit(Enum):
	Fahrenheit = 1
	Rankine = 2
	Celsius = 3
	Kelvin = 4

class ProjectCreationStatus(Enum):
	'''
	Indicates that whether a Material was created successfully. 
            If not, this indicates why the material was not created.
	'''
	Success = 1
	Failure = 2
	DuplicateNameFailure = 3

class ProjectDeletionStatus(Enum):
	'''
	Indicates that whether a Material was created successfully. 
            If not, this indicates why the material was not created.
	'''
	Success = 1
	Failure = 2
	ProjectDoesNotExistFailure = 3
	ActiveProjectFailure = 4

class SetUnitsStatus(Enum):
	Success = 1
	Error = 2
	MixedUnitSystemError = 3

class PropertyAssignmentStatus(Enum):
	Success = 1
	Failure = 2
	FailureCollectionAssignment = 3
	PropertyIsNull = 4
	PropertyNotFoundInDb = 5
	EmptyCollection = 6

class RundeckCreationStatus(Enum):
	Success = 1
	InputFilePathAlreadyExists = 2
	ResultFilePathAlreadyExists = 3

class RundeckRemoveStatus(Enum):
	Success = 1
	InvalidId = 2
	CannotRemoveLastRundeck = 3
	CannotDeletePrimaryRundeck = 4
	RundeckNotFound = 5

class RundeckUpdateStatus(Enum):
	Success = 1
	InvalidId = 2
	IdDoesNotExist = 3
	RundeckAlreadyPrimary = 4
	InputPathInUse = 5
	ResultPathInUse = 6
	RundeckCommitFailure = 7

class ZoneIdUpdateStatus(Enum):
	Success = 1
	DuplicateIdFailure = 2

class UnitSystem(Enum):
	'''
	Unit system specified when starting a scripting Application.
	'''
	English = 1
	SI = 2


class IdEntity(ABC):
	'''
	Represents an entity with an ID.
	'''
	def __init__(self, idEntity: _api.IdEntity):
		self._Entity = idEntity

	@property
	def Id(self) -> int:
		return self._Entity.Id


class IdNameEntity(IdEntity):
	'''
	Represents an entity with an ID and Name.
	'''
	def __init__(self, idNameEntity: _api.IdNameEntity):
		self._Entity = idNameEntity

	@property
	def Name(self) -> str:
		return self._Entity.Name

class AnalysisDefinition(IdNameEntity):
	def __init__(self, analysisDefinition: _api.AnalysisDefinition):
		self._Entity = analysisDefinition

	@property
	def AnalysisId(self) -> int:
		return self._Entity.AnalysisId

	@property
	def Description(self) -> str:
		return self._Entity.Description


class Margin:
	'''
	Represents a Margin result.
	'''
	def __init__(self, margin: _api.Margin):
		self._Entity = margin

	@property
	def AdjustedMargin(self) -> float:
		return self._Entity.AdjustedMargin

	@property
	def IsFailureCode(self) -> bool:
		return self._Entity.IsFailureCode

	@property
	def IsInformationalCode(self) -> bool:
		return self._Entity.IsInformationalCode

	@property
	def MarginCode(self) -> types.MarginCode:
		return types.MarginCode[self._Entity.MarginCode.ToString()]


class AnalysisResult(ABC):
	'''
	Contains result information for an analysis
	'''
	def __init__(self, analysisResult: _api.AnalysisResult):
		self._Entity = analysisResult

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		'''
		Limit vs Ultimate loads.
		'''
		return types.LimitUltimate[self._Entity.LimitUltimate.ToString()]

	@property
	def LoadCaseId(self) -> int:
		return self._Entity.LoadCaseId

	@property
	def Margin(self) -> Margin:
		'''
		Represents a Margin result.
		'''
		return Margin(self._Entity.Margin)

	@property
	def AnalysisDefinition(self) -> AnalysisDefinition:
		return AnalysisDefinition(self._Entity.AnalysisDefinition)


class JointAnalysisResult(AnalysisResult):
	def __init__(self, jointAnalysisResult: _api.JointAnalysisResult):
		self._Entity = jointAnalysisResult

	@property
	def ObjectId(self) -> types.JointObject:
		'''
		Enum identifying the possible entities within a joint
		'''
		return types.JointObject[self._Entity.ObjectId.ToString()]


class ZoneAnalysisConceptResult(AnalysisResult):
	def __init__(self, zoneAnalysisConceptResult: _api.ZoneAnalysisConceptResult):
		self._Entity = zoneAnalysisConceptResult

	@property
	def ConceptId(self) -> types.FamilyConceptUID:
		'''
		Values match UID of family_concept_definition table.
		'''
		return types.FamilyConceptUID[self._Entity.ConceptId.ToString()]


class ZoneAnalysisObjectResult(AnalysisResult):
	def __init__(self, zoneAnalysisObjectResult: _api.ZoneAnalysisObjectResult):
		self._Entity = zoneAnalysisObjectResult

	@property
	def ObjectId(self) -> types.FamilyObjectUID:
		'''
		Values match UID of family_object_definition table.
		'''
		return types.FamilyObjectUID[self._Entity.ObjectId.ToString()]


class AssignableProperty(IdNameEntity):
	def __init__(self, assignableProperty: _api.AssignableProperty):
		self._Entity = assignableProperty


class AssignablePropertyWithFamilyCategory(AssignableProperty):
	def __init__(self, assignablePropertyWithFamilyCategory: _api.AssignablePropertyWithFamilyCategory):
		self._Entity = assignablePropertyWithFamilyCategory

	@property
	def FamilyCategory(self) -> types.FamilyCategory:
		'''
		Representative of the family_category table
		'''
		return types.FamilyCategory[self._Entity.FamilyCategory.ToString()]


class FailureObjectGroup(IdNameEntity):
	def __init__(self, failureObjectGroup: _api.FailureObjectGroup):
		self._Entity = failureObjectGroup

	@property
	def IsEnabled(self) -> bool:
		return self._Entity.IsEnabled

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		'''
		Limit vs Ultimate loads.
		'''
		return types.LimitUltimate[self._Entity.LimitUltimate.ToString()]

	@property
	def RequiredMargin(self) -> float:
		return self._Entity.RequiredMargin


class FailureSetting(IdNameEntity):
	'''
	Setting for a Failure Mode or a Failure Criteria.
	'''
	def __init__(self, failureSetting: _api.FailureSetting):
		self._Entity = failureSetting

	@property
	def CategoryId(self) -> int:
		return self._Entity.CategoryId

	@property
	def DataType(self) -> types.UserConstantDataType:
		return types.UserConstantDataType[self._Entity.DataType.ToString()]

	@property
	def DefaultValue(self) -> str:
		return self._Entity.DefaultValue

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def EnumValues(self) -> dict[int, str]:
		enumValuesDict = {}
		for kvp in self._Entity.EnumValues:
			enumValuesDict[int(kvp.Key)] = str(kvp.Value)

		return enumValuesDict

	@property
	def PackageId(self) -> int:
		return self._Entity.PackageId

	@property
	def PackageSettingId(self) -> int:
		return self._Entity.PackageSettingId

	@property
	def UID(self) -> Guid:
		return self._Entity.UID

	@property
	def Value(self) -> str:
		return self._Entity.Value


class IdEntityCol(Generic[T], ABC):
	def __init__(self, idEntityCol: _api.IdEntityCol):
		self._Entity = idEntityCol

	@property
	def IdEntityColList(self) -> tuple[IdEntity]:
		return tuple([IdEntity(idEntityCol) for idEntityCol in self._Entity])

	@property
	def Ids(self) -> tuple[int]:
		return tuple([int(int32) for int32 in self._Entity.Ids])

	def Contains(self, id: int) -> bool:
		return self._Entity.Contains(id)

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, id: int) -> T:
		return self._Entity.Get(id)

	def __getitem__(self, index: int):
		return self.IdEntityColList[index]

	def __iter__(self):
		yield from self.IdEntityColList

	def __len__(self):
		return len(self.IdEntityColList)


class IdNameEntityCol(IdEntityCol, Generic[T]):
	def __init__(self, idNameEntityCol: _api.IdNameEntityCol):
		self._Entity = idNameEntityCol
		self._CollectedClass = T

	@property
	def IdNameEntityColList(self) -> tuple[T]:
		return tuple([T(idNameEntityCol) for idNameEntityCol in self._Entity])

	@property
	def Names(self) -> tuple[str]:
		return tuple([str(string) for string in self._Entity.Names])

	@overload
	def Get(self, name: str) -> T: ...

	@overload
	def Get(self, id: int) -> T: ...

	def Get(self, item1 = None) -> T:
		if isinstance(item1, str):
			return self._Entity.Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.IdNameEntityColList[index]

	def __iter__(self):
		yield from self.IdNameEntityColList

	def __len__(self):
		return len(self.IdNameEntityColList)


class FailureObjectGroupCol(IdNameEntityCol[FailureObjectGroup]):
	def __init__(self, failureObjectGroupCol: _api.FailureObjectGroupCol):
		self._Entity = failureObjectGroupCol
		self._CollectedClass = FailureObjectGroup

	@property
	def FailureObjectGroupColList(self) -> tuple[FailureObjectGroup]:
		return tuple([FailureObjectGroup(failureObjectGroupCol) for failureObjectGroupCol in self._Entity])

	@overload
	def Get(self, name: str) -> FailureObjectGroup: ...

	@overload
	def Get(self, id: int) -> FailureObjectGroup: ...

	def Get(self, item1 = None) -> FailureObjectGroup:
		if isinstance(item1, str):
			return FailureObjectGroup(super().Get(item1))

		if isinstance(item1, int):
			return FailureObjectGroup(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.FailureObjectGroupColList[index]

	def __iter__(self):
		yield from self.FailureObjectGroupColList

	def __len__(self):
		return len(self.FailureObjectGroupColList)


class FailureSettingCol(IdNameEntityCol[FailureSetting]):
	def __init__(self, failureSettingCol: _api.FailureSettingCol):
		self._Entity = failureSettingCol
		self._CollectedClass = FailureSetting

	@property
	def FailureSettingColList(self) -> tuple[FailureSetting]:
		return tuple([FailureSetting(failureSettingCol) for failureSettingCol in self._Entity])

	@overload
	def Get(self, name: str) -> FailureSetting: ...

	@overload
	def Get(self, id: int) -> FailureSetting: ...

	def Get(self, item1 = None) -> FailureSetting:
		if isinstance(item1, str):
			return FailureSetting(super().Get(item1))

		if isinstance(item1, int):
			return FailureSetting(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.FailureSettingColList[index]

	def __iter__(self):
		yield from self.FailureSettingColList

	def __len__(self):
		return len(self.FailureSettingColList)


class FailureCriterion(IdNameEntity):
	def __init__(self, failureCriterion: _api.FailureCriterion):
		self._Entity = failureCriterion

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def IsEnabled(self) -> bool:
		return self._Entity.IsEnabled

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		return types.LimitUltimate[self._Entity.LimitUltimate.ToString()]

	@property
	def ObjectGroups(self) -> FailureObjectGroupCol:
		return FailureObjectGroupCol(self._Entity.ObjectGroups)

	@property
	def RequiredMargin(self) -> float:
		return self._Entity.RequiredMargin

	@property
	def Settings(self) -> FailureSettingCol:
		return FailureSettingCol(self._Entity.Settings)


class IdNameEntityRenameable(IdNameEntity):
	def __init__(self, idNameEntityRenameable: _api.IdNameEntityRenameable):
		self._Entity = idNameEntityRenameable

	def Rename(self, name: str) -> None:
		return self._Entity.Rename(name)


class FailureCriterionCol(IdNameEntityCol[FailureCriterion]):
	def __init__(self, failureCriterionCol: _api.FailureCriterionCol):
		self._Entity = failureCriterionCol
		self._CollectedClass = FailureCriterion

	@property
	def FailureCriterionColList(self) -> tuple[FailureCriterion]:
		return tuple([FailureCriterion(failureCriterionCol) for failureCriterionCol in self._Entity])

	@overload
	def Get(self, name: str) -> FailureCriterion: ...

	@overload
	def Get(self, id: int) -> FailureCriterion: ...

	def Get(self, item1 = None) -> FailureCriterion:
		if isinstance(item1, str):
			return FailureCriterion(super().Get(item1))

		if isinstance(item1, int):
			return FailureCriterion(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.FailureCriterionColList[index]

	def __iter__(self):
		yield from self.FailureCriterionColList

	def __len__(self):
		return len(self.FailureCriterionColList)


class FailureMode(IdNameEntityRenameable):
	def __init__(self, failureMode: _api.FailureMode):
		self._Entity = failureMode

	@property
	def AnalysisCategoryId(self) -> int:
		return self._Entity.AnalysisCategoryId

	@property
	def AnalysisCategoryName(self) -> str:
		return self._Entity.AnalysisCategoryName

	@property
	def Criteria(self) -> FailureCriterionCol:
		return FailureCriterionCol(self._Entity.Criteria)

	@property
	def Settings(self) -> FailureSettingCol:
		return FailureSettingCol(self._Entity.Settings)


class FailureModeCol(IdNameEntityCol[FailureMode]):
	def __init__(self, failureModeCol: _api.FailureModeCol):
		self._Entity = failureModeCol
		self._CollectedClass = FailureMode

	@property
	def FailureModeColList(self) -> tuple[FailureMode]:
		return tuple([FailureMode(failureModeCol) for failureModeCol in self._Entity])

	@overload
	def Get(self, name: str) -> FailureMode: ...

	@overload
	def Get(self, id: int) -> FailureMode: ...

	def Get(self, item1 = None) -> FailureMode:
		if isinstance(item1, str):
			return FailureMode(super().Get(item1))

		if isinstance(item1, int):
			return FailureMode(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.FailureModeColList[index]

	def __iter__(self):
		yield from self.FailureModeColList

	def __len__(self):
		return len(self.FailureModeColList)


class AnalysisProperty(AssignablePropertyWithFamilyCategory):
	def __init__(self, analysisProperty: _api.AnalysisProperty):
		self._Entity = analysisProperty

	@property
	def FailureModes(self) -> FailureModeCol:
		return FailureModeCol(self._Entity.FailureModes)

	@overload
	def AddFailureMode(self, id: int) -> None: ...

	@overload
	def AddFailureMode(self, ids: tuple[int]) -> None: ...

	@overload
	def RemoveFailureMode(self, id: int) -> None: ...

	@overload
	def RemoveFailureMode(self, ids: tuple[int]) -> None: ...

	def AddFailureMode(self, item1 = None) -> None:
		if isinstance(item1, int):
			return self._Entity.AddFailureMode(item1)

		if isinstance(item1, tuple):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return self._Entity.AddFailureMode(idsEnumerable)

		return self._Entity.AddFailureMode(item1)

	def RemoveFailureMode(self, item1 = None) -> None:
		if isinstance(item1, int):
			return self._Entity.RemoveFailureMode(item1)

		if isinstance(item1, tuple):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return self._Entity.RemoveFailureMode(idsEnumerable)

		return self._Entity.RemoveFailureMode(item1)


class DesignProperty(AssignablePropertyWithFamilyCategory):
	def __init__(self, designProperty: _api.DesignProperty):
		self._Entity = designProperty

	def Copy(self, newName: str) -> int:
		return self._Entity.Copy(newName)


class LoadProperty(AssignableProperty):
	def __init__(self, loadProperty: _api.LoadProperty):
		self._Entity = loadProperty


class DesignLoadSubcase(IdNameEntity):
	def __init__(self, designLoadSubcase: _api.DesignLoadSubcase):
		self._Entity = designLoadSubcase

	@property
	def RunDeckId(self) -> int:
		return self._Entity.RunDeckId

	@property
	def IsThermal(self) -> bool:
		return self._Entity.IsThermal

	@property
	def IsEditable(self) -> bool:
		return self._Entity.IsEditable

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def NastranSubcaseId(self) -> int:
		return self._Entity.NastranSubcaseId

	@property
	def NastranLoadId(self) -> int:
		return self._Entity.NastranLoadId

	@property
	def NastranSpcId(self) -> int:
		return self._Entity.NastranSpcId

	@property
	def AbaqusStepName(self) -> str:
		return self._Entity.AbaqusStepName

	@property
	def AbaqusLoadCaseName(self) -> str:
		return self._Entity.AbaqusLoadCaseName

	@property
	def AbaqusStepTime(self) -> float:
		return self._Entity.AbaqusStepTime

	@property
	def RunDeckOrder(self) -> int:
		return self._Entity.RunDeckOrder

	@property
	def SolutionType(self) -> types.FeaSolutionType:
		return types.FeaSolutionType[self._Entity.SolutionType.ToString()]


class DesignLoadSubcaseMultiplier(IdNameEntity):
	def __init__(self, designLoadSubcaseMultiplier: _api.DesignLoadSubcaseMultiplier):
		self._Entity = designLoadSubcaseMultiplier

	@property
	def LimitFactor(self) -> float:
		return self._Entity.LimitFactor

	@property
	def Subcase(self) -> DesignLoadSubcase:
		return DesignLoadSubcase(self._Entity.Subcase)

	@property
	def UltimateFactor(self) -> float:
		return self._Entity.UltimateFactor

	@property
	def Value(self) -> float:
		return self._Entity.Value


class DesignLoadSubcaseTemperature(IdNameEntity):
	def __init__(self, designLoadSubcaseTemperature: _api.DesignLoadSubcaseTemperature):
		self._Entity = designLoadSubcaseTemperature

	@property
	def HasTemperatureSubcase(self) -> bool:
		return self._Entity.HasTemperatureSubcase

	@property
	def Subcase(self) -> DesignLoadSubcase:
		return DesignLoadSubcase(self._Entity.Subcase)

	@property
	def TemperatureChoiceType(self) -> types.TemperatureChoiceType:
		'''
		Load Case Setting selection for analysis and initial temperature.
		'''
		return types.TemperatureChoiceType[self._Entity.TemperatureChoiceType.ToString()]

	@property
	def Value(self) -> float:
		return self._Entity.Value


class DesignLoadSubcaseMultiplierCol(IdNameEntityCol[DesignLoadSubcaseMultiplier]):
	def __init__(self, designLoadSubcaseMultiplierCol: _api.DesignLoadSubcaseMultiplierCol):
		self._Entity = designLoadSubcaseMultiplierCol
		self._CollectedClass = DesignLoadSubcaseMultiplier

	@property
	def DesignLoadSubcaseMultiplierColList(self) -> tuple[DesignLoadSubcaseMultiplier]:
		return tuple([DesignLoadSubcaseMultiplier(designLoadSubcaseMultiplierCol) for designLoadSubcaseMultiplierCol in self._Entity])

	@overload
	def Get(self, name: str) -> DesignLoadSubcaseMultiplier: ...

	@overload
	def Get(self, id: int) -> DesignLoadSubcaseMultiplier: ...

	def Get(self, item1 = None) -> DesignLoadSubcaseMultiplier:
		if isinstance(item1, str):
			return DesignLoadSubcaseMultiplier(super().Get(item1))

		if isinstance(item1, int):
			return DesignLoadSubcaseMultiplier(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.DesignLoadSubcaseMultiplierColList[index]

	def __iter__(self):
		yield from self.DesignLoadSubcaseMultiplierColList

	def __len__(self):
		return len(self.DesignLoadSubcaseMultiplierColList)


class DesignLoad(IdNameEntity):
	def __init__(self, designLoad: _api.DesignLoad):
		self._Entity = designLoad

	@property
	def AnalysisTemperature(self) -> DesignLoadSubcaseTemperature:
		return DesignLoadSubcaseTemperature(self._Entity.AnalysisTemperature)

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def InitialTemperature(self) -> DesignLoadSubcaseTemperature:
		return DesignLoadSubcaseTemperature(self._Entity.InitialTemperature)

	@property
	def IsActive(self) -> bool:
		return self._Entity.IsActive

	@property
	def IsEditable(self) -> bool:
		return self._Entity.IsEditable

	@property
	def IsVirtual(self) -> bool:
		return self._Entity.IsVirtual

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def SubcaseMultipliers(self) -> DesignLoadSubcaseMultiplierCol:
		return DesignLoadSubcaseMultiplierCol(self._Entity.SubcaseMultipliers)

	@property
	def Types(self) -> list[types.LoadCaseType]:
		return [types.LoadCaseType[loadCaseType.ToString()] for loadCaseType in self._Entity.Types]

	@property
	def UID(self) -> Guid:
		return self._Entity.UID


class Vector3d:
	'''
	Represents a readonly 3D vector.
	'''
	def __init__(self, vector3d: _api.Vector3d):
		self._Entity = vector3d

	def Create_Vector3d(x: float, y: float, z: float):
		return Vector3d(_api.Vector3d(x, y, z))

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@property
	def Z(self) -> float:
		return self._Entity.Z

	@overload
	def Equals(self, other) -> bool: ...

	@overload
	def Equals(self, obj) -> bool: ...

	def GetHashCode(self) -> int:
		return self._Entity.GetHashCode()

	def Equals(self, item1 = None) -> bool:
		if isinstance(item1, Vector3d):
			return self._Entity.Equals(item1._Entity)

		return self._Entity.Equals(item1._Entity)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)


class DiscreteField(IdNameEntityRenameable):
	'''
	Represents a table of discrete field data.
	'''
	def __init__(self, discreteField: _api.DiscreteField):
		self._Entity = discreteField

	@property
	def Columns(self) -> dict[int, str]:
		columnsDict = {}
		for kvp in self._Entity.Columns:
			columnsDict[int(kvp.Key)] = str(kvp.Value)

		return columnsDict

	@property
	def ColumnCount(self) -> int:
		return self._Entity.ColumnCount

	@property
	def DataType(self) -> types.DiscreteFieldDataType:
		'''
		Defines the type of data stored in a Discrete Field. Such as Vector, Scalar, String.
		'''
		return types.DiscreteFieldDataType[self._Entity.DataType.ToString()]

	@property
	def PhysicalEntityType(self) -> types.DiscreteFieldPhysicalEntityType:
		'''
		Defines the type of physical entity that a Discrete Field applies to, such as zone, element, joint, etc.
		'''
		return types.DiscreteFieldPhysicalEntityType[self._Entity.PhysicalEntityType.ToString()]

	@property
	def PointIds(self) -> list[Vector3d]:
		return [Vector3d(vector3d) for vector3d in self._Entity.PointIds]

	@property
	def RowCount(self) -> int:
		return self._Entity.RowCount

	@property
	def RowIds(self) -> list[int]:
		return [int32 for int32 in self._Entity.RowIds]

	def AddColumn(self, name: str) -> int:
		return self._Entity.AddColumn(name)

	def AddPointRow(self, pointId: Vector3d) -> None:
		return self._Entity.AddPointRow(pointId._Entity)

	@overload
	def ReadNumericCell(self, entityId: int, columnId: int) -> float: ...

	@overload
	def ReadNumericCell(self, pointId: Vector3d, columnId: int) -> float: ...

	@overload
	def ReadStringCell(self, entityId: int, columnId: int) -> str: ...

	@overload
	def ReadStringCell(self, pointId: Vector3d, columnId: int) -> str: ...

	def SetColumnName(self, columnId: int, name: str) -> None:
		return self._Entity.SetColumnName(columnId, name)

	@overload
	def SetNumericValue(self, entityId: int, columnId: int, value: float) -> None: ...

	@overload
	def SetNumericValue(self, pointId: Vector3d, columnId: int, value: float) -> None: ...

	@overload
	def SetStringValue(self, entityId: int, columnId: int, value: str) -> None: ...

	@overload
	def SetStringValue(self, pointId: Vector3d, columnId: int, value: str) -> None: ...

	def DeleteAllRows(self) -> None:
		'''
		Delete all rows for this discrete field.
		'''
		return self._Entity.DeleteAllRows()

	def DeleteColumn(self, columnId: int) -> None:
		return self._Entity.DeleteColumn(columnId)

	def DeletePointRow(self, pointId: Vector3d) -> None:
		return self._Entity.DeletePointRow(pointId._Entity)

	def DeleteRow(self, entityId: int) -> None:
		return self._Entity.DeleteRow(entityId)

	def DeleteRowsAndColumns(self) -> None:
		'''
		Delete all rows and columns for this discrete field.
		'''
		return self._Entity.DeleteRowsAndColumns()

	def ReadNumericCell(self, item1 = None, item2 = None) -> float:
		if isinstance(item1, int) and isinstance(item2, int):
			return self._Entity.ReadNumericCell(item1, item2)

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return self._Entity.ReadNumericCell(item1._Entity, item2)

		return self._Entity.ReadNumericCell(item1, item2)

	def ReadStringCell(self, item1 = None, item2 = None) -> str:
		if isinstance(item1, int) and isinstance(item2, int):
			return self._Entity.ReadStringCell(item1, item2)

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return self._Entity.ReadStringCell(item1._Entity, item2)

		return self._Entity.ReadStringCell(item1, item2)

	def SetNumericValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, int) and isinstance(item3, float):
			return self._Entity.SetNumericValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and isinstance(item3, float):
			return self._Entity.SetNumericValue(item1._Entity, item2, item3)

		return self._Entity.SetNumericValue(item1, item2, item3)

	def SetStringValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, int) and isinstance(item3, str):
			return self._Entity.SetStringValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and isinstance(item3, str):
			return self._Entity.SetStringValue(item1._Entity, item2, item3)

		return self._Entity.SetStringValue(item1, item2, item3)


class Centroid:
	def __init__(self, centroid: _api.Centroid):
		self._Entity = centroid

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@property
	def Z(self) -> float:
		return self._Entity.Z


class Element(IdEntity):
	def __init__(self, element: _api.Element):
		self._Entity = element

	@property
	def MarginOfSafety(self) -> float:
		return self._Entity.MarginOfSafety

	@property
	def Centroid(self) -> Centroid:
		return Centroid(self._Entity.Centroid)


class FailureModeCategory(IdNameEntity):
	def __init__(self, failureModeCategory: _api.FailureModeCategory):
		self._Entity = failureModeCategory

	@property
	def PackageId(self) -> int:
		return self._Entity.PackageId


class EntityWithAssignableProperties(IdNameEntityRenameable):
	def __init__(self, entityWithAssignableProperties: _api.EntityWithAssignableProperties):
		self._Entity = entityWithAssignableProperties

	@property
	def AssignedAnalysisProperty(self) -> AnalysisProperty:
		return AnalysisProperty(self._Entity.AssignedAnalysisProperty)

	@property
	def AssignedDesignProperty(self) -> DesignProperty:
		thisClass = type(self._Entity.AssignedDesignProperty).__name__
		givenClass = DesignProperty
		for subclass in DesignProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(self._Entity.AssignedDesignProperty)

	@property
	def AssignedLoadProperty(self) -> LoadProperty:
		return LoadProperty(self._Entity.AssignedLoadProperty)

	def AssignAnalysisProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignAnalysisProperty(id).ToString()]

	def AssignDesignProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignDesignProperty(id).ToString()]

	def AssignLoadProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignLoadProperty(id).ToString()]

	def AssignProperty(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignProperty(property._Entity).ToString()]


class AnalysisResultCol(Generic[T]):
	def __init__(self, analysisResultCol: _api.AnalysisResultCol):
		self._Entity = analysisResultCol

	@property
	def AnalysisResultColList(self) -> tuple[AnalysisResult]:
		return tuple([AnalysisResult(analysisResultCol) for analysisResultCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def __getitem__(self, index: int):
		return self.AnalysisResultColList[index]

	def __iter__(self):
		yield from self.AnalysisResultColList

	def __len__(self):
		return len(self.AnalysisResultColList)


class ZoneJointEntity(EntityWithAssignableProperties):
	'''
	Abstract base for a Zone or Joint.
	'''
	def __init__(self, zoneJointEntity: _api.ZoneJointEntity):
		self._Entity = zoneJointEntity

	@abstractmethod
	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())

	@abstractmethod
	def GetControllingResult(self) -> AnalysisResult:
		return AnalysisResult(self._Entity.GetControllingResult())

	@abstractmethod
	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetAllResults())


class Joint(ZoneJointEntity):
	def __init__(self, joint: _api.Joint):
		self._Entity = joint

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetAllResults())

	def GetControllingResult(self) -> AnalysisResult:
		return AnalysisResult(self._Entity.GetControllingResult())

	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())


class ZoneBase(ZoneJointEntity):
	'''
	Abstract for regular Zones and Panel Segments.
	'''
	def __init__(self, zoneBase: _api.ZoneBase):
		self._Entity = zoneBase

	@property
	def Centroid(self) -> Centroid:
		return Centroid(self._Entity.Centroid)

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def Weight(self) -> float:
		return self._Entity.Weight

	def RenumberZone(self, newId: int) -> ZoneIdUpdateStatus:
		return ZoneIdUpdateStatus[self._Entity.RenumberZone(newId).ToString()]

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetAllResults())

	def GetControllingResult(self) -> AnalysisResult:
		return AnalysisResult(self._Entity.GetControllingResult())

	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())


class ElementCol(IdEntityCol[Element]):
	def __init__(self, elementCol: _api.ElementCol):
		self._Entity = elementCol
		self._CollectedClass = Element

	@property
	def ElementColList(self) -> tuple[Element]:
		return tuple([Element(elementCol) for elementCol in self._Entity])

	def __getitem__(self, index: int):
		return self.ElementColList[index]

	def __iter__(self):
		yield from self.ElementColList

	def __len__(self):
		return len(self.ElementColList)


class PanelSegment(ZoneBase):
	def __init__(self, panelSegment: _api.PanelSegment):
		self._Entity = panelSegment

	@property
	def ElementsByObjectOrSkin(self) -> dict[types.DiscreteDefinitionType, ElementCol]:
		elementsByObjectOrSkinDict = {}
		for kvp in self._Entity.ElementsByObjectOrSkin:
			elementsByObjectOrSkinDict[types.DiscreteDefinitionType[kvp.Key.ToString()]] = ElementCol(kvp.Value)

		return elementsByObjectOrSkinDict

	@property
	def Skins(self) -> tuple[types.DiscreteDefinitionType]:
		return tuple([types.DiscreteDefinitionType(discreteDefinitionType) for discreteDefinitionType in self._Entity.Skins])

	@property
	def Objects(self) -> tuple[types.DiscreteDefinitionType]:
		return tuple([types.DiscreteDefinitionType(discreteDefinitionType) for discreteDefinitionType in self._Entity.Objects])

	@property
	def DiscreteTechnique(self) -> types.DiscreteTechnique:
		return types.DiscreteTechnique[self._Entity.DiscreteTechnique.ToString()]

	@property
	def LeftSkinZoneId(self) -> int:
		return self._Entity.LeftSkinZoneId

	@property
	def RightSkinZoneId(self) -> int:
		return self._Entity.RightSkinZoneId

	def GetElements(self, discreteDefinitionType: types.DiscreteDefinitionType) -> ElementCol:
		return ElementCol(self._Entity.GetElements(_types.DiscreteDefinitionType(discreteDefinitionType.value)))

	def SetObjectElements(self, discreteDefinitionType: types.DiscreteDefinitionType, elementIds: tuple[int]) -> None:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self._Entity.SetObjectElements(_types.DiscreteDefinitionType(discreteDefinitionType.value), elementIdsEnumerable)


class Zone(ZoneBase):
	'''
	Abstract for regular Zones (not Panel Segments).
	'''
	def __init__(self, zone: _api.Zone):
		self._Entity = zone

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self._Entity.Elements)

	def AddElements(self, elementIds: tuple[int]) -> None:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self._Entity.AddElements(elementIdsEnumerable)


class EntityWithAssignablePropertiesCol(IdNameEntityCol, Generic[T]):
	def __init__(self, entityWithAssignablePropertiesCol: _api.EntityWithAssignablePropertiesCol):
		self._Entity = entityWithAssignablePropertiesCol
		self._CollectedClass = T

	@property
	def EntityWithAssignablePropertiesColList(self) -> tuple[T]:
		return tuple([T(entityWithAssignablePropertiesCol) for entityWithAssignablePropertiesCol in self._Entity])

	def AssignPropertyToAll(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignPropertyToAll(property._Entity).ToString()]

	@overload
	def Get(self, name: str) -> T: ...

	@overload
	def Get(self, id: int) -> T: ...

	def Get(self, item1 = None) -> T:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.EntityWithAssignablePropertiesColList[index]

	def __iter__(self):
		yield from self.EntityWithAssignablePropertiesColList

	def __len__(self):
		return len(self.EntityWithAssignablePropertiesColList)


class JointCol(EntityWithAssignablePropertiesCol[Joint]):
	def __init__(self, jointCol: _api.JointCol):
		self._Entity = jointCol
		self._CollectedClass = Joint

	@property
	def JointColList(self) -> tuple[Joint]:
		return tuple([Joint(jointCol) for jointCol in self._Entity])

	@overload
	def Get(self, name: str) -> Joint: ...

	@overload
	def Get(self, id: int) -> Joint: ...

	def Get(self, item1 = None) -> Joint:
		if isinstance(item1, str):
			return Joint(super().Get(item1))

		if isinstance(item1, int):
			return Joint(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.JointColList[index]

	def __iter__(self):
		yield from self.JointColList

	def __len__(self):
		return len(self.JointColList)


class PanelSegmentCol(EntityWithAssignablePropertiesCol[PanelSegment]):
	def __init__(self, panelSegmentCol: _api.PanelSegmentCol):
		self._Entity = panelSegmentCol
		self._CollectedClass = PanelSegment

	@property
	def PanelSegmentColList(self) -> tuple[PanelSegment]:
		return tuple([PanelSegment(panelSegmentCol) for panelSegmentCol in self._Entity])

	@overload
	def Get(self, name: str) -> PanelSegment: ...

	@overload
	def Get(self, id: int) -> PanelSegment: ...

	def Get(self, item1 = None) -> PanelSegment:
		if isinstance(item1, str):
			return PanelSegment(super().Get(item1))

		if isinstance(item1, int):
			return PanelSegment(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.PanelSegmentColList[index]

	def __iter__(self):
		yield from self.PanelSegmentColList

	def __len__(self):
		return len(self.PanelSegmentColList)


class ZoneCol(EntityWithAssignablePropertiesCol[Zone]):
	def __init__(self, zoneCol: _api.ZoneCol):
		self._Entity = zoneCol
		self._CollectedClass = Zone

	@property
	def ZoneColList(self) -> tuple[Zone]:
		return tuple([Zone(zoneCol) for zoneCol in self._Entity])

	@overload
	def Get(self, name: str) -> Zone: ...

	@overload
	def Get(self, id: int) -> Zone: ...

	def Get(self, item1 = None) -> Zone:
		if isinstance(item1, str):
			return Zone(super().Get(item1))

		if isinstance(item1, int):
			return Zone(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.ZoneColList[index]

	def __iter__(self):
		yield from self.ZoneColList

	def __len__(self):
		return len(self.ZoneColList)


class ZoneJointContainer(IdNameEntityRenameable):
	'''
	Represents an entity that contains a collection of Zones and Joints.
	'''
	def __init__(self, zoneJointContainer: _api.ZoneJointContainer):
		self._Entity = zoneJointContainer

	@property
	def Centroid(self) -> Centroid:
		return Centroid(self._Entity.Centroid)

	@property
	def Joints(self) -> JointCol:
		return JointCol(self._Entity.Joints)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self._Entity.PanelSegments)

	@property
	def TotalBeamLength(self) -> float:
		return self._Entity.TotalBeamLength

	@property
	def TotalPanelArea(self) -> float:
		return self._Entity.TotalPanelArea

	@property
	def TotalZoneWeight(self) -> float:
		return self._Entity.TotalZoneWeight

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self._Entity.Zones)

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoints(self, joints: JointCol) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zones: ZoneCol) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segments: PanelSegmentCol) -> CollectionModificationStatus: ...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		return self._Entity.AddJoint(item1)

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.RemoveJoint(item1._Entity).ToString()]

		return self._Entity.RemoveJoint(item1)

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, JointCol):
			return CollectionModificationStatus[self._Entity.RemoveJoints(item1._Entity).ToString()]

		return self._Entity.RemoveJoints(jointIdsEnumerable)

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.AddZone(item1._Entity).ToString()]

		return self._Entity.AddZone(item1)

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.RemoveZone(item1._Entity).ToString()]

		return self._Entity.RemoveZone(item1)

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, ZoneCol):
			return CollectionModificationStatus[self._Entity.RemoveZones(item1._Entity).ToString()]

		return self._Entity.RemoveZones(zoneIdsEnumerable)

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		return self._Entity.AddPanelSegment(item1)

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1._Entity).ToString()]

		return self._Entity.RemovePanelSegment(item1)

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, PanelSegmentCol):
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(item1._Entity).ToString()]

		return self._Entity.RemovePanelSegments(segmentIdsEnumerable)


class FoamTemperature:
	'''
	Foam material temperature dependent properties.
	'''
	def __init__(self, foamTemperature: _api.FoamTemperature):
		self._Entity = foamTemperature

	@property
	def Temperature(self) -> float:
		return self._Entity.Temperature

	@property
	def Et(self) -> float:
		return self._Entity.Et

	@property
	def Ec(self) -> float:
		return self._Entity.Ec

	@property
	def G(self) -> float:
		return self._Entity.G

	@property
	def Ef(self) -> float:
		return self._Entity.Ef

	@property
	def Ftu(self) -> float:
		return self._Entity.Ftu

	@property
	def Fcu(self) -> float:
		return self._Entity.Fcu

	@property
	def Fsu(self) -> float:
		return self._Entity.Fsu

	@property
	def Ffu(self) -> float:
		return self._Entity.Ffu

	@property
	def K(self) -> float:
		return self._Entity.K

	@property
	def C(self) -> float:
		return self._Entity.C

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@Et.setter
	def Et(self, value: float) -> None:
		self._Entity.Et = value

	@Ec.setter
	def Ec(self, value: float) -> None:
		self._Entity.Ec = value

	@G.setter
	def G(self, value: float) -> None:
		self._Entity.G = value

	@Ef.setter
	def Ef(self, value: float) -> None:
		self._Entity.Ef = value

	@Ftu.setter
	def Ftu(self, value: float) -> None:
		self._Entity.Ftu = value

	@Fcu.setter
	def Fcu(self, value: float) -> None:
		self._Entity.Fcu = value

	@Fsu.setter
	def Fsu(self, value: float) -> None:
		self._Entity.Fsu = value

	@Ffu.setter
	def Ffu(self, value: float) -> None:
		self._Entity.Ffu = value

	@K.setter
	def K(self, value: float) -> None:
		self._Entity.K = value

	@C.setter
	def C(self, value: float) -> None:
		self._Entity.C = value


class Foam:
	'''
	Foam material.
	'''
	def __init__(self, foam: _api.Foam):
		self._Entity = foam

	@property
	def MaterialFamilyName(self) -> str:
		return self._Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Wet(self) -> bool:
		return self._Entity.Wet

	@property
	def Density(self) -> float:
		return self._Entity.Density

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def FemMaterialId(self) -> int:
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self._Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float:
		return self._Entity.BucklingStiffnessKnockdown

	@property
	def Absorption(self) -> float:
		return self._Entity.Absorption

	@property
	def Manufacturer(self) -> str:
		return self._Entity.Manufacturer

	@property
	def FoamTemperatureProperties(self) -> list[FoamTemperature]:
		return [FoamTemperature(foamTemperature) for foamTemperature in self._Entity.FoamTemperatureProperties]

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Wet.setter
	def Wet(self, value: bool) -> None:
		self._Entity.Wet = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float) -> None:
		self._Entity.Cost = value

	@BucklingStiffnessKnockdown.setter
	def BucklingStiffnessKnockdown(self, value: float) -> None:
		self._Entity.BucklingStiffnessKnockdown = value

	@Absorption.setter
	def Absorption(self, value: float) -> None:
		self._Entity.Absorption = value

	@Manufacturer.setter
	def Manufacturer(self, value: str) -> None:
		self._Entity.Manufacturer = value

	def AddTemperatureProperty(self, temperature: float, et: float = None, ec: float = None, g: float = None, ef: float = None, ftu: float = None, fcu: float = None, fsu: float = None, ffu: float = None, k: float = None, c: float = None) -> FoamTemperature:
		return FoamTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, g, ef, ftu, fcu, fsu, ffu, k, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> FoamTemperature:
		return FoamTemperature(self._Entity.GetTemperature(lookupTemperature))

	def Save(self) -> None:
		'''
		Save any changes to this foam material to the database.
		'''
		return self._Entity.Save()


class HoneycombTemperature:
	'''
	Honeycomb material temperature dependent properties.
	'''
	def __init__(self, honeycombTemperature: _api.HoneycombTemperature):
		self._Entity = honeycombTemperature

	@property
	def Temperature(self) -> float:
		return self._Entity.Temperature

	@property
	def Et(self) -> float:
		return self._Entity.Et

	@property
	def Ec(self) -> float:
		return self._Entity.Ec

	@property
	def Gw(self) -> float:
		return self._Entity.Gw

	@property
	def Gl(self) -> float:
		return self._Entity.Gl

	@property
	def Ftu(self) -> float:
		return self._Entity.Ftu

	@property
	def Fcus(self) -> float:
		return self._Entity.Fcus

	@property
	def Fcub(self) -> float:
		return self._Entity.Fcub

	@property
	def Fcuc(self) -> float:
		return self._Entity.Fcuc

	@property
	def Fsuw(self) -> float:
		return self._Entity.Fsuw

	@property
	def Fsul(self) -> float:
		return self._Entity.Fsul

	@property
	def SScfl(self) -> float:
		return self._Entity.SScfl

	@property
	def SScfh(self) -> float:
		return self._Entity.SScfh

	@property
	def Kl(self) -> float:
		return self._Entity.Kl

	@property
	def Kw(self) -> float:
		return self._Entity.Kw

	@property
	def Kt(self) -> float:
		return self._Entity.Kt

	@property
	def C(self) -> float:
		return self._Entity.C

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@Et.setter
	def Et(self, value: float) -> None:
		self._Entity.Et = value

	@Ec.setter
	def Ec(self, value: float) -> None:
		self._Entity.Ec = value

	@Gw.setter
	def Gw(self, value: float) -> None:
		self._Entity.Gw = value

	@Gl.setter
	def Gl(self, value: float) -> None:
		self._Entity.Gl = value

	@Ftu.setter
	def Ftu(self, value: float) -> None:
		self._Entity.Ftu = value

	@Fcus.setter
	def Fcus(self, value: float) -> None:
		self._Entity.Fcus = value

	@Fcub.setter
	def Fcub(self, value: float) -> None:
		self._Entity.Fcub = value

	@Fcuc.setter
	def Fcuc(self, value: float) -> None:
		self._Entity.Fcuc = value

	@Fsuw.setter
	def Fsuw(self, value: float) -> None:
		self._Entity.Fsuw = value

	@Fsul.setter
	def Fsul(self, value: float) -> None:
		self._Entity.Fsul = value

	@SScfl.setter
	def SScfl(self, value: float) -> None:
		self._Entity.SScfl = value

	@SScfh.setter
	def SScfh(self, value: float) -> None:
		self._Entity.SScfh = value

	@Kl.setter
	def Kl(self, value: float) -> None:
		self._Entity.Kl = value

	@Kw.setter
	def Kw(self, value: float) -> None:
		self._Entity.Kw = value

	@Kt.setter
	def Kt(self, value: float) -> None:
		self._Entity.Kt = value

	@C.setter
	def C(self, value: float) -> None:
		self._Entity.C = value


class Honeycomb:
	'''
	Honeycomb material.
	'''
	def __init__(self, honeycomb: _api.Honeycomb):
		self._Entity = honeycomb

	@property
	def MaterialFamilyName(self) -> str:
		return self._Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Wet(self) -> bool:
		return self._Entity.Wet

	@property
	def Density(self) -> float:
		return self._Entity.Density

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def FemMaterialId(self) -> int:
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self._Entity.Cost

	@property
	def CellSize(self) -> float:
		return self._Entity.CellSize

	@property
	def Manufacturer(self) -> str:
		return self._Entity.Manufacturer

	@property
	def HoneycombTemperatureProperties(self) -> list[HoneycombTemperature]:
		return [HoneycombTemperature(honeycombTemperature) for honeycombTemperature in self._Entity.HoneycombTemperatureProperties]

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Wet.setter
	def Wet(self, value: bool) -> None:
		self._Entity.Wet = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float) -> None:
		self._Entity.Cost = value

	@CellSize.setter
	def CellSize(self, value: float) -> None:
		self._Entity.CellSize = value

	@Manufacturer.setter
	def Manufacturer(self, value: str) -> None:
		self._Entity.Manufacturer = value

	def AddTemperatureProperty(self, temperature: float, et: float = None, ec: float = None, gw: float = None, gl: float = None, ftu: float = None, fcus: float = None, fcub: float = None, fcuc: float = None, fsuw: float = None, fsul: float = None, sScfl: float = None, sScfh: float = None, k1: float = None, k2: float = None, k3: float = None, c: float = None) -> HoneycombTemperature:
		return HoneycombTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, gw, gl, ftu, fcus, fcub, fcuc, fsuw, fsul, sScfl, sScfh, k1, k2, k3, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> HoneycombTemperature:
		return HoneycombTemperature(self._Entity.GetTemperature(lookupTemperature))

	def Save(self) -> None:
		'''
		Save any changes to this honeycomb material to the database.
		'''
		return self._Entity.Save()


class IsotropicTemperature:
	'''
	Isotropic material temperature dependent properties.
	'''
	def __init__(self, isotropicTemperature: _api.IsotropicTemperature):
		self._Entity = isotropicTemperature

	@property
	def Temperature(self) -> float:
		return self._Entity.Temperature

	@property
	def Et(self) -> float:
		return self._Entity.Et

	@property
	def Ec(self) -> float:
		return self._Entity.Ec

	@property
	def G(self) -> float:
		return self._Entity.G

	@property
	def n(self) -> float:
		return self._Entity.n

	@property
	def F02(self) -> float:
		return self._Entity.F02

	@property
	def FtuL(self) -> float:
		return self._Entity.FtuL

	@property
	def FtyL(self) -> float:
		return self._Entity.FtyL

	@property
	def FcyL(self) -> float:
		return self._Entity.FcyL

	@property
	def FtuLT(self) -> float:
		return self._Entity.FtuLT

	@property
	def FtyLT(self) -> float:
		return self._Entity.FtyLT

	@property
	def FcyLT(self) -> float:
		return self._Entity.FcyLT

	@property
	def Fsu(self) -> float:
		return self._Entity.Fsu

	@property
	def Fbru15(self) -> float:
		return self._Entity.Fbru15

	@property
	def Fbry15(self) -> float:
		return self._Entity.Fbry15

	@property
	def Fbru20(self) -> float:
		return self._Entity.Fbru20

	@property
	def Fbry20(self) -> float:
		return self._Entity.Fbry20

	@property
	def alpha(self) -> float:
		return self._Entity.alpha

	@property
	def K(self) -> float:
		return self._Entity.K

	@property
	def C(self) -> float:
		return self._Entity.C

	@property
	def etyL(self) -> float:
		return self._Entity.etyL

	@property
	def ecyL(self) -> float:
		return self._Entity.ecyL

	@property
	def etyLT(self) -> float:
		return self._Entity.etyLT

	@property
	def ecyLT(self) -> float:
		return self._Entity.ecyLT

	@property
	def esu(self) -> float:
		return self._Entity.esu

	@property
	def Fpadh(self) -> float:
		return self._Entity.Fpadh

	@property
	def Fsadh(self) -> float:
		return self._Entity.Fsadh

	@property
	def esadh(self) -> float:
		return self._Entity.esadh

	@property
	def cd(self) -> float:
		return self._Entity.cd

	@property
	def Ffwt(self) -> float:
		return self._Entity.Ffwt

	@property
	def Ffxz(self) -> float:
		return self._Entity.Ffxz

	@property
	def Ffyz(self) -> float:
		return self._Entity.Ffyz

	@property
	def FtFatigue(self) -> float:
		return self._Entity.FtFatigue

	@property
	def FcFatigue(self) -> float:
		return self._Entity.FcFatigue

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@Et.setter
	def Et(self, value: float) -> None:
		self._Entity.Et = value

	@Ec.setter
	def Ec(self, value: float) -> None:
		self._Entity.Ec = value

	@G.setter
	def G(self, value: float) -> None:
		self._Entity.G = value

	@n.setter
	def n(self, value: float) -> None:
		self._Entity.n = value

	@F02.setter
	def F02(self, value: float) -> None:
		self._Entity.F02 = value

	@FtuL.setter
	def FtuL(self, value: float) -> None:
		self._Entity.FtuL = value

	@FtyL.setter
	def FtyL(self, value: float) -> None:
		self._Entity.FtyL = value

	@FcyL.setter
	def FcyL(self, value: float) -> None:
		self._Entity.FcyL = value

	@FtuLT.setter
	def FtuLT(self, value: float) -> None:
		self._Entity.FtuLT = value

	@FtyLT.setter
	def FtyLT(self, value: float) -> None:
		self._Entity.FtyLT = value

	@FcyLT.setter
	def FcyLT(self, value: float) -> None:
		self._Entity.FcyLT = value

	@Fsu.setter
	def Fsu(self, value: float) -> None:
		self._Entity.Fsu = value

	@Fbru15.setter
	def Fbru15(self, value: float) -> None:
		self._Entity.Fbru15 = value

	@Fbry15.setter
	def Fbry15(self, value: float) -> None:
		self._Entity.Fbry15 = value

	@Fbru20.setter
	def Fbru20(self, value: float) -> None:
		self._Entity.Fbru20 = value

	@Fbry20.setter
	def Fbry20(self, value: float) -> None:
		self._Entity.Fbry20 = value

	@alpha.setter
	def alpha(self, value: float) -> None:
		self._Entity.alpha = value

	@K.setter
	def K(self, value: float) -> None:
		self._Entity.K = value

	@C.setter
	def C(self, value: float) -> None:
		self._Entity.C = value

	@etyL.setter
	def etyL(self, value: float) -> None:
		self._Entity.etyL = value

	@ecyL.setter
	def ecyL(self, value: float) -> None:
		self._Entity.ecyL = value

	@etyLT.setter
	def etyLT(self, value: float) -> None:
		self._Entity.etyLT = value

	@ecyLT.setter
	def ecyLT(self, value: float) -> None:
		self._Entity.ecyLT = value

	@esu.setter
	def esu(self, value: float) -> None:
		self._Entity.esu = value

	@Fpadh.setter
	def Fpadh(self, value: float) -> None:
		self._Entity.Fpadh = value

	@Fsadh.setter
	def Fsadh(self, value: float) -> None:
		self._Entity.Fsadh = value

	@esadh.setter
	def esadh(self, value: float) -> None:
		self._Entity.esadh = value

	@cd.setter
	def cd(self, value: float) -> None:
		self._Entity.cd = value

	@Ffwt.setter
	def Ffwt(self, value: float) -> None:
		self._Entity.Ffwt = value

	@Ffxz.setter
	def Ffxz(self, value: float) -> None:
		self._Entity.Ffxz = value

	@Ffyz.setter
	def Ffyz(self, value: float) -> None:
		self._Entity.Ffyz = value

	@FtFatigue.setter
	def FtFatigue(self, value: float) -> None:
		self._Entity.FtFatigue = value

	@FcFatigue.setter
	def FcFatigue(self, value: float) -> None:
		self._Entity.FcFatigue = value


class Isotropic:
	'''
	Isotropic material.
	'''
	def __init__(self, isotropic: _api.Isotropic):
		self._Entity = isotropic

	@property
	def MaterialFamilyName(self) -> str:
		return self._Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def Temper(self) -> str:
		return self._Entity.Temper

	@property
	def Basis(self) -> str:
		return self._Entity.Basis

	@property
	def Density(self) -> float:
		return self._Entity.Density

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def FemMaterialId(self) -> int:
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self._Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float:
		return self._Entity.BucklingStiffnessKnockdown

	@property
	def IsotropicTemperatureProperties(self) -> list[IsotropicTemperature]:
		return [IsotropicTemperature(isotropicTemperature) for isotropicTemperature in self._Entity.IsotropicTemperatureProperties]

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@Temper.setter
	def Temper(self, value: str) -> None:
		self._Entity.Temper = value

	@Basis.setter
	def Basis(self, value: str) -> None:
		self._Entity.Basis = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float) -> None:
		self._Entity.Cost = value

	@BucklingStiffnessKnockdown.setter
	def BucklingStiffnessKnockdown(self, value: float) -> None:
		self._Entity.BucklingStiffnessKnockdown = value

	def AddTemperatureProperty(self, temperature: float, et: float = None, ec: float = None, g: float = None, n: float = None, f02: float = None, ftuL: float = None, ftyL: float = None, fcyL: float = None, ftuLT: float = None, ftyLT: float = None, fcyLT: float = None, fsu: float = None, fbru15: float = None, fbry15: float = None, fbru20: float = None, fbry20: float = None, alpha: float = None, k: float = None, c: float = None, etyL: float = None, ecyL: float = None, etyLT: float = None, ecyLT: float = None, esu: float = None, fpadh: float = None, fsadh: float = None, esadh: float = None, cd: float = None, ffwt: float = None, ffxz: float = None, ffyz: float = None, ftFatigue: float = None, fcFatigue: float = None) -> IsotropicTemperature:
		return IsotropicTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, g, n, f02, ftuL, ftyL, fcyL, ftuLT, ftyLT, fcyLT, fsu, fbru15, fbry15, fbru20, fbry20, alpha, k, c, etyL, ecyL, etyLT, ecyLT, esu, fpadh, fsadh, esadh, cd, ffwt, ffxz, ffyz, ftFatigue, fcFatigue))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> IsotropicTemperature:
		return IsotropicTemperature(self._Entity.GetTemperature(lookupTemperature))

	def Save(self) -> None:
		'''
		Save any changes to this isotropic material to the database.
		'''
		return self._Entity.Save()


class OrthotropicCorrectionFactorBase(ABC):
	'''
	Orthotropic material correction factor.
	'''
	def __init__(self, orthotropicCorrectionFactorBase: _api.OrthotropicCorrectionFactorBase):
		self._Entity = orthotropicCorrectionFactorBase

	@property
	def CorrectionId(self) -> types.CorrectionId:
		'''
		Correction ID for a correction factor. (Columns in HyperX)
		'''
		return types.CorrectionId[self._Entity.CorrectionId.ToString()]

	@property
	def PropertyId(self) -> types.CorrectionProperty:
		'''
		Property name for a correction factor. (Rows in HyperX)
		'''
		return types.CorrectionProperty[self._Entity.PropertyId.ToString()]


class OrthotropicCorrectionFactorValue:
	'''
	Orthotropic material correction factor value.
	'''
	def __init__(self, orthotropicCorrectionFactorValue: _api.OrthotropicCorrectionFactorValue):
		self._Entity = orthotropicCorrectionFactorValue

	@property
	def Property(self) -> types.CorrectionProperty:
		'''
		Property name for a correction factor. (Rows in HyperX)
		'''
		return types.CorrectionProperty[self._Entity.Property.ToString()]

	@property
	def Correction(self) -> types.CorrectionId:
		'''
		Correction ID for a correction factor. (Columns in HyperX)
		'''
		return types.CorrectionId[self._Entity.Correction.ToString()]

	@property
	def Equation(self) -> types.CorrectionEquation:
		'''
		Equation for a correction factor.
		'''
		return types.CorrectionEquation[self._Entity.Equation.ToString()]

	@property
	def EquationParameter(self) -> types.EquationParameterId:
		'''
		Correction factor parameter names.
		'''
		return types.EquationParameterId[self._Entity.EquationParameter.ToString()]

	@property
	def Value(self) -> float:
		return self._Entity.Value

	@Value.setter
	def Value(self, value: float) -> None:
		self._Entity.Value = value


class OrthotropicEquationCorrectionFactor(OrthotropicCorrectionFactorBase):
	'''
	Represents an equation-based orthotropic material correction factor.
	'''
	def __init__(self, orthotropicEquationCorrectionFactor: _api.OrthotropicEquationCorrectionFactor):
		self._Entity = orthotropicEquationCorrectionFactor

	@property
	def Equation(self) -> types.CorrectionEquation:
		'''
		Equation for a correction factor.
		'''
		return types.CorrectionEquation[self._Entity.Equation.ToString()]

	@property
	def OrthotropicCorrectionValues(self) -> dict[types.EquationParameterId, OrthotropicCorrectionFactorValue]:
		orthotropicCorrectionValuesDict = {}
		for kvp in self._Entity.OrthotropicCorrectionValues:
			orthotropicCorrectionValuesDict[types.EquationParameterId[kvp.Key.ToString()]] = OrthotropicCorrectionFactorValue(kvp.Value)

		return orthotropicCorrectionValuesDict

	def AddCorrectionFactorValue(self, equationParameterName: types.EquationParameterId, valueToAdd: float) -> OrthotropicCorrectionFactorValue:
		return OrthotropicCorrectionFactorValue(self._Entity.AddCorrectionFactorValue(_types.EquationParameterId(equationParameterName.value), valueToAdd))


class TabularCorrectionFactorIndependentValue:
	'''
	Contains an independent value for a tabular correction factor row.
	'''
	def __init__(self, tabularCorrectionFactorIndependentValue: _api.TabularCorrectionFactorIndependentValue):
		self._Entity = tabularCorrectionFactorIndependentValue

	@property
	def BoolValue(self) -> bool:
		return self._Entity.BoolValue

	@property
	def DoubleValue(self) -> float:
		return self._Entity.DoubleValue

	@property
	def IntValue(self) -> int:
		return self._Entity.IntValue

	@property
	def ValueType(self) -> types.CorrectionValueType:
		'''
		Defines the type of the independent values on a tabular correction factor row.
		'''
		return types.CorrectionValueType[self._Entity.ValueType.ToString()]


class TabularCorrectionFactorRow:
	'''
	Row data for a tabular correction factor.
	'''
	def __init__(self, tabularCorrectionFactorRow: _api.TabularCorrectionFactorRow):
		self._Entity = tabularCorrectionFactorRow

	@property
	def DependentValue(self) -> float:
		return self._Entity.DependentValue

	@property
	def IndependentValues(self) -> dict[types.CorrectionIndependentDefinition, TabularCorrectionFactorIndependentValue]:
		return dict[types.CorrectionIndependentDefinition, TabularCorrectionFactorIndependentValue](self._Entity.IndependentValues)


class OrthotropicTabularCorrectionFactor(OrthotropicCorrectionFactorBase):
	'''
	Tabular correction factor.
	'''
	def __init__(self, orthotropicTabularCorrectionFactor: _api.OrthotropicTabularCorrectionFactor):
		self._Entity = orthotropicTabularCorrectionFactor

	@property
	def CorrectionFactorRows(self) -> dict[int, TabularCorrectionFactorRow]:
		correctionFactorRowsDict = {}
		for kvp in self._Entity.CorrectionFactorRows:
			correctionFactorRowsDict[int(kvp.Key)] = TabularCorrectionFactorRow(kvp.Value)

		return correctionFactorRowsDict

	@property
	def CorrectionIndependentDefinitions(self) -> set[types.CorrectionIndependentDefinition]:
		return {types.CorrectionIndependentDefinition(correctionIndependentDefinition) for correctionIndependentDefinition in self._Entity.CorrectionIndependentDefinitions}

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: float) -> None: ...

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: bool) -> None: ...

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: int) -> None: ...

	def SetKValue(self, correctionPointId: int, value: float) -> None:
		return self._Entity.SetKValue(correctionPointId, value)

	def SetIndependentValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, float):
			return self._Entity.SetIndependentValue(item1, item2, item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, bool):
			return self._Entity.SetIndependentValue(item1, item2, item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, int):
			return self._Entity.SetIndependentValue(item1, item2, item3)

		return self._Entity.SetIndependentValue(item1, item2, item3)


class OrthotropicAllowableCurvePoint:
	'''
	Represents a point on a laminate allowable curve.
	'''
	def __init__(self, orthotropicAllowableCurvePoint: _api.OrthotropicAllowableCurvePoint):
		self._Entity = orthotropicAllowableCurvePoint

	@property
	def Property_ID(self) -> types.AllowablePropertyName:
		'''
		Property name for a laminate allowable.
		'''
		return types.AllowablePropertyName[self._Entity.Property_ID.ToString()]

	@property
	def Temperature(self) -> float:
		return self._Entity.Temperature

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@Property_ID.setter
	def Property_ID(self, value: types.AllowablePropertyName) -> None:
		self._Entity.Property_ID = _types.AllowablePropertyName(value.value)

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@X.setter
	def X(self, value: float) -> None:
		self._Entity.X = value

	@Y.setter
	def Y(self, value: float) -> None:
		self._Entity.Y = value


class OrthotropicEffectiveLaminate:
	'''
	Orthotropic material effective laminate properties. Read-only from the API.
            Check if material is an effective laminate with orthotropic.IsEffectiveLaminate.
	'''
	def __init__(self, orthotropicEffectiveLaminate: _api.OrthotropicEffectiveLaminate):
		self._Entity = orthotropicEffectiveLaminate

	@property
	def Percent_tape_0(self) -> float:
		return self._Entity.Percent_tape_0

	@property
	def Percent_tape_90(self) -> float:
		return self._Entity.Percent_tape_90

	@property
	def Percent_tape_45(self) -> float:
		return self._Entity.Percent_tape_45

	@property
	def Percent_fabric_0(self) -> float:
		return self._Entity.Percent_fabric_0

	@property
	def Percent_fabric_90(self) -> float:
		return self._Entity.Percent_fabric_90

	@property
	def Percent_fabric_45(self) -> float:
		return self._Entity.Percent_fabric_45

	@property
	def Tape_Orthotropic(self) -> str:
		return self._Entity.Tape_Orthotropic

	@property
	def Fabric_Orthotropic(self) -> str:
		return self._Entity.Fabric_Orthotropic

	@property
	def Valid(self) -> bool:
		return self._Entity.Valid

	@property
	def Use_tape_allowables(self) -> bool:
		return self._Entity.Use_tape_allowables


class OrthotropicLaminateAllowable:
	'''
	Orthotropic material laminate allowable properties.
	'''
	def __init__(self, orthotropicLaminateAllowable: _api.OrthotropicLaminateAllowable):
		self._Entity = orthotropicLaminateAllowable

	@property
	def Property_ID(self) -> types.AllowablePropertyName:
		'''
		Property name for a laminate allowable.
		'''
		return types.AllowablePropertyName[self._Entity.Property_ID.ToString()]

	@property
	def Method_ID(self) -> types.AllowableMethodName:
		'''
		Method name for a laminate allowable.
		'''
		return types.AllowableMethodName[self._Entity.Method_ID.ToString()]

	@Property_ID.setter
	def Property_ID(self, value: types.AllowablePropertyName) -> None:
		self._Entity.Property_ID = _types.AllowablePropertyName(value.value)

	@Method_ID.setter
	def Method_ID(self, value: types.AllowableMethodName) -> None:
		self._Entity.Method_ID = _types.AllowableMethodName(value.value)


class OrthotropicTemperature:
	'''
	Orthotropic material temperature dependent properties.
	'''
	def __init__(self, orthotropicTemperature: _api.OrthotropicTemperature):
		self._Entity = orthotropicTemperature

	@property
	def Temperature(self) -> float:
		return self._Entity.Temperature

	@property
	def Et1(self) -> float:
		return self._Entity.Et1

	@property
	def Et2(self) -> float:
		return self._Entity.Et2

	@property
	def vt12(self) -> float:
		return self._Entity.vt12

	@property
	def Ec1(self) -> float:
		return self._Entity.Ec1

	@property
	def Ec2(self) -> float:
		return self._Entity.Ec2

	@property
	def vc12(self) -> float:
		return self._Entity.vc12

	@property
	def G12(self) -> float:
		return self._Entity.G12

	@property
	def G13(self) -> float:
		return self._Entity.G13

	@property
	def G23(self) -> float:
		return self._Entity.G23

	@property
	def Ftu1(self) -> float:
		return self._Entity.Ftu1

	@property
	def Ftu2(self) -> float:
		return self._Entity.Ftu2

	@property
	def Fcu1(self) -> float:
		return self._Entity.Fcu1

	@property
	def Fcu2(self) -> float:
		return self._Entity.Fcu2

	@property
	def Fsu12(self) -> float:
		return self._Entity.Fsu12

	@property
	def Fsu13(self) -> float:
		return self._Entity.Fsu13

	@property
	def Fsu23(self) -> float:
		return self._Entity.Fsu23

	@property
	def GIc(self) -> float:
		return self._Entity.GIc

	@property
	def alpha1(self) -> float:
		return self._Entity.alpha1

	@property
	def alpha2(self) -> float:
		return self._Entity.alpha2

	@property
	def K1(self) -> float:
		return self._Entity.K1

	@property
	def K2(self) -> float:
		return self._Entity.K2

	@property
	def C(self) -> float:
		return self._Entity.C

	@property
	def etu1(self) -> float:
		return self._Entity.etu1

	@property
	def etu2(self) -> float:
		return self._Entity.etu2

	@property
	def ecu1(self) -> float:
		return self._Entity.ecu1

	@property
	def ecu2(self) -> float:
		return self._Entity.ecu2

	@property
	def ecuoh(self) -> float:
		return self._Entity.ecuoh

	@property
	def ecuai(self) -> float:
		return self._Entity.ecuai

	@property
	def esu12(self) -> float:
		return self._Entity.esu12

	@property
	def Ftu3(self) -> float:
		return self._Entity.Ftu3

	@property
	def GIIc(self) -> float:
		return self._Entity.GIIc

	@property
	def d0Tension(self) -> float:
		return self._Entity.d0Tension

	@property
	def cd(self) -> float:
		return self._Entity.cd

	@property
	def d0Compression(self) -> float:
		return self._Entity.d0Compression

	@property
	def TLt(self) -> float:
		return self._Entity.TLt

	@property
	def TLc(self) -> float:
		return self._Entity.TLc

	@property
	def TTt(self) -> float:
		return self._Entity.TTt

	@property
	def TTc(self) -> float:
		return self._Entity.TTc

	@property
	def OrthotropicAllowableCurvePoints(self) -> list[OrthotropicAllowableCurvePoint]:
		return [OrthotropicAllowableCurvePoint(orthotropicAllowableCurvePoint) for orthotropicAllowableCurvePoint in self._Entity.OrthotropicAllowableCurvePoints]

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value

	@Et1.setter
	def Et1(self, value: float) -> None:
		self._Entity.Et1 = value

	@Et2.setter
	def Et2(self, value: float) -> None:
		self._Entity.Et2 = value

	@vt12.setter
	def vt12(self, value: float) -> None:
		self._Entity.vt12 = value

	@Ec1.setter
	def Ec1(self, value: float) -> None:
		self._Entity.Ec1 = value

	@Ec2.setter
	def Ec2(self, value: float) -> None:
		self._Entity.Ec2 = value

	@vc12.setter
	def vc12(self, value: float) -> None:
		self._Entity.vc12 = value

	@G12.setter
	def G12(self, value: float) -> None:
		self._Entity.G12 = value

	@G13.setter
	def G13(self, value: float) -> None:
		self._Entity.G13 = value

	@G23.setter
	def G23(self, value: float) -> None:
		self._Entity.G23 = value

	@Ftu1.setter
	def Ftu1(self, value: float) -> None:
		self._Entity.Ftu1 = value

	@Ftu2.setter
	def Ftu2(self, value: float) -> None:
		self._Entity.Ftu2 = value

	@Fcu1.setter
	def Fcu1(self, value: float) -> None:
		self._Entity.Fcu1 = value

	@Fcu2.setter
	def Fcu2(self, value: float) -> None:
		self._Entity.Fcu2 = value

	@Fsu12.setter
	def Fsu12(self, value: float) -> None:
		self._Entity.Fsu12 = value

	@Fsu13.setter
	def Fsu13(self, value: float) -> None:
		self._Entity.Fsu13 = value

	@Fsu23.setter
	def Fsu23(self, value: float) -> None:
		self._Entity.Fsu23 = value

	@GIc.setter
	def GIc(self, value: float) -> None:
		self._Entity.GIc = value

	@alpha1.setter
	def alpha1(self, value: float) -> None:
		self._Entity.alpha1 = value

	@alpha2.setter
	def alpha2(self, value: float) -> None:
		self._Entity.alpha2 = value

	@K1.setter
	def K1(self, value: float) -> None:
		self._Entity.K1 = value

	@K2.setter
	def K2(self, value: float) -> None:
		self._Entity.K2 = value

	@C.setter
	def C(self, value: float) -> None:
		self._Entity.C = value

	@etu1.setter
	def etu1(self, value: float) -> None:
		self._Entity.etu1 = value

	@etu2.setter
	def etu2(self, value: float) -> None:
		self._Entity.etu2 = value

	@ecu1.setter
	def ecu1(self, value: float) -> None:
		self._Entity.ecu1 = value

	@ecu2.setter
	def ecu2(self, value: float) -> None:
		self._Entity.ecu2 = value

	@ecuoh.setter
	def ecuoh(self, value: float) -> None:
		self._Entity.ecuoh = value

	@ecuai.setter
	def ecuai(self, value: float) -> None:
		self._Entity.ecuai = value

	@esu12.setter
	def esu12(self, value: float) -> None:
		self._Entity.esu12 = value

	@Ftu3.setter
	def Ftu3(self, value: float) -> None:
		self._Entity.Ftu3 = value

	@GIIc.setter
	def GIIc(self, value: float) -> None:
		self._Entity.GIIc = value

	@d0Tension.setter
	def d0Tension(self, value: float) -> None:
		self._Entity.d0Tension = value

	@cd.setter
	def cd(self, value: float) -> None:
		self._Entity.cd = value

	@d0Compression.setter
	def d0Compression(self, value: float) -> None:
		self._Entity.d0Compression = value

	@TLt.setter
	def TLt(self, value: float) -> None:
		self._Entity.TLt = value

	@TLc.setter
	def TLc(self, value: float) -> None:
		self._Entity.TLc = value

	@TTt.setter
	def TTt(self, value: float) -> None:
		self._Entity.TTt = value

	@TTc.setter
	def TTc(self, value: float) -> None:
		self._Entity.TTc = value

	def AddCurvePoint(self, property: types.AllowablePropertyName, x: float, y: float) -> OrthotropicAllowableCurvePoint:
		return OrthotropicAllowableCurvePoint(self._Entity.AddCurvePoint(_types.AllowablePropertyName(property.value), x, y))

	def DeleteCurvePoint(self, property: types.AllowablePropertyName, x: float) -> bool:
		return self._Entity.DeleteCurvePoint(_types.AllowablePropertyName(property.value), x)

	def GetCurvePoint(self, property: types.AllowablePropertyName, x: float) -> OrthotropicAllowableCurvePoint:
		return OrthotropicAllowableCurvePoint(self._Entity.GetCurvePoint(_types.AllowablePropertyName(property.value), x))


class Orthotropic:
	'''
	Orthotropic material.
	'''
	def __init__(self, orthotropic: _api.Orthotropic):
		self._Entity = orthotropic

	@property
	def MaterialFamilyName(self) -> str:
		return self._Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self._Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Form(self) -> str:
		return self._Entity.Form

	@property
	def Specification(self) -> str:
		return self._Entity.Specification

	@property
	def Basis(self) -> str:
		return self._Entity.Basis

	@property
	def Wet(self) -> bool:
		return self._Entity.Wet

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def Density(self) -> float:
		return self._Entity.Density

	@property
	def FiberVolume(self) -> float:
		return self._Entity.FiberVolume

	@property
	def GlassTransition(self) -> float:
		return self._Entity.GlassTransition

	@property
	def Manufacturer(self) -> str:
		return self._Entity.Manufacturer

	@property
	def Processes(self) -> str:
		return self._Entity.Processes

	@property
	def MaterialDescription(self) -> str:
		return self._Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self._Entity.UserNote

	@property
	def BendingCorrectionFactor(self) -> float:
		return self._Entity.BendingCorrectionFactor

	@property
	def FemMaterialId(self) -> int:
		return self._Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self._Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float:
		return self._Entity.BucklingStiffnessKnockdown

	@property
	def OrthotropicTemperatureProperties(self) -> list[OrthotropicTemperature]:
		return [OrthotropicTemperature(orthotropicTemperature) for orthotropicTemperature in self._Entity.OrthotropicTemperatureProperties]

	@property
	def OrthotropicLaminateAllowables(self) -> list[OrthotropicLaminateAllowable]:
		return [OrthotropicLaminateAllowable(orthotropicLaminateAllowable) for orthotropicLaminateAllowable in self._Entity.OrthotropicLaminateAllowables]

	@property
	def OrthotropicEffectiveLaminate(self) -> OrthotropicEffectiveLaminate:
		'''
		Orthotropic material effective laminate properties. Read-only from the API.
            Check if material is an effective laminate with orthotropic.IsEffectiveLaminate.
		'''
		return OrthotropicEffectiveLaminate(self._Entity.OrthotropicEffectiveLaminate)

	@property
	def OrthotropicEquationCorrectionFactors(self) -> dict[tuple[types.CorrectionProperty, types.CorrectionId], OrthotropicEquationCorrectionFactor]:
		orthotropicEquationCorrectionFactorsDict = {}
		for kvp in self._Entity.OrthotropicEquationCorrectionFactors:
			orthotropicEquationCorrectionFactorsDict[tuple[types.CorrectionProperty, types.CorrectionId](kvp.Key)] = OrthotropicEquationCorrectionFactor(kvp.Value)

		return orthotropicEquationCorrectionFactorsDict

	@property
	def OrthotropicTabularCorrectionFactors(self) -> dict[tuple[types.CorrectionProperty, types.CorrectionId], OrthotropicTabularCorrectionFactor]:
		orthotropicTabularCorrectionFactorsDict = {}
		for kvp in self._Entity.OrthotropicTabularCorrectionFactors:
			orthotropicTabularCorrectionFactorsDict[tuple[types.CorrectionProperty, types.CorrectionId](kvp.Key)] = OrthotropicTabularCorrectionFactor(kvp.Value)

		return orthotropicTabularCorrectionFactorsDict

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@Form.setter
	def Form(self, value: str) -> None:
		self._Entity.Form = value

	@Specification.setter
	def Specification(self, value: str) -> None:
		self._Entity.Specification = value

	@Basis.setter
	def Basis(self, value: str) -> None:
		self._Entity.Basis = value

	@Wet.setter
	def Wet(self, value: bool) -> None:
		self._Entity.Wet = value

	@Thickness.setter
	def Thickness(self, value: float) -> None:
		self._Entity.Thickness = value

	@Density.setter
	def Density(self, value: float) -> None:
		self._Entity.Density = value

	@FiberVolume.setter
	def FiberVolume(self, value: float) -> None:
		self._Entity.FiberVolume = value

	@GlassTransition.setter
	def GlassTransition(self, value: float) -> None:
		self._Entity.GlassTransition = value

	@Manufacturer.setter
	def Manufacturer(self, value: str) -> None:
		self._Entity.Manufacturer = value

	@Processes.setter
	def Processes(self, value: str) -> None:
		self._Entity.Processes = value

	@MaterialDescription.setter
	def MaterialDescription(self, value: str) -> None:
		self._Entity.MaterialDescription = value

	@UserNote.setter
	def UserNote(self, value: str) -> None:
		self._Entity.UserNote = value

	@BendingCorrectionFactor.setter
	def BendingCorrectionFactor(self, value: float) -> None:
		self._Entity.BendingCorrectionFactor = value

	@FemMaterialId.setter
	def FemMaterialId(self, value: int) -> None:
		self._Entity.FemMaterialId = value

	@Cost.setter
	def Cost(self, value: float) -> None:
		self._Entity.Cost = value

	@BucklingStiffnessKnockdown.setter
	def BucklingStiffnessKnockdown(self, value: float) -> None:
		self._Entity.BucklingStiffnessKnockdown = value

	def AddTemperatureProperty(self, temperature: float, et1: float = None, et2: float = None, vt12: float = None, ec1: float = None, ec2: float = None, vc12: float = None, g12: float = None, ftu1: float = None, ftu2: float = None, fcu1: float = None, fcu2: float = None, fsu12: float = None, alpha1: float = None, alpha2: float = None, etu1: float = None, etu2: float = None, ecu1: float = None, ecu2: float = None, esu12: float = None) -> OrthotropicTemperature:
		return OrthotropicTemperature(self._Entity.AddTemperatureProperty(temperature, et1, et2, vt12, ec1, ec2, vc12, g12, ftu1, ftu2, fcu1, fcu2, fsu12, alpha1, alpha2, etu1, etu2, ecu1, ecu2, esu12))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> OrthotropicTemperature:
		return OrthotropicTemperature(self._Entity.GetTemperature(lookupTemperature))

	def IsEffectiveLaminate(self) -> bool:
		'''
		Returns true if this material is an effective laminate.
		'''
		return self._Entity.IsEffectiveLaminate()

	def HasLaminateAllowable(self, property: types.AllowablePropertyName) -> bool:
		return self._Entity.HasLaminateAllowable(_types.AllowablePropertyName(property.value))

	def AddLaminateAllowable(self, property: types.AllowablePropertyName, method: types.AllowableMethodName) -> OrthotropicLaminateAllowable:
		return OrthotropicLaminateAllowable(self._Entity.AddLaminateAllowable(_types.AllowablePropertyName(property.value), _types.AllowableMethodName(method.value)))

	def GetLaminateAllowable(self, lookupAllowableProperty: types.AllowablePropertyName) -> OrthotropicLaminateAllowable:
		return OrthotropicLaminateAllowable(self._Entity.GetLaminateAllowable(_types.AllowablePropertyName(lookupAllowableProperty.value)))

	def AddEquationCorrectionFactor(self, propertyId: types.CorrectionProperty, correctionId: types.CorrectionId, equationId: types.CorrectionEquation) -> OrthotropicEquationCorrectionFactor:
		return OrthotropicEquationCorrectionFactor(self._Entity.AddEquationCorrectionFactor(_types.CorrectionProperty(propertyId.value), _types.CorrectionId(correctionId.value), _types.CorrectionEquation(equationId.value)))

	def GetEquationCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicEquationCorrectionFactor:
		return OrthotropicEquationCorrectionFactor(self._Entity.GetEquationCorrectionFactor(_types.CorrectionProperty(property.value), _types.CorrectionId(correction.value)))

	def GetTabularCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicTabularCorrectionFactor:
		return OrthotropicTabularCorrectionFactor(self._Entity.GetTabularCorrectionFactor(_types.CorrectionProperty(property.value), _types.CorrectionId(correction.value)))

	def Save(self) -> None:
		'''
		Save any changes to this orthotropic material to the database.
		'''
		return self._Entity.Save()


class Vector2d:
	'''
	Represents a readonly 2D vector.
	'''
	def __init__(self, vector2d: _api.Vector2d):
		self._Entity = vector2d

	def Create_Vector2d(x: float, y: float):
		return Vector2d(_api.Vector2d(x, y))

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@overload
	def Equals(self, other) -> bool: ...

	@overload
	def Equals(self, obj) -> bool: ...

	def GetHashCode(self) -> int:
		return self._Entity.GetHashCode()

	def Equals(self, item1 = None) -> bool:
		if isinstance(item1, Vector2d):
			return self._Entity.Equals(item1._Entity)

		return self._Entity.Equals(item1._Entity)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)


class ElementSet(IdNameEntity):
	'''
	A set of elements defined in the input file.
	'''
	def __init__(self, elementSet: _api.ElementSet):
		self._Entity = elementSet

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self._Entity.Elements)


class FemProperty(IdNameEntity):
	'''
	A property description.
	'''
	def __init__(self, femProperty: _api.FemProperty):
		self._Entity = femProperty

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self._Entity.Elements)

	@property
	def FemType(self) -> types.FemType:
		return types.FemType[self._Entity.FemType.ToString()]


class ElementSetCol(IdEntityCol[ElementSet]):
	def __init__(self, elementSetCol: _api.ElementSetCol):
		self._Entity = elementSetCol
		self._CollectedClass = ElementSet

	@property
	def ElementSetColList(self) -> tuple[ElementSet]:
		return tuple([ElementSet(elementSetCol) for elementSetCol in self._Entity])

	def __getitem__(self, index: int):
		return self.ElementSetColList[index]

	def __iter__(self):
		yield from self.ElementSetColList

	def __len__(self):
		return len(self.ElementSetColList)


class FemPropertyCol(IdEntityCol[FemProperty]):
	def __init__(self, femPropertyCol: _api.FemPropertyCol):
		self._Entity = femPropertyCol
		self._CollectedClass = FemProperty

	@property
	def FemPropertyColList(self) -> tuple[FemProperty]:
		return tuple([FemProperty(femPropertyCol) for femPropertyCol in self._Entity])

	def __getitem__(self, index: int):
		return self.FemPropertyColList[index]

	def __iter__(self):
		yield from self.FemPropertyColList

	def __len__(self):
		return len(self.FemPropertyColList)


class FemDataSet:
	def __init__(self, femDataSet: _api.FemDataSet):
		self._Entity = femDataSet

	@property
	def FemProperties(self) -> FemPropertyCol:
		return FemPropertyCol(self._Entity.FemProperties)

	@property
	def ElementSets(self) -> ElementSetCol:
		return ElementSetCol(self._Entity.ElementSets)


class Ply(IdNameEntity):
	def __init__(self, ply: _api.Ply):
		self._Entity = ply

	@property
	def InnerCurves(self) -> list[int]:
		return [int32 for int32 in self._Entity.InnerCurves]

	@property
	def OuterCurves(self) -> list[int]:
		return [int32 for int32 in self._Entity.OuterCurves]

	@property
	def FiberDirectionCurves(self) -> list[int]:
		return [int32 for int32 in self._Entity.FiberDirectionCurves]

	@property
	def Area(self) -> float:
		return self._Entity.Area

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self._Entity.Elements)

	@property
	def MaterialId(self) -> int:
		return self._Entity.MaterialId

	@property
	def Orientation(self) -> int:
		return self._Entity.Orientation

	@property
	def Sequence(self) -> int:
		return self._Entity.Sequence

	@property
	def StructureId(self) -> int:
		return self._Entity.StructureId

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness


class Rundeck(IdEntity):
	def __init__(self, rundeck: _api.Rundeck):
		self._Entity = rundeck

	@property
	def InputFilePath(self) -> str:
		return self._Entity.InputFilePath

	@property
	def IsPrimary(self) -> bool:
		return self._Entity.IsPrimary

	@property
	def ResultFilePath(self) -> str:
		return self._Entity.ResultFilePath

	def SetInputFilePath(self, filepath: str) -> RundeckUpdateStatus:
		return RundeckUpdateStatus[self._Entity.SetInputFilePath(filepath).ToString()]

	def SetResultFilePath(self, filepath: str) -> RundeckUpdateStatus:
		return RundeckUpdateStatus[self._Entity.SetResultFilePath(filepath).ToString()]


class BeamLoads:
	def __init__(self, beamLoads: _api.BeamLoads):
		self._Entity = beamLoads

	@property
	def AxialForce(self) -> float:
		return self._Entity.AxialForce

	@property
	def MomentX(self) -> float:
		return self._Entity.MomentX

	@property
	def MomentY(self) -> float:
		return self._Entity.MomentY

	@property
	def ShearX(self) -> float:
		return self._Entity.ShearX

	@property
	def ShearY(self) -> float:
		return self._Entity.ShearY

	@property
	def Torque(self) -> float:
		return self._Entity.Torque


class SectionCut(IdNameEntity):
	def __init__(self, sectionCut: _api.SectionCut):
		self._Entity = sectionCut

	@property
	def ReferencePoint(self) -> types.SectionCutPropertyLocation:
		'''
		Centroid vs Origin
		'''
		return types.SectionCutPropertyLocation[self._Entity.ReferencePoint.ToString()]

	@property
	def HorizontalVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		return Vector3d(self._Entity.HorizontalVector)

	@property
	def NormalVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		return Vector3d(self._Entity.NormalVector)

	@property
	def OriginVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		return Vector3d(self._Entity.OriginVector)

	@property
	def VerticalVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		return Vector3d(self._Entity.VerticalVector)

	@property
	def MaxAngleBound(self) -> float:
		return self._Entity.MaxAngleBound

	@property
	def MinAngleBound(self) -> float:
		return self._Entity.MinAngleBound

	@property
	def MinStiffnessEihh(self) -> float:
		return self._Entity.MinStiffnessEihh

	@property
	def MinStiffnessEivv(self) -> float:
		return self._Entity.MinStiffnessEivv

	@property
	def MinStiffnessGJ(self) -> float:
		return self._Entity.MinStiffnessGJ

	@property
	def ZoneStiffnessDistribution(self) -> float:
		return self._Entity.ZoneStiffnessDistribution

	@property
	def CN_hmax(self) -> float:
		return self._Entity.CN_hmax

	@property
	def CN_hmin(self) -> float:
		return self._Entity.CN_hmin

	@property
	def CN_vmax(self) -> float:
		return self._Entity.CN_vmax

	@property
	def CN_vmin(self) -> float:
		return self._Entity.CN_vmin

	@property
	def CQ_hmax(self) -> float:
		return self._Entity.CQ_hmax

	@property
	def CQ_hmin(self) -> float:
		return self._Entity.CQ_hmin

	@property
	def CQ_vmax(self) -> float:
		return self._Entity.CQ_vmax

	@property
	def CQ_vmin(self) -> float:
		return self._Entity.CQ_vmin

	@property
	def CG(self) -> Vector2d:
		'''
		Represents a readonly 2D vector.
		'''
		return Vector2d(self._Entity.CG)

	@property
	def CN(self) -> Vector2d:
		'''
		Represents a readonly 2D vector.
		'''
		return Vector2d(self._Entity.CN)

	@property
	def CQ(self) -> Vector2d:
		'''
		Represents a readonly 2D vector.
		'''
		return Vector2d(self._Entity.CQ)

	@property
	def EnclosedArea(self) -> float:
		return self._Entity.EnclosedArea

	@property
	def NumberOfCells(self) -> int:
		return self._Entity.NumberOfCells

	@property
	def EIhh(self) -> float:
		return self._Entity.EIhh

	@property
	def EIhv(self) -> float:
		return self._Entity.EIhv

	@property
	def EIvv(self) -> float:
		return self._Entity.EIvv

	@property
	def GJ(self) -> float:
		return self._Entity.GJ

	@property
	def EA(self) -> float:
		return self._Entity.EA

	@property
	def EImax(self) -> float:
		return self._Entity.EImax

	@property
	def EImin(self) -> float:
		return self._Entity.EImin

	@property
	def PrincipalAngle(self) -> float:
		return self._Entity.PrincipalAngle

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self._Entity.Elements)

	@property
	def PlateElements(self) -> ElementCol:
		return ElementCol(self._Entity.PlateElements)

	@property
	def BeamElements(self) -> ElementCol:
		return ElementCol(self._Entity.BeamElements)

	@ReferencePoint.setter
	def ReferencePoint(self, value: types.SectionCutPropertyLocation) -> None:
		self._Entity.ReferencePoint = _types.SectionCutPropertyLocation(value.value)

	@MaxAngleBound.setter
	def MaxAngleBound(self, value: float) -> None:
		self._Entity.MaxAngleBound = value

	@MinAngleBound.setter
	def MinAngleBound(self, value: float) -> None:
		self._Entity.MinAngleBound = value

	@MinStiffnessEihh.setter
	def MinStiffnessEihh(self, value: float) -> None:
		self._Entity.MinStiffnessEihh = value

	@MinStiffnessEivv.setter
	def MinStiffnessEivv(self, value: float) -> None:
		self._Entity.MinStiffnessEivv = value

	@MinStiffnessGJ.setter
	def MinStiffnessGJ(self, value: float) -> None:
		self._Entity.MinStiffnessGJ = value

	@ZoneStiffnessDistribution.setter
	def ZoneStiffnessDistribution(self, value: float) -> None:
		self._Entity.ZoneStiffnessDistribution = value

	@CN_hmax.setter
	def CN_hmax(self, value: float) -> None:
		self._Entity.CN_hmax = value

	@CN_hmin.setter
	def CN_hmin(self, value: float) -> None:
		self._Entity.CN_hmin = value

	@CN_vmax.setter
	def CN_vmax(self, value: float) -> None:
		self._Entity.CN_vmax = value

	@CN_vmin.setter
	def CN_vmin(self, value: float) -> None:
		self._Entity.CN_vmin = value

	@CQ_hmax.setter
	def CQ_hmax(self, value: float) -> None:
		self._Entity.CQ_hmax = value

	@CQ_hmin.setter
	def CQ_hmin(self, value: float) -> None:
		self._Entity.CQ_hmin = value

	@CQ_vmax.setter
	def CQ_vmax(self, value: float) -> None:
		self._Entity.CQ_vmax = value

	@CQ_vmin.setter
	def CQ_vmin(self, value: float) -> None:
		self._Entity.CQ_vmin = value

	def AlignToHorizontalPrincipalAxes(self) -> None:
		'''
		Set this Section Cut's horizontal vector to be equal to its principal axis horizontal vector.
		'''
		return self._Entity.AlignToHorizontalPrincipalAxes()

	def AlignToVerticalPrincipalAxes(self) -> None:
		'''
		Set this Section Cut's horizontal vector to be equal to its principal axis vertical vector.
		'''
		return self._Entity.AlignToVerticalPrincipalAxes()

	def SetHorizontalVector(self, vector: Vector3d) -> None:
		return self._Entity.SetHorizontalVector(vector._Entity)

	def SetNormalVector(self, vector: Vector3d) -> None:
		return self._Entity.SetNormalVector(vector._Entity)

	def SetOrigin(self, vector: Vector3d) -> None:
		return self._Entity.SetOrigin(vector._Entity)

	def GetBeamLoads(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> BeamLoads:
		return BeamLoads(self._Entity.GetBeamLoads(loadCaseId, _types.LoadSubCaseFactor(factor.value)))

	def InclinationAngle(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return self._Entity.InclinationAngle(loadCaseId, _types.LoadSubCaseFactor(factor.value))

	def HorizontalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return self._Entity.HorizontalIntercept(loadCaseId, _types.LoadSubCaseFactor(factor.value))

	def VerticalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return self._Entity.VerticalIntercept(loadCaseId, _types.LoadSubCaseFactor(factor.value))

	def SetElements(self, elements: list[int]) -> bool:
		elementsList = MakeCSharpIntList(elements)
		return self._Entity.SetElements(elementsList)


class Set(ZoneJointContainer):
	def __init__(self, set: _api.Set):
		self._Entity = set

	@property
	def Joints(self) -> JointCol:
		return JointCol(self._Entity.Joints)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self._Entity.PanelSegments)

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self._Entity.Zones)

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoints(self, joints: JointCol) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zones: ZoneCol) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segments: PanelSegmentCol) -> CollectionModificationStatus: ...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddJoint(item1))

		return self._Entity.AddJoint(item1._Entity)

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddPanelSegment(item1))

		return self._Entity.AddPanelSegment(item1._Entity)

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.AddZone(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddZone(item1))

		return self._Entity.AddZone(item1._Entity)

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, JointCol):
			return CollectionModificationStatus(super().RemoveJoints(item1))

		return self._Entity.RemoveJoints(jointIdsEnumerable)

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, PanelSegmentCol):
			return CollectionModificationStatus(super().RemovePanelSegments(item1))

		return self._Entity.RemovePanelSegments(segmentIdsEnumerable)

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, ZoneCol):
			return CollectionModificationStatus(super().RemoveZones(item1))

		return self._Entity.RemoveZones(zoneIdsEnumerable)

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		if isinstance(item1, Joint):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		return self._Entity.RemoveJoint(item1)

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().RemoveZone(item1))

		return self._Entity.RemoveZone(item1)

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		return self._Entity.RemovePanelSegment(item1)


class PlyCol(IdNameEntityCol[Ply]):
	def __init__(self, plyCol: _api.PlyCol):
		self._Entity = plyCol
		self._CollectedClass = Ply

	@property
	def PlyColList(self) -> tuple[Ply]:
		return tuple([Ply(plyCol) for plyCol in self._Entity])

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self._Entity.Delete(id).ToString()]

	def DeleteAll(self) -> None:
		'''
		Delete all plies in the collection.
		'''
		return self._Entity.DeleteAll()

	def ExportToCSV(self, filepath: str) -> None:
		return self._Entity.ExportToCSV(filepath)

	def ImportCSV(self, filepath: str) -> None:
		return self._Entity.ImportCSV(filepath)

	@overload
	def Get(self, name: str) -> Ply: ...

	@overload
	def Get(self, id: int) -> Ply: ...

	def Get(self, item1 = None) -> Ply:
		if isinstance(item1, str):
			return Ply(super().Get(item1))

		if isinstance(item1, int):
			return Ply(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.PlyColList[index]

	def __iter__(self):
		yield from self.PlyColList

	def __len__(self):
		return len(self.PlyColList)


class Structure(ZoneJointContainer):
	def __init__(self, structure: _api.Structure):
		self._Entity = structure

	@property
	def Plies(self) -> PlyCol:
		return PlyCol(self._Entity.Plies)

	@property
	def Joints(self) -> JointCol:
		return JointCol(self._Entity.Joints)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self._Entity.PanelSegments)

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self._Entity.Zones)

	def ExportVCP(self, fileName: str) -> None:
		return self._Entity.ExportVCP(fileName)

	def AddElements(self, elementIds: tuple[int]) -> CollectionModificationStatus:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return CollectionModificationStatus[self._Entity.AddElements(elementIdsEnumerable).ToString()]

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	def AddPfemProperties(self, pfemPropertyIds: tuple[int]) -> CollectionModificationStatus:
		pfemPropertyIdsList = MakeCSharpIntList(pfemPropertyIds)
		pfemPropertyIdsEnumerable = IEnumerable(pfemPropertyIdsList)
		return CollectionModificationStatus[self._Entity.AddPfemProperties(pfemPropertyIdsEnumerable).ToString()]

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus: ...

	def CreateZone(self, elementIds: tuple[int], name: str = None) -> None:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self._Entity.CreateZone(elementIdsEnumerable, name)

	def CreatePanelSegment(self, discreteTechnique: types.DiscreteTechnique, discreteElementLkp: dict[types.DiscreteDefinitionType, list[int]], name: str = None) -> int:
		discreteElementLkpDict = Dictionary[_types.DiscreteDefinitionType, List[int]]()
		for kvp in discreteElementLkp:
			discreteElementLkpDict.Add(_types.DiscreteDefinitionType(kvp.value), MakeCSharpIntList(discreteElementLkp[kvp]))
		return self._Entity.CreatePanelSegment(_types.DiscreteTechnique(discreteTechnique.value), discreteElementLkpDict, name)

	@overload
	def Remove(self, zoneIds: tuple[int], jointIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def Remove(self, zoneIds: tuple[int], jointIds: tuple[int], panelSegmentIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoints(self, joints: JointCol) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zones: ZoneCol) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segments: PanelSegmentCol) -> CollectionModificationStatus: ...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddJoint(item1))

		return self._Entity.AddJoint(item1._Entity)

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddPanelSegment(item1))

		return self._Entity.AddPanelSegment(item1._Entity)

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.AddZone(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddZone(item1))

		return self._Entity.AddZone(item1._Entity)

	def Remove(self, item1 = None, item2 = None, item3 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and isinstance(item2, tuple) and isinstance(item3, tuple):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = MakeCSharpIntList(item2)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			panelSegmentIdsList = MakeCSharpIntList(item3)
			panelSegmentIdsEnumerable = IEnumerable(panelSegmentIdsList)
			return CollectionModificationStatus[self._Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable, panelSegmentIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and isinstance(item2, tuple):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = MakeCSharpIntList(item2)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable).ToString()]

		return self._Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable, panelSegmentIdsEnumerable)

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, JointCol):
			return CollectionModificationStatus(super().RemoveJoints(item1))

		return self._Entity.RemoveJoints(jointIdsEnumerable)

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, PanelSegmentCol):
			return CollectionModificationStatus(super().RemovePanelSegments(item1))

		return self._Entity.RemovePanelSegments(segmentIdsEnumerable)

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, ZoneCol):
			return CollectionModificationStatus(super().RemoveZones(item1))

		return self._Entity.RemoveZones(zoneIdsEnumerable)

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		if isinstance(item1, Joint):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		return self._Entity.RemoveJoint(item1)

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().RemoveZone(item1))

		return self._Entity.RemoveZone(item1)

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		return self._Entity.RemovePanelSegment(item1)


class AnalysisPropertyCol(IdNameEntityCol[AnalysisProperty]):
	def __init__(self, analysisPropertyCol: _api.AnalysisPropertyCol):
		self._Entity = analysisPropertyCol
		self._CollectedClass = AnalysisProperty

	@property
	def AnalysisPropertyColList(self) -> tuple[AnalysisProperty]:
		return tuple([AnalysisProperty(analysisPropertyCol) for analysisPropertyCol in self._Entity])

	@overload
	def Get(self, name: str) -> AnalysisProperty: ...

	@overload
	def Get(self, id: int) -> AnalysisProperty: ...

	def Get(self, item1 = None) -> AnalysisProperty:
		if isinstance(item1, str):
			return AnalysisProperty(super().Get(item1))

		if isinstance(item1, int):
			return AnalysisProperty(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.AnalysisPropertyColList[index]

	def __iter__(self):
		yield from self.AnalysisPropertyColList

	def __len__(self):
		return len(self.AnalysisPropertyColList)


class DesignPropertyCol(IdNameEntityCol[DesignProperty]):
	def __init__(self, designPropertyCol: _api.DesignPropertyCol):
		self._Entity = designPropertyCol
		self._CollectedClass = DesignProperty

	@property
	def DesignPropertyColList(self) -> tuple[DesignProperty]:
		return tuple([DesignProperty(designPropertyCol) for designPropertyCol in self._Entity])

	@overload
	def Get(self, name: str) -> DesignProperty: ...

	@overload
	def Get(self, id: int) -> DesignProperty: ...

	def Get(self, item1 = None) -> DesignProperty:
		if isinstance(item1, str):
			return DesignProperty(super().Get(item1))

		if isinstance(item1, int):
			return DesignProperty(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.DesignPropertyColList[index]

	def __iter__(self):
		yield from self.DesignPropertyColList

	def __len__(self):
		return len(self.DesignPropertyColList)


class LoadPropertyCol(IdNameEntityCol[LoadProperty]):
	def __init__(self, loadPropertyCol: _api.LoadPropertyCol):
		self._Entity = loadPropertyCol
		self._CollectedClass = LoadProperty

	@property
	def LoadPropertyColList(self) -> tuple[LoadProperty]:
		return tuple([LoadProperty(loadPropertyCol) for loadPropertyCol in self._Entity])

	@overload
	def Get(self, name: str) -> LoadProperty: ...

	@overload
	def Get(self, id: int) -> LoadProperty: ...

	def Get(self, item1 = None) -> LoadProperty:
		if isinstance(item1, str):
			return LoadProperty(super().Get(item1))

		if isinstance(item1, int):
			return LoadProperty(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.LoadPropertyColList[index]

	def __iter__(self):
		yield from self.LoadPropertyColList

	def __len__(self):
		return len(self.LoadPropertyColList)


class DesignLoadCol(IdNameEntityCol[DesignLoad]):
	def __init__(self, designLoadCol: _api.DesignLoadCol):
		self._Entity = designLoadCol
		self._CollectedClass = DesignLoad

	@property
	def DesignLoadColList(self) -> tuple[DesignLoad]:
		return tuple([DesignLoad(designLoadCol) for designLoadCol in self._Entity])

	@overload
	def Get(self, name: str) -> DesignLoad: ...

	@overload
	def Get(self, id: int) -> DesignLoad: ...

	def Get(self, item1 = None) -> DesignLoad:
		if isinstance(item1, str):
			return DesignLoad(super().Get(item1))

		if isinstance(item1, int):
			return DesignLoad(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.DesignLoadColList[index]

	def __iter__(self):
		yield from self.DesignLoadColList

	def __len__(self):
		return len(self.DesignLoadColList)


class DiscreteFieldCol(IdNameEntityCol[DiscreteField]):
	def __init__(self, discreteFieldCol: _api.DiscreteFieldCol):
		self._Entity = discreteFieldCol
		self._CollectedClass = DiscreteField

	@property
	def DiscreteFieldColList(self) -> tuple[DiscreteField]:
		return tuple([DiscreteField(discreteFieldCol) for discreteFieldCol in self._Entity])

	def Create(self, name: str, entityType: types.DiscreteFieldPhysicalEntityType, dataType: types.DiscreteFieldDataType) -> int:
		return self._Entity.Create(name, _types.DiscreteFieldPhysicalEntityType(entityType.value), _types.DiscreteFieldDataType(dataType.value))

	def CreateFromVCP(self, filepath: str) -> list[int]:
		return list[int](self._Entity.CreateFromVCP(filepath))

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self._Entity.Delete(id).ToString()]

	def CreateByPointMapToElements(self, elementIds: list[int], discreteFieldIds: list[int], suffix: str = None, tolerance: float = None) -> None:
		elementIdsList = MakeCSharpIntList(elementIds)
		discreteFieldIdsList = MakeCSharpIntList(discreteFieldIds)
		return self._Entity.CreateByPointMapToElements(elementIdsList, discreteFieldIdsList, suffix, tolerance)

	@overload
	def Get(self, name: str) -> DiscreteField: ...

	@overload
	def Get(self, id: int) -> DiscreteField: ...

	def Get(self, item1 = None) -> DiscreteField:
		if isinstance(item1, str):
			return DiscreteField(super().Get(item1))

		if isinstance(item1, int):
			return DiscreteField(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.DiscreteFieldColList[index]

	def __iter__(self):
		yield from self.DiscreteFieldColList

	def __len__(self):
		return len(self.DiscreteFieldColList)


class ZoneJointContainerCol(IdNameEntityCol, Generic[T]):
	def __init__(self, zoneJointContainerCol: _api.ZoneJointContainerCol):
		self._Entity = zoneJointContainerCol
		self._CollectedClass = T

	@property
	def ZoneJointContainerColList(self) -> tuple[T]:
		return tuple([T(zoneJointContainerCol) for zoneJointContainerCol in self._Entity])

	@abstractmethod
	def Create(self, name: str) -> bool:
		return self._Entity.Create(name)

	@overload
	def Get(self, name: str) -> T: ...

	@overload
	def Get(self, id: int) -> T: ...

	def Get(self, item1 = None) -> T:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.ZoneJointContainerColList[index]

	def __iter__(self):
		yield from self.ZoneJointContainerColList

	def __len__(self):
		return len(self.ZoneJointContainerColList)


class RundeckCol(IdEntityCol[Rundeck]):
	def __init__(self, rundeckCol: _api.RundeckCol):
		self._Entity = rundeckCol
		self._CollectedClass = Rundeck

	@property
	def RundeckColList(self) -> tuple[Rundeck]:
		return tuple([Rundeck(rundeckCol) for rundeckCol in self._Entity])

	def AddRundeck(self, inputPath: str, resultPath: str = None) -> RundeckCreationStatus:
		return RundeckCreationStatus[self._Entity.AddRundeck(inputPath, resultPath).ToString()]

	def ReassignPrimary(self, id: int) -> RundeckUpdateStatus:
		return RundeckUpdateStatus[self._Entity.ReassignPrimary(id).ToString()]

	def RemoveRundeck(self, id: int) -> RundeckRemoveStatus:
		return RundeckRemoveStatus[self._Entity.RemoveRundeck(id).ToString()]

	def __getitem__(self, index: int):
		return self.RundeckColList[index]

	def __iter__(self):
		yield from self.RundeckColList

	def __len__(self):
		return len(self.RundeckColList)


class SectionCutCol(IdNameEntityCol[SectionCut]):
	def __init__(self, sectionCutCol: _api.SectionCutCol):
		self._Entity = sectionCutCol
		self._CollectedClass = SectionCut

	@property
	def SectionCutColList(self) -> tuple[SectionCut]:
		return tuple([SectionCut(sectionCutCol) for sectionCutCol in self._Entity])

	def Create(self, name: str, origin: Vector3d, normal: Vector3d, horizontal: Vector3d) -> None:
		return self._Entity.Create(name, origin._Entity, normal._Entity, horizontal._Entity)

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self._Entity.Delete(id).ToString()]

	@overload
	def Get(self, name: str) -> SectionCut: ...

	@overload
	def Get(self, id: int) -> SectionCut: ...

	def Get(self, item1 = None) -> SectionCut:
		if isinstance(item1, str):
			return SectionCut(super().Get(item1))

		if isinstance(item1, int):
			return SectionCut(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.SectionCutColList[index]

	def __iter__(self):
		yield from self.SectionCutColList

	def __len__(self):
		return len(self.SectionCutColList)


class SetCol(ZoneJointContainerCol[Set]):
	def __init__(self, setCol: _api.SetCol):
		self._Entity = setCol
		self._CollectedClass = Set

	@property
	def SetColList(self) -> tuple[Set]:
		return tuple([Set(setCol) for setCol in self._Entity])

	def Create(self, name: str) -> bool:
		return self._Entity.Create(name)

	@overload
	def Get(self, name: str) -> Set: ...

	@overload
	def Get(self, id: int) -> Set: ...

	def Get(self, item1 = None) -> Set:
		if isinstance(item1, str):
			return Set(super().Get(item1))

		if isinstance(item1, int):
			return Set(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.SetColList[index]

	def __iter__(self):
		yield from self.SetColList

	def __len__(self):
		return len(self.SetColList)


class StructureCol(ZoneJointContainerCol[Structure]):
	def __init__(self, structureCol: _api.StructureCol):
		self._Entity = structureCol
		self._CollectedClass = Structure

	@property
	def StructureColList(self) -> tuple[Structure]:
		return tuple([Structure(structureCol) for structureCol in self._Entity])

	def Create(self, name: str) -> bool:
		return self._Entity.Create(name)

	@overload
	def DeleteStructure(self, structure: Structure) -> CollectionModificationStatus: ...

	@overload
	def DeleteStructure(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def Get(self, name: str) -> Structure: ...

	@overload
	def Get(self, id: int) -> Structure: ...

	def DeleteStructure(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Structure):
			return CollectionModificationStatus[self._Entity.DeleteStructure(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.DeleteStructure(item1).ToString()]

		return self._Entity.DeleteStructure(item1._Entity)

	def Get(self, item1 = None) -> Structure:
		if isinstance(item1, str):
			return Structure(super().Get(item1))

		if isinstance(item1, int):
			return Structure(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.StructureColList[index]

	def __iter__(self):
		yield from self.StructureColList

	def __len__(self):
		return len(self.StructureColList)


class Project:
	'''
	Represents a HyperX project within a database.
	'''
	def __init__(self, project: _api.Project):
		self._Entity = project

	@property
	def WorkingFolder(self) -> str:
		return self._Entity.WorkingFolder

	@property
	def FemDataSet(self) -> FemDataSet:
		return FemDataSet(self._Entity.FemDataSet)

	@property
	def Beams(self) -> ZoneCol:
		return ZoneCol(self._Entity.Beams)

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def Joints(self) -> JointCol:
		return JointCol(self._Entity.Joints)

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Panels(self) -> ZoneCol:
		return ZoneCol(self._Entity.Panels)

	@property
	def Rundecks(self) -> RundeckCol:
		return RundeckCol(self._Entity.Rundecks)

	@property
	def Sets(self) -> SetCol:
		return SetCol(self._Entity.Sets)

	@property
	def Structures(self) -> StructureCol:
		return StructureCol(self._Entity.Structures)

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self._Entity.Zones)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self._Entity.PanelSegments)

	@property
	def SectionCuts(self) -> SectionCutCol:
		return SectionCutCol(self._Entity.SectionCuts)

	@property
	def DesignLoads(self) -> DesignLoadCol:
		return DesignLoadCol(self._Entity.DesignLoads)

	@property
	def DiscreteFieldTables(self) -> DiscreteFieldCol:
		return DiscreteFieldCol(self._Entity.DiscreteFieldTables)

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		return AnalysisPropertyCol(self._Entity.AnalysisProperties)

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		return DesignPropertyCol(self._Entity.DesignProperties)

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		return LoadPropertyCol(self._Entity.LoadProperties)

	@property
	def FemFormat(self) -> types.ProjectModelFormat:
		return types.ProjectModelFormat[self._Entity.FemFormat.ToString()]

	def Upload(self, uploadSetName: str, company: str, program: str, tags: list[str], notes: str, zoneIds: set[int], jointIds: set[int]) -> bool:
		tagsList = List[str]()
		if tags is not None:
			for thing in tags:
				if thing is not None:
					tagsList.Add(thing)
		return self._Entity.Upload(uploadSetName, company, program, tagsList, notes, zoneIds._Entity, jointIds._Entity)

	def GetDashboardCompanies(self) -> list[str]:
		'''
		This method fetches an array of Dashboard company names that are available to the user who is currently logged in. The URL and authentication token are taken from the last
            Dashboard login made through HyperX.
		'''
		return list[str](self._Entity.GetDashboardCompanies())

	def GetDashboardPrograms(self, companyName: str) -> list[str]:
		return list[str](self._Entity.GetDashboardPrograms(companyName))

	def GetDashboardTags(self, companyName: str) -> list[str]:
		return list[str](self._Entity.GetDashboardTags(companyName))

	def Dispose(self) -> None:
		return self._Entity.Dispose()

	def GetConceptName(self, zoneId: int) -> str:
		return self._Entity.GetConceptName(zoneId)

	def GetJointAnalysisResults(self, joints: list[Joint] = None, analysisResultType: AnalysisResultToReturn = AnalysisResultToReturn.Minimum) -> dict[int, dict[types.JointObject, dict[types.AnalysisId, tuple[float, types.MarginCode]]]]:
		jointsList = List[_api.Joint]()
		if joints is not None:
			for thing in joints:
				if thing is not None:
					jointsList.Add(thing._Entity)
		return dict[int, dict[types.JointObject, dict[types.AnalysisId, tuple[float, types.MarginCode]]]](self._Entity.GetJointAnalysisResults(joints if joints is None else jointsList, _api.AnalysisResultToReturn(analysisResultType.value)))

	def GetObjectName(self, zoneId: int, objectId: int) -> str:
		return self._Entity.GetObjectName(zoneId, objectId)

	def GetZoneConceptAnalysisResults(self, zones: list[Zone] = None, analysisResultType: AnalysisResultToReturn = AnalysisResultToReturn.Minimum) -> dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]]:
		zonesList = List[_api.Zone]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesList.Add(thing._Entity)
		return dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]](self._Entity.GetZoneConceptAnalysisResults(zones if zones is None else zonesList, _api.AnalysisResultToReturn(analysisResultType.value)))

	def GetZoneObjectAnalysisResults(self, zones: list[Zone] = None, analysisResultType: AnalysisResultToReturn = AnalysisResultToReturn.Minimum) -> dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]]:
		zonesList = List[_api.Zone]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesList.Add(thing._Entity)
		return dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]](self._Entity.GetZoneObjectAnalysisResults(zones if zones is None else zonesList, _api.AnalysisResultToReturn(analysisResultType.value)))

	def ImportFem(self) -> None:
		return self._Entity.ImportFem()

	def SetFemFormat(self, femFormat: types.ProjectModelFormat) -> None:
		return self._Entity.SetFemFormat(_types.ProjectModelFormat(femFormat.value))

	def SetFemUnits(self, femForceId: DbForceUnit, femLengthId: DbLengthUnit, femMassId: DbMassUnit, femTemperatureId: DbTemperatureUnit) -> SetUnitsStatus:
		return SetUnitsStatus[self._Entity.SetFemUnits(_api.DbForceUnit(femForceId.value), _api.DbLengthUnit(femLengthId.value), _api.DbMassUnit(femMassId.value), _api.DbTemperatureUnit(femTemperatureId.value)).ToString()]

	def SizeJoints(self, joints: list[Joint] = None) -> tuple[bool, str, set[int]]:
		jointsList = List[_api.Joint]()
		if joints is not None:
			for thing in joints:
				if thing is not None:
					jointsList.Add(thing._Entity)
		result = self._Entity.SizeJoints(joints if joints is None else jointsList)
		return tuple([result.Item1, result.Item2, result.Item3])

	@overload
	def AnalyzeZones(self, zones: list[Zone] = None) -> tuple[bool, str]: ...

	@overload
	def AnalyzeZones(self, zoneIds: list[int]) -> tuple[bool, str]: ...

	@overload
	def SizeZones(self, zones: list[Zone] = None) -> tuple[bool, str]: ...

	@overload
	def SizeZones(self, zoneIds: list[int]) -> tuple[bool, str]: ...

	def UnimportFemAsync(self) -> Task:
		return Task(self._Entity.UnimportFemAsync())

	def ExportFem(self, destinationFolder: str) -> None:
		return self._Entity.ExportFem(destinationFolder)

	def ImportCad(self, filePath: str) -> None:
		return self._Entity.ImportCad(filePath)

	@overload
	def ExportCad(self, filePath: str) -> None: ...

	@overload
	def ExportCad(self, cadIds: tuple[int], filePath: str) -> None: ...

	def AnalyzeZones(self, item1 = None) -> tuple[bool, str]:
		if isinstance(item1, list):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			result = self._Entity.AnalyzeZones(item1 if item1 is None else zonesList)
			return tuple([result.Item1, result.Item2])

		if isinstance(item1, list):
			zoneIdsList = MakeCSharpIntList(item1)
			result = self._Entity.AnalyzeZones(zoneIdsList)
			return tuple([result.Item1, result.Item2])

		return self._Entity.AnalyzeZones(item1 if item1 is None else zonesList)

	def SizeZones(self, item1 = None) -> tuple[bool, str]:
		if isinstance(item1, list):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			result = self._Entity.SizeZones(item1 if item1 is None else zonesList)
			return tuple([result.Item1, result.Item2])

		if isinstance(item1, list):
			zoneIdsList = MakeCSharpIntList(item1)
			result = self._Entity.SizeZones(zoneIdsList)
			return tuple([result.Item1, result.Item2])

		return self._Entity.SizeZones(item1 if item1 is None else zonesList)

	def ExportCad(self, item1 = None, item2 = None) -> None:
		if isinstance(item1, tuple) and isinstance(item2, str):
			cadIdsList = MakeCSharpIntList(item1)
			cadIdsEnumerable = IEnumerable(cadIdsList)
			return self._Entity.ExportCad(cadIdsEnumerable, item2)

		if isinstance(item1, str):
			return self._Entity.ExportCad(item1)

		return self._Entity.ExportCad(cadIdsEnumerable, item2)


class ProjectInfo(IdNameEntityRenameable):
	def __init__(self, projectInfo: _api.ProjectInfo):
		self._Entity = projectInfo


class FailureModeCategoryCol(IdNameEntityCol[FailureModeCategory]):
	def __init__(self, failureModeCategoryCol: _api.FailureModeCategoryCol):
		self._Entity = failureModeCategoryCol
		self._CollectedClass = FailureModeCategory

	@property
	def FailureModeCategoryColList(self) -> tuple[FailureModeCategory]:
		return tuple([FailureModeCategory(failureModeCategoryCol) for failureModeCategoryCol in self._Entity])

	@overload
	def Get(self, name: str) -> FailureModeCategory: ...

	@overload
	def Get(self, id: int) -> FailureModeCategory: ...

	def Get(self, item1 = None) -> FailureModeCategory:
		if isinstance(item1, str):
			return FailureModeCategory(super().Get(item1))

		if isinstance(item1, int):
			return FailureModeCategory(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.FailureModeCategoryColList[index]

	def __iter__(self):
		yield from self.FailureModeCategoryColList

	def __len__(self):
		return len(self.FailureModeCategoryColList)


class FoamCol(Generic[T]):
	def __init__(self, foamCol: _api.FoamCol):
		self._Entity = foamCol

	@property
	def FoamColList(self) -> tuple[Foam]:
		return tuple([Foam(foamCol) for foamCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Foam:
		return Foam(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self._Entity.Contains(materialName)

	def Create(self, newMaterialName: str, materialFamilyName: str, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Create(newMaterialName, materialFamilyName, density, femId).ToString()]

	def Copy(self, fmToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Copy(fmToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.FoamColList[index]

	def __iter__(self):
		yield from self.FoamColList

	def __len__(self):
		return len(self.FoamColList)


class HoneycombCol(Generic[T]):
	def __init__(self, honeycombCol: _api.HoneycombCol):
		self._Entity = honeycombCol

	@property
	def HoneycombColList(self) -> tuple[Honeycomb]:
		return tuple([Honeycomb(honeycombCol) for honeycombCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Honeycomb:
		return Honeycomb(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self._Entity.Contains(materialName)

	def Create(self, newMaterialName: str, materialFamilyName: str, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Create(newMaterialName, materialFamilyName, density, femId).ToString()]

	def Copy(self, honeyToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Copy(honeyToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.HoneycombColList[index]

	def __iter__(self):
		yield from self.HoneycombColList

	def __len__(self):
		return len(self.HoneycombColList)


class IsotropicCol(Generic[T]):
	def __init__(self, isotropicCol: _api.IsotropicCol):
		self._Entity = isotropicCol

	@property
	def IsotropicColList(self) -> tuple[Isotropic]:
		return tuple([Isotropic(isotropicCol) for isotropicCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Isotropic:
		return Isotropic(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self._Entity.Contains(materialName)

	def Create(self, newMaterialName: str, materialFamilyName: str, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Create(newMaterialName, materialFamilyName, density, femId).ToString()]

	def Copy(self, isoToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Copy(isoToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.IsotropicColList[index]

	def __iter__(self):
		yield from self.IsotropicColList

	def __len__(self):
		return len(self.IsotropicColList)


class OrthotropicCol(Generic[T]):
	def __init__(self, orthotropicCol: _api.OrthotropicCol):
		self._Entity = orthotropicCol

	@property
	def OrthotropicColList(self) -> tuple[Orthotropic]:
		return tuple([Orthotropic(orthotropicCol) for orthotropicCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Orthotropic:
		return Orthotropic(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self._Entity.Contains(materialName)

	def Create(self, newMaterialName: str, materialFamilyName: str, thickness: float, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Create(newMaterialName, materialFamilyName, thickness, density, femId).ToString()]

	def Copy(self, orthoToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self._Entity.Copy(orthoToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.OrthotropicColList[index]

	def __iter__(self):
		yield from self.OrthotropicColList

	def __len__(self):
		return len(self.OrthotropicColList)


class ProjectInfoCol(IdNameEntityCol[ProjectInfo]):
	def __init__(self, projectInfoCol: _api.ProjectInfoCol):
		self._Entity = projectInfoCol
		self._CollectedClass = ProjectInfo

	@property
	def ProjectInfoColList(self) -> tuple[ProjectInfo]:
		return tuple([ProjectInfo(projectInfoCol) for projectInfoCol in self._Entity])

	@overload
	def Get(self, name: str) -> ProjectInfo: ...

	@overload
	def Get(self, id: int) -> ProjectInfo: ...

	def Get(self, item1 = None) -> ProjectInfo:
		if isinstance(item1, str):
			return ProjectInfo(super().Get(item1))

		if isinstance(item1, int):
			return ProjectInfo(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.ProjectInfoColList[index]

	def __iter__(self):
		yield from self.ProjectInfoColList

	def __len__(self):
		return len(self.ProjectInfoColList)


class Application:
	'''
	HyperX scripting application.
            This API is not guaranteed to be thread-safe.
            Calls into a single application instance or its descendents are not safe to be called concurrently.
            
            However, it is safe enough for integration testing to have multiple
            application instances with a single process.
	'''
	def __init__(self, application: _api.Application):
		self._Entity = application

	@property
	def CompilationDate(self) -> str:
		return self._Entity.CompilationDate

	@property
	def DatabasePath(self) -> str:
		return self._Entity.DatabasePath

	@property
	def ActiveProject(self) -> Project:
		'''
		Represents a HyperX project within a database.
		'''
		return Project(self._Entity.ActiveProject)

	@property
	def UiRunnerMode(self) -> bool:
		return self._Entity.UiRunnerMode

	@property
	def Version(self) -> str:
		return self._Entity.Version

	@property
	def FailureModeCategories(self) -> FailureModeCategoryCol:
		return FailureModeCategoryCol(self._Entity.FailureModeCategories)

	@property
	def FailureModes(self) -> FailureModeCol:
		return FailureModeCol(self._Entity.FailureModes)

	@property
	def Foams(self) -> FoamCol:
		'''
		Contains a set of all foam materials in a database.
		'''
		return FoamCol(self._Entity.Foams)

	@property
	def Honeycombs(self) -> HoneycombCol:
		'''
		Contains a set of all honeycomb materials in a database.
		'''
		return HoneycombCol(self._Entity.Honeycombs)

	@property
	def Isotropics(self) -> IsotropicCol:
		'''
		Contains a set of all isotropic materials in a database.
		'''
		return IsotropicCol(self._Entity.Isotropics)

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		return AnalysisPropertyCol(self._Entity.AnalysisProperties)

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		return DesignPropertyCol(self._Entity.DesignProperties)

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		return LoadPropertyCol(self._Entity.LoadProperties)

	@property
	def Orthotropics(self) -> OrthotropicCol:
		'''
		Contains a set of all orthotropic materials in a database.
		'''
		return OrthotropicCol(self._Entity.Orthotropics)

	@property
	def ProjectInfos(self) -> ProjectInfoCol:
		'''
		Contains a set of all projects in a database.
		'''
		return ProjectInfoCol(self._Entity.ProjectInfos)

	@property
	def UserName(self) -> str:
		return self._Entity.UserName

	@UserName.setter
	def UserName(self, value: str) -> None:
		self._Entity.UserName = value

	def CloseDatabase(self, delay: int = 0) -> None:
		return self._Entity.CloseDatabase(delay)

	def CopyProject(self, projectId: int, newName: str, copyDesignProperties: bool = True, copyAnalysisProperties: bool = True, copyLoadProperties: bool = True, copyWorkingFolder: bool = True) -> int:
		return self._Entity.CopyProject(projectId, newName, copyDesignProperties, copyAnalysisProperties, copyLoadProperties, copyWorkingFolder)

	def CreateAnalysisProperty(self, name: str, type: types.FamilyCategory) -> int:
		return self._Entity.CreateAnalysisProperty(name, _types.FamilyCategory(type.value))

	def CreateFailureMode(self, failureModeCategoryId: int) -> int:
		return self._Entity.CreateFailureMode(failureModeCategoryId)

	def CreateDatabaseFromTemplate(self, templateName: str, newPath: str) -> CreateDatabaseStatus:
		return CreateDatabaseStatus[self._Entity.CreateDatabaseFromTemplate(templateName, newPath).ToString()]

	def CreateProject(self, projectName: str) -> ProjectCreationStatus:
		return ProjectCreationStatus[self._Entity.CreateProject(projectName).ToString()]

	def DeleteAnalysisProperty(self, id: int) -> None:
		return self._Entity.DeleteAnalysisProperty(id)

	def DeleteProject(self, projectName: str) -> ProjectDeletionStatus:
		return ProjectDeletionStatus[self._Entity.DeleteProject(projectName).ToString()]

	def Dispose(self) -> None:
		'''
		Dispose of the application. Should be explicitly called after the application
            is no longer needed unless the application is wrapped with a using clause.
		'''
		return self._Entity.Dispose()

	def GetAnalyses(self) -> dict[int, AnalysisDefinition]:
		'''
		Get all Analysis Defintions in the database.
		'''
		return dict[int, AnalysisDefinition](self._Entity.GetAnalyses())

	def Login(self, userName: str, password: str = "") -> None:
		return self._Entity.Login(userName, password)

	def Migrate(self, databasePath: str) -> str:
		return self._Entity.Migrate(databasePath)

	def OpenDatabase(self, databasePath: str) -> None:
		return self._Entity.OpenDatabase(databasePath)

	def SelectProject(self, projectName: str) -> Project:
		return Project(self._Entity.SelectProject(projectName))


class JointDesignProperty(DesignProperty):
	def __init__(self, jointDesignProperty: _api.JointDesignProperty):
		self._Entity = jointDesignProperty


class ToolingConstraint(IdNameEntity):
	'''
	Tooling constraints are a feature of Design Properties for Zones.
	'''
	def __init__(self, toolingConstraint: _api.ToolingConstraint):
		self._Entity = toolingConstraint

	@property
	def ConstraintMax(self) -> float:
		return self._Entity.ConstraintMax

	@property
	def ConstraintMin(self) -> float:
		return self._Entity.ConstraintMin

	@property
	def ConstraintValue(self) -> float:
		return self._Entity.ConstraintValue

	@property
	def ToolingSelectionType(self) -> types.ToolingSelectionType:
		'''
		Defines which selection a given tooling constraint is currently set to.
		'''
		return types.ToolingSelectionType[self._Entity.ToolingSelectionType.ToString()]

	def SetToAnyValue(self) -> None:
		return self._Entity.SetToAnyValue()

	def SetToInequality(self, value: float) -> None:
		return self._Entity.SetToInequality(value)

	def SetToRange(self, min: float, max: float) -> None:
		return self._Entity.SetToRange(min, max)

	def SetToValue(self, value: float) -> None:
		return self._Entity.SetToValue(value)


class DesignVariable(IdEntity):
	'''
	Holds design variable data.
            Min, max, steps, materials.
	'''
	def __init__(self, designVariable: _api.DesignVariable):
		self._Entity = designVariable

	@property
	def AllowMaterials(self) -> bool:
		return self._Entity.AllowMaterials

	@property
	def Max(self) -> float:
		return self._Entity.Max

	@property
	def Min(self) -> float:
		return self._Entity.Min

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def StepSize(self) -> float:
		return self._Entity.StepSize

	@property
	def UseAnalysis(self) -> bool:
		return self._Entity.UseAnalysis

	@Max.setter
	def Max(self, value: float) -> None:
		self._Entity.Max = value

	@Min.setter
	def Min(self, value: float) -> None:
		self._Entity.Min = value

	@StepSize.setter
	def StepSize(self, value: float) -> None:
		self._Entity.StepSize = value

	@UseAnalysis.setter
	def UseAnalysis(self, value: bool) -> None:
		self._Entity.UseAnalysis = value

	def AddMaterials(self, materialIds: list[int]) -> None:
		materialIdsList = MakeCSharpIntList(materialIds)
		return self._Entity.AddMaterials(materialIdsList)

	def GetSizingMaterials(self) -> list[int]:
		'''
		Get a list of materials used for sizing, if they exist.
		'''
		return list[int](self._Entity.GetSizingMaterials())

	def GetAnalysisMaterial(self) -> int:
		'''
		Get the material used for analysis, if it exists.
		'''
		return self._Entity.GetAnalysisMaterial()

	def RemoveSizingMaterials(self, materialIds: tuple[int] = None) -> None:
		materialIdsList = MakeCSharpIntList(materialIds)
		materialIdsEnumerable = IEnumerable(materialIdsList)
		return self._Entity.RemoveSizingMaterials(materialIds if materialIds is None else materialIdsEnumerable)

	def RemoveAnalysisMaterial(self) -> None:
		'''
		Remove the analysis material assigned to this variable.
		'''
		return self._Entity.RemoveAnalysisMaterial()


class ToolingConstraintCol(IdNameEntityCol[ToolingConstraint]):
	def __init__(self, toolingConstraintCol: _api.ToolingConstraintCol):
		self._Entity = toolingConstraintCol
		self._CollectedClass = ToolingConstraint

	@property
	def ToolingConstraintColList(self) -> tuple[ToolingConstraint]:
		return tuple([ToolingConstraint(toolingConstraintCol) for toolingConstraintCol in self._Entity])

	@overload
	def Get(self, name: str) -> ToolingConstraint: ...

	@overload
	def Get(self, id: int) -> ToolingConstraint: ...

	def Get(self, item1 = None) -> ToolingConstraint:
		if isinstance(item1, str):
			return ToolingConstraint(super().Get(item1))

		if isinstance(item1, int):
			return ToolingConstraint(super().Get(item1))

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.ToolingConstraintColList[index]

	def __iter__(self):
		yield from self.ToolingConstraintColList

	def __len__(self):
		return len(self.ToolingConstraintColList)


class DesignVariableCol(IdEntityCol[DesignVariable]):
	def __init__(self, designVariableCol: _api.DesignVariableCol):
		self._Entity = designVariableCol
		self._CollectedClass = DesignVariable

	@property
	def DesignVariableColList(self) -> tuple[DesignVariable]:
		return tuple([DesignVariable(designVariableCol) for designVariableCol in self._Entity])

	def __getitem__(self, index: int):
		return self.DesignVariableColList[index]

	def __iter__(self):
		yield from self.DesignVariableColList

	def __len__(self):
		return len(self.DesignVariableColList)


class ZoneDesignProperty(DesignProperty):
	def __init__(self, zoneDesignProperty: _api.ZoneDesignProperty):
		self._Entity = zoneDesignProperty

	@property
	def ToolingConstraints(self) -> ToolingConstraintCol:
		return ToolingConstraintCol(self._Entity.ToolingConstraints)

	@property
	def DesignVariables(self) -> DesignVariableCol:
		return DesignVariableCol(self._Entity.DesignVariables)


class Environment(ABC):
	'''
	Represents HyperX's execution environment (where HyperX is installed).
	'''
	def __init__(self, environment: _api.Environment):
		self._Entity = environment

	def SetLocation(self, location: str) -> None:
		return self._Entity.SetLocation(location)

	def Initialize(self) -> None:
		'''
		Initialize the HyperX scripting environment.
		'''
		return self._Entity.Initialize()


class FailureCriterionSetting(FailureSetting):
	'''
	Setting for a Failure Criteria.
	'''
	def __init__(self, failureCriterionSetting: _api.FailureCriterionSetting):
		self._Entity = failureCriterionSetting


class FailureModeSetting(FailureSetting):
	'''
	Setting for a Failure Mode.
	'''
	def __init__(self, failureModeSetting: _api.FailureModeSetting):
		self._Entity = failureModeSetting


class HelperFunctions(ABC):
	def __init__(self, helperFunctions: _api.HelperFunctions):
		self._Entity = helperFunctions

	def NullableSingle(self, input: float) -> float:
		return self._Entity.NullableSingle(input)


class Beam(Zone):
	def __init__(self, beam: _api.Beam):
		self._Entity = beam

	@property
	def Length(self) -> float:
		return self._Entity.Length


class Panel(Zone):
	def __init__(self, panel: _api.Panel):
		self._Entity = panel

	@property
	def Area(self) -> float:
		return self._Entity.Area
