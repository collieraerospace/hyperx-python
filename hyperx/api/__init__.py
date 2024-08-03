from __future__ import annotations
from ..library import _api, _types

from ..api import types
from typing import TypeVar, Generic, overload
from enum import Enum
from System.Collections.Generic import List, IEnumerable, Dictionary, HashSet
from System.Threading.Tasks import Task
from System import Guid, DateTime, Action, Double, String, Nullable

from abc import ABC, abstractmethod

T = TypeVar('T')

def MakeCSharpIntList(ints: list[int]) -> List[int]:
	intsList = List[int]()
	if ints is not None:
		for thing in ints:
			if thing is not None:
				intsList.Add(thing)
	
	return intsList

'''
Taken from: https://stackoverflow.com/a/3862957
'''
def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])

class AnalysisResultToReturn(Enum):
	'''
	Used to specify which analysis result to return.
	'''
	Limit = 1
	Ultimate = 2
	Minimum = 3

class CollectionModificationStatus(Enum):
	'''
	Indicates whether a collection was manipulated successfully.
	'''
	Success = 1
	DuplicateIdFailure = 2
	EntityMissingAddFailure = 3
	EntityMissingRemovalFailure = 4
	FemConnectionFailure = 5
	RunSetUsageFailure = 6
	EntityRemovalDependencyFailure = 7

class CreateDatabaseStatus(Enum):
	Success = 1
	TemplateNotFound = 2
	ImproperExtension = 3

class MaterialCreationStatus(Enum):
	'''
	Indicates whether a material was created successfully. 
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
	Indicates whether a project was created successfully. 
            If not, this indicates why the project was not created.
	'''
	Success = 1
	Failure = 2
	DuplicateNameFailure = 3

class ProjectDeletionStatus(Enum):
	'''
	Indicates whether a project was deleted successfully. 
            If not, this indicates why the project was not deleted.
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
	IncompatiblePropertyAssignment = 7
	EntityDoesNotExist = 8

class RundeckBulkUpdateStatus(Enum):
	NoRundecksUpdated = 0
	Success = 1
	InputFilePathDoesNotExist = 2
	ResultFilePathDoesNotExist = 3
	InputFilePathAlreadyExists = 4
	ResultFilePathAlreadyExists = 5
	InvalidPathCount = 6
	RundeckBulkUpdateFailure = 7
	SuccessButIncompatibleFem = 8

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
	RundeckRemoveFailure = 6
	SuccessButIncompatibleFem = 7

class RundeckUpdateStatus(Enum):
	Success = 1
	InvalidId = 2
	IdDoesNotExist = 3
	RundeckAlreadyPrimary = 4
	InputPathInUse = 5
	ResultPathInUse = 6
	RundeckCommitFailure = 7
	InputPathDoesNotExist = 8
	ResultPathDoesNotExist = 9
	SuccessButIncompatibleFem = 10

class ZoneCreationStatus(Enum):
	'''
	Indicates whether a zone was created successfully. 
            If not, this indicates why the zone was not created.
	'''
	Success = 1
	DuplicateNameFailure = 2
	InvalidFamilyCategory = 3

class ZoneIdUpdateStatus(Enum):
	Success = 1
	DuplicateIdFailure = 2
	IdOutOfRangeError = 3

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
		result = self._Entity.MarginCode
		return types.MarginCode[result.ToString()] if result is not None else None

	def CompareTo(self, other) -> int:
		return self._Entity.CompareTo(other._Entity)


class AnalysisDetail:
	def __init__(self, analysisDetail: _api.AnalysisDetail):
		self._Entity = analysisDetail

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Path(self) -> list[str]:
		return [string for string in self._Entity.Path]

	@property
	def DataType(self) -> type:
		return self._Entity.DataType

	@property
	def Value(self) -> object:
		return self._Entity.Value

	@property
	def AnalysisDetails(self) -> AnalysisDetailCol:
		result = self._Entity.AnalysisDetails
		return AnalysisDetailCol(result) if result is not None else None

	def GetValue(self) -> object:
		return self._Entity.GetValue()


class AnalysisDetailCol(Generic[T]):
	def __init__(self, analysisDetailCol: _api.AnalysisDetailCol):
		self._Entity = analysisDetailCol

	@property
	def AnalysisDetailColList(self) -> tuple[AnalysisDetail]:
		return tuple([AnalysisDetail(analysisDetailCol) for analysisDetailCol in self._Entity])

	@overload
	def Get(self, name: str) -> AnalysisDetail: ...

	@overload
	def Get(self, path: tuple[str]) -> AnalysisDetail: ...

	def Get(self, item1 = None) -> AnalysisDetail:
		if isinstance(item1, str):
			return AnalysisDetail(self._Entity.Get(item1))

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], str):
			pathList = List[str]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						pathList.Add(thing)
			pathEnumerable = IEnumerable(pathList)
			return AnalysisDetail(self._Entity.Get(pathEnumerable))

		return AnalysisDetail(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.AnalysisDetailColList[index]

	def __iter__(self):
		yield from self.AnalysisDetailColList

	def __len__(self):
		return len(self.AnalysisDetailColList)


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
		result = self._Entity.LimitUltimate
		return types.LimitUltimate[result.ToString()] if result is not None else None

	@property
	def LoadCaseId(self) -> int:
		return self._Entity.LoadCaseId

	@property
	def ScenarioId(self) -> int:
		return self._Entity.ScenarioId

	@property
	def Margin(self) -> Margin:
		'''
		Represents a Margin result.
		'''
		result = self._Entity.Margin
		return Margin(result) if result is not None else None

	@property
	def AnalysisDefinition(self) -> AnalysisDefinition:
		result = self._Entity.AnalysisDefinition
		return AnalysisDefinition(result) if result is not None else None

	@property
	def AnalysisDetails(self) -> AnalysisDetailCol:
		result = self._Entity.AnalysisDetails
		return AnalysisDetailCol(result) if result is not None else None


class JointAnalysisResult(AnalysisResult):
	def __init__(self, jointAnalysisResult: _api.JointAnalysisResult):
		self._Entity = jointAnalysisResult

	@property
	def ObjectId(self) -> types.JointObject:
		'''
		Enum identifying the possible entities within a joint
		'''
		result = self._Entity.ObjectId
		return types.JointObject[result.ToString()] if result is not None else None


class ZoneAnalysisResult(AnalysisResult):
	def __init__(self, zoneAnalysisResult: _api.ZoneAnalysisResult):
		self._Entity = zoneAnalysisResult


class ZoneAnalysisConceptResult(ZoneAnalysisResult):
	def __init__(self, zoneAnalysisConceptResult: _api.ZoneAnalysisConceptResult):
		self._Entity = zoneAnalysisConceptResult

	@property
	def ConceptId(self) -> types.FamilyConceptUID:
		result = self._Entity.ConceptId
		return types.FamilyConceptUID[result.ToString()] if result is not None else None


class ZoneAnalysisObjectResult(ZoneAnalysisResult):
	def __init__(self, zoneAnalysisObjectResult: _api.ZoneAnalysisObjectResult):
		self._Entity = zoneAnalysisObjectResult

	@property
	def ObjectId(self) -> types.FamilyObjectUID:
		result = self._Entity.ObjectId
		return types.FamilyObjectUID[result.ToString()] if result is not None else None


class ZoneAnalysisSolverResult(ZoneAnalysisResult):
	def __init__(self, zoneAnalysisSolverResult: _api.ZoneAnalysisSolverResult):
		self._Entity = zoneAnalysisSolverResult

	def Create_ZoneAnalysisSolverResult(limitUltimate: types.LimitUltimate, loadCaseId: int, scenarioId: int, margin: Margin, analysisDefinition: AnalysisDefinition, analysisObjectTag: Enum, analysisObjectIndex: int, analysisDetails: AnalysisDetailCol):
		return ZoneAnalysisSolverResult(_api.ZoneAnalysisSolverResult(_types.LimitUltimate(limitUltimate.value), loadCaseId, scenarioId, margin._Entity, analysisDefinition._Entity, analysisObjectTag._Entity, analysisObjectIndex, analysisDetails._Entity))

	@property
	def AnalysisObjectTag(self) -> Enum:
		result = self._Entity.AnalysisObjectTag
		thisClass = type(result).__name__
		givenClass = Enum
		for subclass in Enum.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def AnalysisObjectIndex(self) -> int:
		return self._Entity.AnalysisObjectIndex

	def GetFamilyObjectUID(self, familyId: types.BeamPanelFamily, conceptId: int) -> types.FamilyObjectUID:
		return types.FamilyObjectUID(self._Entity.GetFamilyObjectUID(_types.BeamPanelFamily(familyId.value), conceptId))


class AssignableProperty(IdNameEntity):
	def __init__(self, assignableProperty: _api.AssignableProperty):
		self._Entity = assignableProperty


class AssignablePropertyWithFamilyCategory(AssignableProperty):
	def __init__(self, assignablePropertyWithFamilyCategory: _api.AssignablePropertyWithFamilyCategory):
		self._Entity = assignablePropertyWithFamilyCategory

	@property
	def FamilyCategory(self) -> types.FamilyCategory:
		result = self._Entity.FamilyCategory
		return types.FamilyCategory[result.ToString()] if result is not None else None


class FailureObjectGroup(IdNameEntity):
	def __init__(self, failureObjectGroup: _api.FailureObjectGroup):
		self._Entity = failureObjectGroup

	@property
	def ObjectGroup(self) -> types.ObjectGroup:
		result = self._Entity.ObjectGroup
		return types.ObjectGroup[result.ToString()] if result is not None else None

	@property
	def IsEnabled(self) -> bool:
		return self._Entity.IsEnabled

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		'''
		Limit vs Ultimate loads.
		'''
		result = self._Entity.LimitUltimate
		return types.LimitUltimate[result.ToString()] if result is not None else None

	@property
	def RequiredMargin(self) -> float:
		return self._Entity.RequiredMargin

	@IsEnabled.setter
	def IsEnabled(self, value: bool) -> None:
		self._Entity.IsEnabled = value

	@LimitUltimate.setter
	def LimitUltimate(self, value: types.LimitUltimate) -> None:
		self._Entity.LimitUltimate = _types.LimitUltimate(value.value)

	@RequiredMargin.setter
	def RequiredMargin(self, value: float) -> None:
		self._Entity.RequiredMargin = value


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
		result = self._Entity.DataType
		return types.UserConstantDataType[result.ToString()] if result is not None else None

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

	def SetStringValue(self, value: str) -> None:
		return self._Entity.SetStringValue(value)

	def SetIntValue(self, value: int) -> None:
		return self._Entity.SetIntValue(value)

	def SetFloatValue(self, value: float) -> None:
		return self._Entity.SetFloatValue(value)

	def SetBoolValue(self, value: bool) -> None:
		return self._Entity.SetBoolValue(value)

	def SetSelectionValue(self, index: int) -> None:
		'''
		Set enum value by index.
		'''
		return self._Entity.SetSelectionValue(index)


class IdEntityCol(Generic[T], ABC):
	def __init__(self, idEntityCol: _api.IdEntityCol):
		self._Entity = idEntityCol

	@property
	def IdEntityColList(self) -> tuple[IdEntity]:
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = IdEntity
		for subclass in IdEntity.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(idEntityCol) for idEntityCol in self._Entity])

	@property
	def Ids(self) -> tuple[int]:
		return tuple([int32 for int32 in self._Entity.Ids])

	def Contains(self, id: int) -> bool:
		return self._Entity.Contains(id)

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, id: int) -> IdEntity:
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
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = T
		for subclass in T.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(idNameEntityCol) for idNameEntityCol in self._Entity])

	@property
	def Names(self) -> tuple[str]:
		return tuple([string for string in self._Entity.Names])

	@overload
	def Get(self, name: str) -> IdNameEntity: ...

	@overload
	def Get(self, id: int) -> IdNameEntity: ...

	def Get(self, item1 = None) -> IdNameEntity:
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
	def Get(self, objectGroup: types.ObjectGroup) -> FailureObjectGroup: ...

	@overload
	def Get(self, name: str) -> FailureObjectGroup: ...

	@overload
	def Get(self, id: int) -> FailureObjectGroup: ...

	def Get(self, item1 = None) -> FailureObjectGroup:
		if isinstance(item1, types.ObjectGroup):
			return FailureObjectGroup(self._Entity.Get(_types.ObjectGroup(item1.value)))

		if isinstance(item1, str):
			return FailureObjectGroup(super().Get(item1))

		if isinstance(item1, int):
			return FailureObjectGroup(super().Get(item1))

		return FailureObjectGroup(self._Entity.Get(_types.ObjectGroup(item1.value)))

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
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = FailureSetting
			for subclass in FailureSetting.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = FailureSetting
			for subclass in FailureSetting.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = FailureSetting
		for subclass in FailureSetting.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

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
		result = self._Entity.LimitUltimate
		return types.LimitUltimate[result.ToString()] if result is not None else None

	@property
	def ObjectGroups(self) -> FailureObjectGroupCol:
		result = self._Entity.ObjectGroups
		return FailureObjectGroupCol(result) if result is not None else None

	@property
	def RequiredMargin(self) -> float:
		return self._Entity.RequiredMargin

	@property
	def Settings(self) -> FailureSettingCol:
		result = self._Entity.Settings
		return FailureSettingCol(result) if result is not None else None

	@IsEnabled.setter
	def IsEnabled(self, value: bool) -> None:
		self._Entity.IsEnabled = value

	@LimitUltimate.setter
	def LimitUltimate(self, value: types.LimitUltimate) -> None:
		self._Entity.LimitUltimate = _types.LimitUltimate(value.value)

	@RequiredMargin.setter
	def RequiredMargin(self, value: float) -> None:
		self._Entity.RequiredMargin = value


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

		return FailureCriterion(self._Entity.Get(item1))

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
		result = self._Entity.Criteria
		return FailureCriterionCol(result) if result is not None else None

	@property
	def Settings(self) -> FailureSettingCol:
		result = self._Entity.Settings
		return FailureSettingCol(result) if result is not None else None


class FailureModeCol(IdNameEntityCol[FailureMode]):
	def __init__(self, failureModeCol: _api.FailureModeCol):
		self._Entity = failureModeCol
		self._CollectedClass = FailureMode

	@property
	def FailureModeColList(self) -> tuple[FailureMode]:
		return tuple([FailureMode(failureModeCol) for failureModeCol in self._Entity])

	@overload
	def CreateFailureMode(self, failureModeCategoryId: int, name: str = None) -> FailureMode: ...

	@overload
	def CreateFailureMode(self, failureModeCategory: str, name: str = None) -> FailureMode: ...

	@overload
	def Get(self, name: str) -> FailureMode: ...

	@overload
	def Get(self, id: int) -> FailureMode: ...

	def CreateFailureMode(self, item1 = None, item2 = None) -> FailureMode:
		if isinstance(item1, int) and isinstance(item2, str):
			return FailureMode(self._Entity.CreateFailureMode(item1, item2))

		if isinstance(item1, str) and isinstance(item2, str):
			return FailureMode(self._Entity.CreateFailureMode(item1, item2))

		return FailureMode(self._Entity.CreateFailureMode(item1, item2))

	def Get(self, item1 = None) -> FailureMode:
		if isinstance(item1, str):
			return FailureMode(super().Get(item1))

		if isinstance(item1, int):
			return FailureMode(super().Get(item1))

		return FailureMode(self._Entity.Get(item1))

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
		result = self._Entity.FailureModes
		return FailureModeCol(result) if result is not None else None

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

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return self._Entity.AddFailureMode(idsEnumerable)

		return self._Entity.AddFailureMode(item1)

	def RemoveFailureMode(self, item1 = None) -> None:
		if isinstance(item1, int):
			return self._Entity.RemoveFailureMode(item1)

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return self._Entity.RemoveFailureMode(idsEnumerable)

		return self._Entity.RemoveFailureMode(item1)


class DesignProperty(AssignablePropertyWithFamilyCategory):
	def __init__(self, designProperty: _api.DesignProperty):
		self._Entity = designProperty

	def Copy(self, newName: str = None) -> DesignProperty:
		'''
		Creates a copy of this DesignProperty.
		'''
		result = self._Entity.Copy(newName)
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in DesignProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None


class LoadProperty(AssignableProperty):
	def __init__(self, loadProperty: _api.LoadProperty):
		self._Entity = loadProperty

	@property
	def Category(self) -> types.FamilyCategory:
		result = self._Entity.Category
		return types.FamilyCategory[result.ToString()] if result is not None else None

	@property
	def Type(self) -> types.LoadPropertyType:
		result = self._Entity.Type
		return types.LoadPropertyType[result.ToString()] if result is not None else None

	@property
	def IsZeroCurvature(self) -> bool:
		return self._Entity.IsZeroCurvature

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate


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
		result = self._Entity.SolutionType
		return types.FeaSolutionType[result.ToString()] if result is not None else None


class DesignLoadSubcaseMultiplier(IdNameEntity):
	def __init__(self, designLoadSubcaseMultiplier: _api.DesignLoadSubcaseMultiplier):
		self._Entity = designLoadSubcaseMultiplier

	@property
	def LimitFactor(self) -> float:
		return self._Entity.LimitFactor

	@property
	def Subcase(self) -> DesignLoadSubcase:
		result = self._Entity.Subcase
		return DesignLoadSubcase(result) if result is not None else None

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
		result = self._Entity.Subcase
		return DesignLoadSubcase(result) if result is not None else None

	@property
	def TemperatureChoiceType(self) -> types.TemperatureChoiceType:
		'''
		Load Case Setting selection for analysis and initial temperature.
		'''
		result = self._Entity.TemperatureChoiceType
		return types.TemperatureChoiceType[result.ToString()] if result is not None else None

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

		return DesignLoadSubcaseMultiplier(self._Entity.Get(item1))

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
		result = self._Entity.AnalysisTemperature
		return DesignLoadSubcaseTemperature(result) if result is not None else None

	@property
	def InitialTemperature(self) -> DesignLoadSubcaseTemperature:
		result = self._Entity.InitialTemperature
		return DesignLoadSubcaseTemperature(result) if result is not None else None

	@property
	def Description(self) -> str:
		return self._Entity.Description

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
		result = self._Entity.SubcaseMultipliers
		return DesignLoadSubcaseMultiplierCol(result) if result is not None else None

	@property
	def Types(self) -> list[types.LoadCaseType]:
		return [types.LoadCaseType[loadCaseType.ToString()] for loadCaseType in self._Entity.Types]

	@property
	def UID(self) -> Guid:
		return self._Entity.UID


class JointDesignResult(IdEntity):
	def __init__(self, jointDesignResult: _api.JointDesignResult):
		self._Entity = jointDesignResult


class ZoneDesignResult(IdEntity):
	def __init__(self, zoneDesignResult: _api.ZoneDesignResult):
		self._Entity = zoneDesignResult

	@property
	def VariableParameter(self) -> types.VariableParameter:
		result = self._Entity.VariableParameter
		return types.VariableParameter[result.ToString()] if result is not None else None

	@property
	def Value(self) -> float:
		return self._Entity.Value

	@property
	def MaterialId(self) -> int:
		return self._Entity.MaterialId

	@property
	def MaterialType(self) -> types.MaterialType:
		result = self._Entity.MaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Material(self) -> str:
		return self._Entity.Material


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
	def Equals(self, obj: object) -> bool: ...

	def Equals(self, item1 = None) -> bool:
		if isinstance(item1, Vector3d):
			return self._Entity.Equals(item1._Entity)

		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		return self._Entity.Equals(item1._Entity)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


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
		result = self._Entity.DataType
		return types.DiscreteFieldDataType[result.ToString()] if result is not None else None

	@property
	def PhysicalEntityType(self) -> types.DiscreteFieldPhysicalEntityType:
		'''
		Defines the type of physical entity that a Discrete Field applies to, such as zone, element, joint, etc.
		'''
		result = self._Entity.PhysicalEntityType
		return types.DiscreteFieldPhysicalEntityType[result.ToString()] if result is not None else None

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
		'''
		Create a new column with the given name. Returns the Id of the newly created column
		'''
		return self._Entity.AddColumn(name)

	def AddPointRow(self, pointId: Vector3d) -> None:
		'''
		Create an empty row in a point-based table.
		'''
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
	def SetNumericValues(self, valuesByEntityId: dict[int, tuple[float]]) -> None: ...

	@overload
	def SetNumericValue(self, pointId: Vector3d, columnId: int, value: float) -> None: ...

	@overload
	def SetNumericValues(self, valuesByPoint: dict[Vector3d, tuple[float]]) -> None: ...

	@overload
	def SetStringValue(self, entityId: int, columnId: int, value: str) -> None: ...

	@overload
	def SetStringValues(self, valuesByEntityId: dict[int, tuple[str]]) -> None: ...

	@overload
	def SetStringValue(self, pointId: Vector3d, columnId: int, value: str) -> None: ...

	@overload
	def SetStringValues(self, valuesByPoint: dict[Vector3d, tuple[str]]) -> None: ...

	def DeleteAllRows(self) -> None:
		'''
		Delete all rows for this discrete field.
		'''
		return self._Entity.DeleteAllRows()

	def DeleteColumn(self, columnId: int) -> None:
		'''
		Delete a specified column for this discrete field. Columns are 1-indexed.
		'''
		return self._Entity.DeleteColumn(columnId)

	def DeletePointRow(self, pointId: Vector3d) -> None:
		'''
		Delete a specific row for a point-based table.
		'''
		return self._Entity.DeletePointRow(pointId._Entity)

	def DeleteRow(self, entityId: int) -> None:
		'''
		Delete a specific row for a non-point-based table.
		'''
		return self._Entity.DeleteRow(entityId)

	def DeleteRowsAndColumns(self) -> None:
		'''
		Delete all rows and columns for this discrete field.
		'''
		return self._Entity.DeleteRowsAndColumns()

	def ReadNumericCell(self, item1 = None, item2 = None) -> float:
		if isinstance(item1, int) and isinstance(item2, int):
			return float(self._Entity.ReadNumericCell(item1, item2))

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return float(self._Entity.ReadNumericCell(item1._Entity, item2))

		return float(self._Entity.ReadNumericCell(item1, item2))

	def ReadStringCell(self, item1 = None, item2 = None) -> str:
		if isinstance(item1, int) and isinstance(item2, int):
			return self._Entity.ReadStringCell(item1, item2)

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return self._Entity.ReadStringCell(item1._Entity, item2)

		return self._Entity.ReadStringCell(item1, item2)

	def SetNumericValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, int) and isinstance(item3, float) and (isinstance(item3, float) or isinstance(item3, int)):
			return self._Entity.SetNumericValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and isinstance(item3, float) and (isinstance(item3, float) or isinstance(item3, int)):
			return self._Entity.SetNumericValue(item1._Entity, item2, item3)

		return self._Entity.SetNumericValue(item1, item2, item3)

	def SetNumericValues(self, item1 = None) -> None:
		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], int) and isinstance(list(item1.values())[0], tuple) and list(item1.values())[0] and (isinstance(list(item1.values())[0][0], float) or list(item1.values())[0][0] is None or isinstance(list(item1.values())[0][0], int)):
			valuesByEntityIdDict = Dictionary[int, IEnumerable[Nullable[Double]]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[Nullable[Double]]()
				if dictValue is not None:
					for thing in dictValue:
						dictValueList.Add(thing)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByEntityIdDict.Add(kvp, dictValueEnumerable)
			return self._Entity.SetNumericValues(valuesByEntityIdDict)

		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], Vector3d) and isinstance(list(item1.values())[0], tuple) and list(item1.values())[0] and (isinstance(list(item1.values())[0][0], float) or list(item1.values())[0][0] is None or isinstance(list(item1.values())[0][0], int)):
			valuesByPointDict = Dictionary[_api.Vector3d, IEnumerable[Nullable[Double]]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[Nullable[Double]]()
				if dictValue is not None:
					for thing in dictValue:
						dictValueList.Add(thing)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByPointDict.Add(kvp._Entity, dictValueEnumerable)
			return self._Entity.SetNumericValues(valuesByPointDict)

		return self._Entity.SetNumericValues(item1)

	def SetStringValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, int) and isinstance(item3, str):
			return self._Entity.SetStringValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and isinstance(item3, str):
			return self._Entity.SetStringValue(item1._Entity, item2, item3)

		return self._Entity.SetStringValue(item1, item2, item3)

	def SetStringValues(self, item1 = None) -> None:
		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], int) and isinstance(list(item1.values())[0], tuple) and list(item1.values())[0] and isinstance(list(item1.values())[0][0], str):
			valuesByEntityIdDict = Dictionary[int, IEnumerable[String]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[str]()
				if dictValue is not None:
					for thing in dictValue:
						if thing is not None:
							dictValueList.Add(thing)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByEntityIdDict.Add(kvp, dictValueEnumerable)
			return self._Entity.SetStringValues(valuesByEntityIdDict)

		if isinstance(item1, dict) and item1 and isinstance(list(item1.keys())[0], Vector3d) and isinstance(list(item1.values())[0], tuple) and list(item1.values())[0] and isinstance(list(item1.values())[0][0], str):
			valuesByPointDict = Dictionary[_api.Vector3d, IEnumerable[String]]()
			for kvp in item1:
				dictValue = item1[kvp]
				dictValueList = List[str]()
				if dictValue is not None:
					for thing in dictValue:
						if thing is not None:
							dictValueList.Add(thing)
				dictValueEnumerable = IEnumerable(dictValueList)
				valuesByPointDict.Add(kvp._Entity, dictValueEnumerable)
			return self._Entity.SetStringValues(valuesByPointDict)

		return self._Entity.SetStringValues(item1)


class Node(IdEntity):
	def __init__(self, node: _api.Node):
		self._Entity = node

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@property
	def Z(self) -> float:
		return self._Entity.Z


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
		result = self._Entity.Centroid
		return Centroid(result) if result is not None else None

	@property
	def Nodes(self) -> list[Node]:
		return [Node(node) for node in self._Entity.Nodes]


class FailureModeCategory(IdNameEntity):
	def __init__(self, failureModeCategory: _api.FailureModeCategory):
		self._Entity = failureModeCategory

	@property
	def PackageId(self) -> int:
		return self._Entity.PackageId


class Folder(IdNameEntity):
	def __init__(self, folder: _api.Folder):
		self._Entity = folder

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def ChildFolders(self) -> FolderCol:
		result = self._Entity.ChildFolders
		return FolderCol(result) if result is not None else None

	@property
	def Items(self) -> list[IdNameEntity]:
		result = self._Entity.Items
		if result.Count > 0:
			thisClass = type(result[0]).__name__
			givenClass = IdNameEntity
			for subclass in all_subclasses(givenClass):
				if subclass.__name__ == thisClass:
					givenClass = subclass
		return [givenClass(idNameEntity) for idNameEntity in result]

	def AddItem(self, item: IdNameEntity) -> None:
		return self._Entity.AddItem(item._Entity)

	def AddItems(self, items: tuple[IdNameEntity]) -> None:
		itemsList = List[type(items[0]._Entity)]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return self._Entity.AddItems(itemsEnumerable)

	def RemoveItem(self, item: IdNameEntity) -> None:
		return self._Entity.RemoveItem(item._Entity)

	def RemoveItems(self, items: tuple[IdNameEntity]) -> None:
		itemsList = List[type(items[0]._Entity)]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return self._Entity.RemoveItems(itemsEnumerable)


class EntityWithAssignableProperties(IdNameEntityRenameable):
	def __init__(self, entityWithAssignableProperties: _api.EntityWithAssignableProperties):
		self._Entity = entityWithAssignableProperties

	@property
	def AssignedAnalysisProperty(self) -> AnalysisProperty:
		result = self._Entity.AssignedAnalysisProperty
		return AnalysisProperty(result) if result is not None else None

	@property
	def AssignedDesignProperty(self) -> DesignProperty:
		result = self._Entity.AssignedDesignProperty
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in DesignProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def AssignedLoadProperty(self) -> LoadProperty:
		result = self._Entity.AssignedLoadProperty
		thisClass = type(result).__name__
		givenClass = LoadProperty
		for subclass in LoadProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def AssignAnalysisProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignAnalysisProperty(id).ToString()]

	def AssignDesignProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignDesignProperty(id).ToString()]

	def AssignLoadProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignLoadProperty(id).ToString()]

	def AssignProperty(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		'''
		Assign a Property to this entity.
		'''
		return PropertyAssignmentStatus[self._Entity.AssignProperty(property._Entity).ToString()]


class AnalysisResultCol(Generic[T]):
	def __init__(self, analysisResultCol: _api.AnalysisResultCol):
		self._Entity = analysisResultCol

	@property
	def AnalysisResultColList(self) -> tuple[AnalysisResult]:
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = AnalysisResult
		for subclass in AnalysisResult.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(analysisResultCol) for analysisResultCol in self._Entity])

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
		result = self._Entity.GetControllingResult()
		thisClass = type(result).__name__
		givenClass = AnalysisResult
		for subclass in AnalysisResult.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@abstractmethod
	def GetAllResults(self) -> AnalysisResultCol:
		'''
		Obselete. Use ``hyperx.api.ZoneJointEntity.GetControllingResultsPerCriterion`` instead.
		'''
		return AnalysisResultCol(self._Entity.GetAllResults())

	@abstractmethod
	def GetControllingResultsPerCriterion(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetControllingResultsPerCriterion())


class JointDesignResultCol(IdEntityCol[JointDesignResult]):
	def __init__(self, jointDesignResultCol: _api.JointDesignResultCol):
		self._Entity = jointDesignResultCol
		self._CollectedClass = JointDesignResult

	@property
	def JointDesignResultColList(self) -> tuple[JointDesignResult]:
		return tuple([JointDesignResult(jointDesignResultCol) for jointDesignResultCol in self._Entity])

	@overload
	def Get(self, jointSelectionId: types.JointSelectionId) -> JointDesignResult: ...

	@overload
	def Get(self, jointRangeId: types.JointRangeId) -> JointDesignResult: ...

	@overload
	def Get(self, id: int) -> JointDesignResult: ...

	def Get(self, item1 = None) -> JointDesignResult:
		if isinstance(item1, types.JointSelectionId):
			result = self._Entity.Get(_types.JointSelectionId(item1.value))
			thisClass = type(result).__name__
			givenClass = JointDesignResult
			for subclass in JointDesignResult.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, types.JointRangeId):
			result = self._Entity.Get(_types.JointRangeId(item1.value))
			thisClass = type(result).__name__
			givenClass = JointDesignResult
			for subclass in JointDesignResult.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = JointDesignResult
			for subclass in JointDesignResult.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(_types.JointSelectionId(item1.value))
		thisClass = type(result).__name__
		givenClass = JointDesignResult
		for subclass in JointDesignResult.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.JointDesignResultColList[index]

	def __iter__(self):
		yield from self.JointDesignResultColList

	def __len__(self):
		return len(self.JointDesignResultColList)


class Joint(ZoneJointEntity):
	def __init__(self, joint: _api.Joint):
		self._Entity = joint

	@property
	def JointRangeSizingResults(self) -> JointDesignResultCol:
		result = self._Entity.JointRangeSizingResults
		return JointDesignResultCol(result) if result is not None else None

	@property
	def JointSelectionSizingResults(self) -> JointDesignResultCol:
		result = self._Entity.JointSelectionSizingResults
		return JointDesignResultCol(result) if result is not None else None

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetAllResults())

	def GetControllingResultsPerCriterion(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetControllingResultsPerCriterion())

	def GetControllingResult(self) -> AnalysisResult:
		result = self._Entity.GetControllingResult()
		thisClass = type(result).__name__
		givenClass = AnalysisResult
		for subclass in AnalysisResult.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())


class ZoneDesignResultCol(IdEntityCol[ZoneDesignResult]):
	def __init__(self, zoneDesignResultCol: _api.ZoneDesignResultCol):
		self._Entity = zoneDesignResultCol
		self._CollectedClass = ZoneDesignResult

	@property
	def ZoneDesignResultColList(self) -> tuple[ZoneDesignResult]:
		return tuple([ZoneDesignResult(zoneDesignResultCol) for zoneDesignResultCol in self._Entity])

	@property
	def Weight(self) -> float:
		return self._Entity.Weight

	@overload
	def Get(self, parameterId: types.VariableParameter) -> ZoneDesignResult: ...

	@overload
	def Get(self, id: int) -> ZoneDesignResult: ...

	def Get(self, item1 = None) -> ZoneDesignResult:
		if isinstance(item1, types.VariableParameter):
			return ZoneDesignResult(self._Entity.Get(_types.VariableParameter(item1.value)))

		if isinstance(item1, int):
			return ZoneDesignResult(super().Get(item1))

		return ZoneDesignResult(self._Entity.Get(_types.VariableParameter(item1.value)))

	def __getitem__(self, index: int):
		return self.ZoneDesignResultColList[index]

	def __iter__(self):
		yield from self.ZoneDesignResultColList

	def __len__(self):
		return len(self.ZoneDesignResultColList)


class ZoneBase(ZoneJointEntity):
	'''
	Abstract for regular Zones and Panel Segments.
	'''
	def __init__(self, zoneBase: _api.ZoneBase):
		self._Entity = zoneBase

	@property
	def Centroid(self) -> Centroid:
		result = self._Entity.Centroid
		return Centroid(result) if result is not None else None

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def Weight(self) -> float:
		return self._Entity.Weight

	@property
	def NonOptimumFactor(self) -> float:
		return self._Entity.NonOptimumFactor

	@property
	def AddedWeight(self) -> float:
		return self._Entity.AddedWeight

	@property
	def SuperimposePanel(self) -> bool:
		return self._Entity.SuperimposePanel

	@property
	def BucklingImperfection(self) -> float:
		return self._Entity.BucklingImperfection

	@property
	def IsBeamColumn(self) -> bool:
		return self._Entity.IsBeamColumn

	@property
	def SuperimposeBoundaryCondition(self) -> int:
		return self._Entity.SuperimposeBoundaryCondition

	@property
	def IsZeroOutFeaMoments(self) -> bool:
		return self._Entity.IsZeroOutFeaMoments

	@property
	def IsZeroOutFeaTransverseShears(self) -> bool:
		return self._Entity.IsZeroOutFeaTransverseShears

	@property
	def MechanicalLimit(self) -> float:
		return self._Entity.MechanicalLimit

	@property
	def MechanicalUltimate(self) -> float:
		return self._Entity.MechanicalUltimate

	@property
	def ThermalHelp(self) -> float:
		return self._Entity.ThermalHelp

	@property
	def ThermalHurt(self) -> float:
		return self._Entity.ThermalHurt

	@property
	def FatigueKTSkin(self) -> float:
		return self._Entity.FatigueKTSkin

	@property
	def FatigueKTStiff(self) -> float:
		return self._Entity.FatigueKTStiff

	@property
	def XSpan(self) -> float:
		return self._Entity.XSpan

	@property
	def EARequired(self) -> float:
		return self._Entity.EARequired

	@property
	def EI1Required(self) -> float:
		return self._Entity.EI1Required

	@property
	def EI2Required(self) -> float:
		return self._Entity.EI2Required

	@property
	def GJRequired(self) -> float:
		return self._Entity.GJRequired

	@property
	def EAAuto(self) -> float:
		return self._Entity.EAAuto

	@property
	def EI1Auto(self) -> float:
		return self._Entity.EI1Auto

	@property
	def EI2Auto(self) -> float:
		return self._Entity.EI2Auto

	@property
	def GJAuto(self) -> float:
		return self._Entity.GJAuto

	@property
	def Ex(self) -> float:
		return self._Entity.Ex

	@property
	def Dmid(self) -> float:
		return self._Entity.Dmid

	def GetObjectName(self, objectId: types.FamilyObjectUID) -> str:
		return self._Entity.GetObjectName(_types.FamilyObjectUID(objectId.value))

	def GetConceptName(self) -> str:
		return self._Entity.GetConceptName()

	def GetZoneDesignResults(self, solutionId: int = 1) -> ZoneDesignResultCol:
		'''
		Returns a collection of Zone Design Results for a Solution Id (default 1)
		'''
		return ZoneDesignResultCol(self._Entity.GetZoneDesignResults(solutionId))

	def RenumberZone(self, newId: int) -> ZoneIdUpdateStatus:
		'''
		Attempt to update a zone's ID.
		'''
		return ZoneIdUpdateStatus[self._Entity.RenumberZone(newId).ToString()]

	def GetResults(self) -> AnalysisResultCol:
		'''
		Get all analysis results for this zone.
            Note, analysis details must be available to get results.
            If analysis details are unavailable, use ``hyperx.api.ZoneBase.GetControllingResultsPerCriterion`` or rerun analysis to populate them.
		'''
		return AnalysisResultCol(self._Entity.GetResults())

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetAllResults())

	def GetControllingResultsPerCriterion(self) -> AnalysisResultCol:
		return AnalysisResultCol(self._Entity.GetControllingResultsPerCriterion())

	def GetControllingResult(self) -> AnalysisResult:
		result = self._Entity.GetControllingResult()
		thisClass = type(result).__name__
		givenClass = AnalysisResult
		for subclass in AnalysisResult.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def GetMinimumMargin(self) -> Margin:
		return Margin(self._Entity.GetMinimumMargin())

	@NonOptimumFactor.setter
	def NonOptimumFactor(self, value: float) -> None:
		self._Entity.NonOptimumFactor = value

	@AddedWeight.setter
	def AddedWeight(self, value: float) -> None:
		self._Entity.AddedWeight = value

	@SuperimposePanel.setter
	def SuperimposePanel(self, value: bool) -> None:
		self._Entity.SuperimposePanel = value

	@BucklingImperfection.setter
	def BucklingImperfection(self, value: float) -> None:
		self._Entity.BucklingImperfection = value

	@IsBeamColumn.setter
	def IsBeamColumn(self, value: bool) -> None:
		self._Entity.IsBeamColumn = value

	@SuperimposeBoundaryCondition.setter
	def SuperimposeBoundaryCondition(self, value: int) -> None:
		self._Entity.SuperimposeBoundaryCondition = value

	@IsZeroOutFeaMoments.setter
	def IsZeroOutFeaMoments(self, value: bool) -> None:
		self._Entity.IsZeroOutFeaMoments = value

	@IsZeroOutFeaTransverseShears.setter
	def IsZeroOutFeaTransverseShears(self, value: bool) -> None:
		self._Entity.IsZeroOutFeaTransverseShears = value

	@MechanicalLimit.setter
	def MechanicalLimit(self, value: float) -> None:
		self._Entity.MechanicalLimit = value

	@MechanicalUltimate.setter
	def MechanicalUltimate(self, value: float) -> None:
		self._Entity.MechanicalUltimate = value

	@ThermalHelp.setter
	def ThermalHelp(self, value: float) -> None:
		self._Entity.ThermalHelp = value

	@ThermalHurt.setter
	def ThermalHurt(self, value: float) -> None:
		self._Entity.ThermalHurt = value

	@FatigueKTSkin.setter
	def FatigueKTSkin(self, value: float) -> None:
		self._Entity.FatigueKTSkin = value

	@FatigueKTStiff.setter
	def FatigueKTStiff(self, value: float) -> None:
		self._Entity.FatigueKTStiff = value

	@XSpan.setter
	def XSpan(self, value: float) -> None:
		self._Entity.XSpan = value

	@EARequired.setter
	def EARequired(self, value: float) -> None:
		self._Entity.EARequired = value

	@EI1Required.setter
	def EI1Required(self, value: float) -> None:
		self._Entity.EI1Required = value

	@EI2Required.setter
	def EI2Required(self, value: float) -> None:
		self._Entity.EI2Required = value

	@GJRequired.setter
	def GJRequired(self, value: float) -> None:
		self._Entity.GJRequired = value

	@Ex.setter
	def Ex(self, value: float) -> None:
		self._Entity.Ex = value

	@Dmid.setter
	def Dmid(self, value: float) -> None:
		self._Entity.Dmid = value


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
		return tuple([types.DiscreteDefinitionType[discreteDefinitionType.ToString()] for discreteDefinitionType in self._Entity.Skins])

	@property
	def Objects(self) -> tuple[types.DiscreteDefinitionType]:
		return tuple([types.DiscreteDefinitionType[discreteDefinitionType.ToString()] for discreteDefinitionType in self._Entity.Objects])

	@property
	def DiscreteTechnique(self) -> types.DiscreteTechnique:
		result = self._Entity.DiscreteTechnique
		return types.DiscreteTechnique[result.ToString()] if result is not None else None

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
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

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
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = T
		for subclass in T.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(entityWithAssignablePropertiesCol) for entityWithAssignablePropertiesCol in self._Entity])

	def AssignPropertyToAll(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self._Entity.AssignPropertyToAll(property._Entity).ToString()]

	@overload
	def Get(self, name: str) -> EntityWithAssignableProperties: ...

	@overload
	def Get(self, id: int) -> EntityWithAssignableProperties: ...

	def Get(self, item1 = None) -> EntityWithAssignableProperties:
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

		return Joint(self._Entity.Get(item1))

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

		return PanelSegment(self._Entity.Get(item1))

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
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = Zone
			for subclass in Zone.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = Zone
			for subclass in Zone.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = Zone
		for subclass in Zone.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

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
		result = self._Entity.Centroid
		return Centroid(result) if result is not None else None

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

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
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	@abstractmethod
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	@abstractmethod
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def AddZones(self, ids: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	@abstractmethod
	def AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	@abstractmethod
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	@abstractmethod
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	@abstractmethod
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus: ...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.AddJoint(item1).ToString()]

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.RemoveJoint(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Joint):
			jointsList = List[_api.Joint]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						jointsList.Add(thing._Entity)
			jointsEnumerable = IEnumerable(jointsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointsEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveJoints(item1).ToString()]

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.AddZone(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

	def AddZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			idsList = MakeCSharpIntList(item1)
			idsEnumerable = IEnumerable(idsList)
			return CollectionModificationStatus[self._Entity.AddZones(idsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Zone):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.AddZones(zonesEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.AddZones(item1).ToString()]

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self._Entity.RemoveZone(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Zone):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zonesEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.RemoveZones(item1).ToString()]

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.AddPanelSegment(item1).ToString()]

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1._Entity).ToString()]

		return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], PanelSegment):
			segmentsList = List[_api.PanelSegment]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						segmentsList.Add(thing._Entity)
			segmentsEnumerable = IEnumerable(segmentsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentsEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.RemovePanelSegments(item1).ToString()]


class AutomatedConstraint(IdNameEntityRenameable):
	def __init__(self, automatedConstraint: _api.AutomatedConstraint):
		self._Entity = automatedConstraint

	@property
	def ConstraintType(self) -> types.StiffnessCriteriaType:
		result = self._Entity.ConstraintType
		return types.StiffnessCriteriaType[result.ToString()] if result is not None else None

	@property
	def Set(self) -> str:
		return self._Entity.Set

	@property
	def DesignLoadCases(self) -> list[str]:
		return [string for string in self._Entity.DesignLoadCases]

	@Set.setter
	def Set(self, value: str) -> None:
		self._Entity.Set = value

	def AddDesignLoadCases(self, designLoadCases: tuple[str]) -> None:
		designLoadCasesList = List[str]()
		if designLoadCases is not None:
			for thing in designLoadCases:
				if thing is not None:
					designLoadCasesList.Add(thing)
		designLoadCasesEnumerable = IEnumerable(designLoadCasesList)
		return self._Entity.AddDesignLoadCases(designLoadCasesEnumerable)

	def RemoveDesignLoadCases(self, designLoadCases: tuple[str]) -> None:
		designLoadCasesList = List[str]()
		if designLoadCases is not None:
			for thing in designLoadCases:
				if thing is not None:
					designLoadCasesList.Add(thing)
		designLoadCasesEnumerable = IEnumerable(designLoadCasesList)
		return self._Entity.RemoveDesignLoadCases(designLoadCasesEnumerable)


class ModalAutomatedConstraint(AutomatedConstraint):
	def __init__(self, modalAutomatedConstraint: _api.ModalAutomatedConstraint):
		self._Entity = modalAutomatedConstraint

	@property
	def Eigenvalue(self) -> float:
		return self._Entity.Eigenvalue

	@Eigenvalue.setter
	def Eigenvalue(self, value: float) -> None:
		self._Entity.Eigenvalue = value


class BucklingAutomatedConstraint(ModalAutomatedConstraint):
	def __init__(self, bucklingAutomatedConstraint: _api.BucklingAutomatedConstraint):
		self._Entity = bucklingAutomatedConstraint


class StaticAutomatedConstraint(AutomatedConstraint):
	def __init__(self, staticAutomatedConstraint: _api.StaticAutomatedConstraint):
		self._Entity = staticAutomatedConstraint

	@property
	def VirtualDesignLoad(self) -> str:
		return self._Entity.VirtualDesignLoad

	@property
	def GridId(self) -> int:
		return self._Entity.GridId

	@property
	def Orientation(self) -> types.DisplacementShapeType:
		result = self._Entity.Orientation
		return types.DisplacementShapeType[result.ToString()] if result is not None else None

	@property
	def HasVector(self) -> bool:
		return self._Entity.HasVector

	@property
	def X(self) -> float:
		return self._Entity.X

	@property
	def Y(self) -> float:
		return self._Entity.Y

	@property
	def Z(self) -> float:
		return self._Entity.Z

	@VirtualDesignLoad.setter
	def VirtualDesignLoad(self, value: str) -> None:
		self._Entity.VirtualDesignLoad = value

	@GridId.setter
	def GridId(self, value: int) -> None:
		self._Entity.GridId = value

	@Orientation.setter
	def Orientation(self, value: types.DisplacementShapeType) -> None:
		self._Entity.Orientation = _types.DisplacementShapeType(value.value)

	@X.setter
	def X(self, value: float) -> None:
		self._Entity.X = value

	@Y.setter
	def Y(self, value: float) -> None:
		self._Entity.Y = value

	@Z.setter
	def Z(self, value: float) -> None:
		self._Entity.Z = value


class DisplacementAutomatedConstraint(StaticAutomatedConstraint):
	def __init__(self, displacementAutomatedConstraint: _api.DisplacementAutomatedConstraint):
		self._Entity = displacementAutomatedConstraint

	@property
	def Limit(self) -> float:
		return self._Entity.Limit

	@Limit.setter
	def Limit(self, value: float) -> None:
		self._Entity.Limit = value


class FrequencyAutomatedConstraint(ModalAutomatedConstraint):
	def __init__(self, frequencyAutomatedConstraint: _api.FrequencyAutomatedConstraint):
		self._Entity = frequencyAutomatedConstraint


class RotationAutomatedConstraint(StaticAutomatedConstraint):
	def __init__(self, rotationAutomatedConstraint: _api.RotationAutomatedConstraint):
		self._Entity = rotationAutomatedConstraint

	@property
	def Limit(self) -> float:
		return self._Entity.Limit

	@Limit.setter
	def Limit(self, value: float) -> None:
		self._Entity.Limit = value


class ManualConstraint(IdNameEntityRenameable):
	def __init__(self, manualConstraint: _api.ManualConstraint):
		self._Entity = manualConstraint

	@property
	def ConstraintType(self) -> types.ConstraintType:
		result = self._Entity.ConstraintType
		return types.ConstraintType[result.ToString()] if result is not None else None

	@property
	def Set(self) -> str:
		return self._Entity.Set

	@property
	def Limit(self) -> float:
		return self._Entity.Limit

	@property
	def A11(self) -> bool:
		return self._Entity.A11

	@property
	def A22(self) -> bool:
		return self._Entity.A22

	@property
	def A33(self) -> bool:
		return self._Entity.A33

	@property
	def D11(self) -> bool:
		return self._Entity.D11

	@property
	def D22(self) -> bool:
		return self._Entity.D22

	@property
	def D33(self) -> bool:
		return self._Entity.D33

	@property
	def EA(self) -> bool:
		return self._Entity.EA

	@property
	def EI1(self) -> bool:
		return self._Entity.EI1

	@property
	def EI2(self) -> bool:
		return self._Entity.EI2

	@property
	def GJ(self) -> bool:
		return self._Entity.GJ

	@property
	def IsActive(self) -> bool:
		return self._Entity.IsActive

	@Set.setter
	def Set(self, value: str) -> None:
		self._Entity.Set = value

	@Limit.setter
	def Limit(self, value: float) -> None:
		self._Entity.Limit = value

	@A11.setter
	def A11(self, value: bool) -> None:
		self._Entity.A11 = value

	@A22.setter
	def A22(self, value: bool) -> None:
		self._Entity.A22 = value

	@A33.setter
	def A33(self, value: bool) -> None:
		self._Entity.A33 = value

	@D11.setter
	def D11(self, value: bool) -> None:
		self._Entity.D11 = value

	@D22.setter
	def D22(self, value: bool) -> None:
		self._Entity.D22 = value

	@D33.setter
	def D33(self, value: bool) -> None:
		self._Entity.D33 = value

	@EA.setter
	def EA(self, value: bool) -> None:
		self._Entity.EA = value

	@EI1.setter
	def EI1(self, value: bool) -> None:
		self._Entity.EI1 = value

	@EI2.setter
	def EI2(self, value: bool) -> None:
		self._Entity.EI2 = value

	@GJ.setter
	def GJ(self, value: bool) -> None:
		self._Entity.GJ = value

	@IsActive.setter
	def IsActive(self, value: bool) -> None:
		self._Entity.IsActive = value


class ManualConstraintWithDesignLoad(ManualConstraint):
	def __init__(self, manualConstraintWithDesignLoad: _api.ManualConstraintWithDesignLoad):
		self._Entity = manualConstraintWithDesignLoad

	@property
	def UseAllDesignLoads(self) -> bool:
		return self._Entity.UseAllDesignLoads

	@property
	def DesignLoadCase(self) -> str:
		return self._Entity.DesignLoadCase

	@UseAllDesignLoads.setter
	def UseAllDesignLoads(self, value: bool) -> None:
		self._Entity.UseAllDesignLoads = value

	@DesignLoadCase.setter
	def DesignLoadCase(self, value: str) -> None:
		self._Entity.DesignLoadCase = value


class BucklingManualConstraint(ManualConstraintWithDesignLoad):
	def __init__(self, bucklingManualConstraint: _api.BucklingManualConstraint):
		self._Entity = bucklingManualConstraint


class DisplacementManualConstraint(ManualConstraintWithDesignLoad):
	def __init__(self, displacementManualConstraint: _api.DisplacementManualConstraint):
		self._Entity = displacementManualConstraint

	@property
	def DOF(self) -> types.DegreeOfFreedom:
		result = self._Entity.DOF
		return types.DegreeOfFreedom[result.ToString()] if result is not None else None

	@property
	def Nodes(self) -> list[int]:
		return [int32 for int32 in self._Entity.Nodes]

	@property
	def RefNodes(self) -> list[int]:
		return [int32 for int32 in self._Entity.RefNodes]

	@DOF.setter
	def DOF(self, value: types.DegreeOfFreedom) -> None:
		self._Entity.DOF = _types.DegreeOfFreedom(value.value)

	def AddNodes(self, ids: tuple[int]) -> None:
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.AddNodes(idsEnumerable)

	def RemoveNodes(self, ids: tuple[int]) -> None:
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.RemoveNodes(idsEnumerable)

	def AddRefNodes(self, ids: tuple[int]) -> None:
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.AddRefNodes(idsEnumerable)

	def RemoveRefNodes(self, ids: tuple[int]) -> None:
		idsList = MakeCSharpIntList(ids)
		idsEnumerable = IEnumerable(idsList)
		return self._Entity.RemoveRefNodes(idsEnumerable)


class FrequencyManualConstraint(ManualConstraintWithDesignLoad):
	def __init__(self, frequencyManualConstraint: _api.FrequencyManualConstraint):
		self._Entity = frequencyManualConstraint


class StaticMomentManualConstraint(ManualConstraint):
	def __init__(self, staticMomentManualConstraint: _api.StaticMomentManualConstraint):
		self._Entity = staticMomentManualConstraint


class AutomatedConstraintCol(IdNameEntityCol[AutomatedConstraint]):
	def __init__(self, automatedConstraintCol: _api.AutomatedConstraintCol):
		self._Entity = automatedConstraintCol
		self._CollectedClass = AutomatedConstraint

	@property
	def AutomatedConstraintColList(self) -> tuple[AutomatedConstraint]:
		return tuple([AutomatedConstraint(automatedConstraintCol) for automatedConstraintCol in self._Entity])

	def AddBucklingConstraint(self, designLoads: tuple[str], eigenvalue: float, name: str = None) -> BucklingAutomatedConstraint:
		designLoadsList = List[str]()
		if designLoads is not None:
			for thing in designLoads:
				if thing is not None:
					designLoadsList.Add(thing)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return BucklingAutomatedConstraint(self._Entity.AddBucklingConstraint(designLoadsEnumerable, eigenvalue, name))

	def AddFrequencyConstraint(self, designLoads: tuple[str], eigenvalue: float, name: str = None) -> FrequencyAutomatedConstraint:
		designLoadsList = List[str]()
		if designLoads is not None:
			for thing in designLoads:
				if thing is not None:
					designLoadsList.Add(thing)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return FrequencyAutomatedConstraint(self._Entity.AddFrequencyConstraint(designLoadsEnumerable, eigenvalue, name))

	def AddDisplacementConstraint(self, designLoads: tuple[str], gridId: int, limit: float, name: str = None) -> DisplacementAutomatedConstraint:
		designLoadsList = List[str]()
		if designLoads is not None:
			for thing in designLoads:
				if thing is not None:
					designLoadsList.Add(thing)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return DisplacementAutomatedConstraint(self._Entity.AddDisplacementConstraint(designLoadsEnumerable, gridId, limit, name))

	def AddRotationConstraint(self, designLoads: tuple[str], gridId: int, limit: float, name: str = None) -> RotationAutomatedConstraint:
		designLoadsList = List[str]()
		if designLoads is not None:
			for thing in designLoads:
				if thing is not None:
					designLoadsList.Add(thing)
		designLoadsEnumerable = IEnumerable(designLoadsList)
		return RotationAutomatedConstraint(self._Entity.AddRotationConstraint(designLoadsEnumerable, gridId, limit, name))

	@overload
	def Delete(self, id: int) -> bool: ...

	@overload
	def Delete(self, name: str) -> bool: ...

	@overload
	def GetBuckling(self, id: int) -> BucklingAutomatedConstraint: ...

	@overload
	def GetBuckling(self, name: str) -> BucklingAutomatedConstraint: ...

	@overload
	def GetFrequency(self, id: int) -> FrequencyAutomatedConstraint: ...

	@overload
	def GetFrequency(self, name: str) -> FrequencyAutomatedConstraint: ...

	@overload
	def GetRotation(self, id: int) -> RotationAutomatedConstraint: ...

	@overload
	def GetRotation(self, name: str) -> RotationAutomatedConstraint: ...

	@overload
	def GetDisplacement(self, id: int) -> DisplacementAutomatedConstraint: ...

	@overload
	def GetDisplacement(self, name: str) -> DisplacementAutomatedConstraint: ...

	@overload
	def Get(self, name: str) -> AutomatedConstraint: ...

	@overload
	def Get(self, id: int) -> AutomatedConstraint: ...

	def Delete(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return self._Entity.Delete(item1)

		if isinstance(item1, str):
			return self._Entity.Delete(item1)

		return self._Entity.Delete(item1)

	def GetBuckling(self, item1 = None) -> BucklingAutomatedConstraint:
		if isinstance(item1, int):
			return BucklingAutomatedConstraint(self._Entity.GetBuckling(item1))

		if isinstance(item1, str):
			return BucklingAutomatedConstraint(self._Entity.GetBuckling(item1))

		return BucklingAutomatedConstraint(self._Entity.GetBuckling(item1))

	def GetFrequency(self, item1 = None) -> FrequencyAutomatedConstraint:
		if isinstance(item1, int):
			return FrequencyAutomatedConstraint(self._Entity.GetFrequency(item1))

		if isinstance(item1, str):
			return FrequencyAutomatedConstraint(self._Entity.GetFrequency(item1))

		return FrequencyAutomatedConstraint(self._Entity.GetFrequency(item1))

	def GetRotation(self, item1 = None) -> RotationAutomatedConstraint:
		if isinstance(item1, int):
			return RotationAutomatedConstraint(self._Entity.GetRotation(item1))

		if isinstance(item1, str):
			return RotationAutomatedConstraint(self._Entity.GetRotation(item1))

		return RotationAutomatedConstraint(self._Entity.GetRotation(item1))

	def GetDisplacement(self, item1 = None) -> DisplacementAutomatedConstraint:
		if isinstance(item1, int):
			return DisplacementAutomatedConstraint(self._Entity.GetDisplacement(item1))

		if isinstance(item1, str):
			return DisplacementAutomatedConstraint(self._Entity.GetDisplacement(item1))

		return DisplacementAutomatedConstraint(self._Entity.GetDisplacement(item1))

	def Get(self, item1 = None) -> AutomatedConstraint:
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = AutomatedConstraint
			for subclass in AutomatedConstraint.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = AutomatedConstraint
			for subclass in AutomatedConstraint.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = AutomatedConstraint
		for subclass in AutomatedConstraint.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def __getitem__(self, index: int):
		return self.AutomatedConstraintColList[index]

	def __iter__(self):
		yield from self.AutomatedConstraintColList

	def __len__(self):
		return len(self.AutomatedConstraintColList)


class ManualConstraintCol(IdNameEntityCol[ManualConstraint]):
	def __init__(self, manualConstraintCol: _api.ManualConstraintCol):
		self._Entity = manualConstraintCol
		self._CollectedClass = ManualConstraint

	@property
	def ManualConstraintColList(self) -> tuple[ManualConstraint]:
		return tuple([ManualConstraint(manualConstraintCol) for manualConstraintCol in self._Entity])

	@overload
	def GetFrequency(self, id: int) -> FrequencyManualConstraint: ...

	@overload
	def GetFrequency(self, name: str) -> FrequencyManualConstraint: ...

	@overload
	def GetBuckling(self, id: int) -> BucklingManualConstraint: ...

	@overload
	def GetBuckling(self, name: str) -> BucklingManualConstraint: ...

	@overload
	def GetDisplacement(self, id: int) -> DisplacementManualConstraint: ...

	@overload
	def GetDisplacement(self, name: str) -> DisplacementManualConstraint: ...

	@overload
	def GetStaticMoment(self, id: int) -> StaticMomentManualConstraint: ...

	@overload
	def GetStaticMoment(self, name: str) -> StaticMomentManualConstraint: ...

	def AddFrequencyConstraint(self, setName: str, limit: float, name: str = None) -> FrequencyManualConstraint:
		'''
		Add a Manual Constraint of type Frequency.
		'''
		return FrequencyManualConstraint(self._Entity.AddFrequencyConstraint(setName, limit, name))

	def AddBucklingConstraint(self, setName: str, limit: float, name: str = None) -> BucklingManualConstraint:
		'''
		Add a Manual Constraint of type Buckling.
		'''
		return BucklingManualConstraint(self._Entity.AddBucklingConstraint(setName, limit, name))

	def AddStaticMomentManualConstraint(self, setName: str, limit: float, name: str = None) -> StaticMomentManualConstraint:
		'''
		Add a Manual Constraint of type Static Moment.
		'''
		return StaticMomentManualConstraint(self._Entity.AddStaticMomentManualConstraint(setName, limit, name))

	def AddDisplacementConstraint(self, setName: str, gridIds: list[int], limit: float, name: str = None) -> DisplacementManualConstraint:
		gridIdsList = MakeCSharpIntList(gridIds)
		return DisplacementManualConstraint(self._Entity.AddDisplacementConstraint(setName, gridIdsList, limit, name))

	@overload
	def DeleteConstraint(self, name: str) -> bool: ...

	@overload
	def DeleteConstraint(self, id: int) -> bool: ...

	@overload
	def Get(self, name: str) -> ManualConstraint: ...

	@overload
	def Get(self, id: int) -> ManualConstraint: ...

	def GetFrequency(self, item1 = None) -> FrequencyManualConstraint:
		if isinstance(item1, int):
			return FrequencyManualConstraint(self._Entity.GetFrequency(item1))

		if isinstance(item1, str):
			return FrequencyManualConstraint(self._Entity.GetFrequency(item1))

		return FrequencyManualConstraint(self._Entity.GetFrequency(item1))

	def GetBuckling(self, item1 = None) -> BucklingManualConstraint:
		if isinstance(item1, int):
			return BucklingManualConstraint(self._Entity.GetBuckling(item1))

		if isinstance(item1, str):
			return BucklingManualConstraint(self._Entity.GetBuckling(item1))

		return BucklingManualConstraint(self._Entity.GetBuckling(item1))

	def GetDisplacement(self, item1 = None) -> DisplacementManualConstraint:
		if isinstance(item1, int):
			return DisplacementManualConstraint(self._Entity.GetDisplacement(item1))

		if isinstance(item1, str):
			return DisplacementManualConstraint(self._Entity.GetDisplacement(item1))

		return DisplacementManualConstraint(self._Entity.GetDisplacement(item1))

	def GetStaticMoment(self, item1 = None) -> StaticMomentManualConstraint:
		if isinstance(item1, int):
			return StaticMomentManualConstraint(self._Entity.GetStaticMoment(item1))

		if isinstance(item1, str):
			return StaticMomentManualConstraint(self._Entity.GetStaticMoment(item1))

		return StaticMomentManualConstraint(self._Entity.GetStaticMoment(item1))

	def DeleteConstraint(self, item1 = None) -> bool:
		if isinstance(item1, str):
			return self._Entity.DeleteConstraint(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteConstraint(item1)

		return self._Entity.DeleteConstraint(item1)

	def Get(self, item1 = None) -> ManualConstraint:
		if isinstance(item1, str):
			return ManualConstraint(super().Get(item1))

		if isinstance(item1, int):
			return ManualConstraint(super().Get(item1))

		return ManualConstraint(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.ManualConstraintColList[index]

	def __iter__(self):
		yield from self.ManualConstraintColList

	def __len__(self):
		return len(self.ManualConstraintColList)


class HyperFea:
	def __init__(self, hyperFea: _api.HyperFea):
		self._Entity = hyperFea

	@property
	def ManualConstraints(self) -> ManualConstraintCol:
		result = self._Entity.ManualConstraints
		return ManualConstraintCol(result) if result is not None else None

	@property
	def AutomatedConstraints(self) -> AutomatedConstraintCol:
		result = self._Entity.AutomatedConstraints
		return AutomatedConstraintCol(result) if result is not None else None

	def RunIterations(self, numberOfIterations: int, startWithSizing: bool) -> None:
		'''
		Run HyperFEA.
		'''
		return self._Entity.RunIterations(numberOfIterations, startWithSizing)

	def SetupSolver(self, solverPath: str, arguments: str) -> types.SimpleStatus:
		'''
		Setup FEA solver.
		'''
		return types.SimpleStatus(self._Entity.SetupSolver(solverPath, arguments))

	def TestSolver(self) -> types.SimpleStatus:
		'''
		Test FEA solver setup.
		'''
		return types.SimpleStatus(self._Entity.TestSolver())

	def GetSolverSetup(self) -> types.HyperFeaSolver:
		'''
		Get the current FEA solver setup.
		'''
		return types.HyperFeaSolver(self._Entity.GetSolverSetup())


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
	def Id(self) -> int:
		return self._Entity.Id

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

	def AddTemperatureProperty(self, temperature: float, et: float, ec: float, g: float, ftu: float, fcu: float, fsu: float, ef: float = None, ffu: float = None, k: float = None, c: float = None) -> FoamTemperature:
		return FoamTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, g, ftu, fcu, fsu, ef, ffu, k, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> FoamTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		:param LookupTemperature: Temperature to search for.
		'''
		return FoamTemperature(self._Entity.GetTemperature(lookupTemperature))

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
	def Id(self) -> int:
		return self._Entity.Id

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

	def AddTemperatureProperty(self, temperature: float, et: float, ec: float, gw: float, gl: float, ftu: float, fcus: float, fcub: float, fcuc: float, fsuw: float, fsul: float, sScfl: float = None, sScfh: float = None, k1: float = None, k2: float = None, k3: float = None, c: float = None) -> HoneycombTemperature:
		return HoneycombTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, gw, gl, ftu, fcus, fcub, fcuc, fsuw, fsul, sScfl, sScfh, k1, k2, k3, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> HoneycombTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		:param LookupTemperature: Temperature to search for.
		'''
		return HoneycombTemperature(self._Entity.GetTemperature(lookupTemperature))

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
	def Id(self) -> int:
		return self._Entity.Id

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

	def AddTemperatureProperty(self, temperature: float, et: float, ec: float, g: float, ftuL: float, ftyL: float, fcyL: float, ftuLT: float, ftyLT: float, fcyLT: float, fsu: float, alpha: float, n: float = None, f02: float = None, k: float = None, c: float = None, fbru15: float = None, fbry15: float = None, fbru20: float = None, fbry20: float = None, etyL: float = None, ecyL: float = None, etyLT: float = None, ecyLT: float = None, esu: float = None, fpadh: float = None, fsadh: float = None, esadh: float = None, cd: float = None, ffwt: float = None, ffxz: float = None, ffyz: float = None, ftFatigue: float = None, fcFatigue: float = None) -> IsotropicTemperature:
		return IsotropicTemperature(self._Entity.AddTemperatureProperty(temperature, et, ec, g, ftuL, ftyL, fcyL, ftuLT, ftyLT, fcyLT, fsu, alpha, n, f02, k, c, fbru15, fbry15, fbru20, fbry20, etyL, ecyL, etyLT, ecyLT, esu, fpadh, fsadh, esadh, cd, ffwt, ffxz, ffyz, ftFatigue, fcFatigue))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> IsotropicTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		:param LookupTemperature: Temperature to search for.
		'''
		return IsotropicTemperature(self._Entity.GetTemperature(lookupTemperature))

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

	def Save(self) -> None:
		'''
		Save any changes to this isotropic material to the database.
		'''
		return self._Entity.Save()


class LaminateBase(ABC):
	def __init__(self, laminateBase: _api.LaminateBase):
		self._Entity = laminateBase

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def IsEditable(self) -> bool:
		return self._Entity.IsEditable

	@property
	def MaterialFamilyName(self) -> str:
		return self._Entity.MaterialFamilyName

	@property
	def LayerCount(self) -> int:
		return self._Entity.LayerCount

	@property
	def Density(self) -> float:
		return self._Entity.Density

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def LaminateFamilyId(self) -> int:
		return self._Entity.LaminateFamilyId

	@property
	def LaminateFamilyOrder(self) -> int:
		return self._Entity.LaminateFamilyOrder

	@property
	def HyperLaminate(self) -> bool:
		return self._Entity.HyperLaminate

	@abstractmethod
	def Save(self) -> None:
		'''
		Save the laminate.
		'''
		return self._Entity.Save()

	@Name.setter
	def Name(self, value: str) -> None:
		self._Entity.Name = value

	@MaterialFamilyName.setter
	def MaterialFamilyName(self, value: str) -> None:
		self._Entity.MaterialFamilyName = value


class LaminateFamily(IdNameEntity):
	def __init__(self, laminateFamily: _api.LaminateFamily):
		self._Entity = laminateFamily

	@property
	def Laminates(self) -> list[LaminateBase]:
		return [LaminateBase(laminateBase) for laminateBase in self._Entity.Laminates]

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate

	@property
	def PlankSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.PlankSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def PlankMinRatio(self) -> float:
		return self._Entity.PlankMinRatio

	@property
	def PlankMaxRatio(self) -> float:
		return self._Entity.PlankMaxRatio

	@property
	def FootChargeSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.FootChargeSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def FootChargeMinRatio(self) -> float:
		return self._Entity.FootChargeMinRatio

	@property
	def FootChargeMaxRatio(self) -> float:
		return self._Entity.FootChargeMaxRatio

	@property
	def WebChargeSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.WebChargeSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def WebChargeMinRatio(self) -> float:
		return self._Entity.WebChargeMinRatio

	@property
	def WebChargeMaxRatio(self) -> float:
		return self._Entity.WebChargeMaxRatio

	@property
	def CapChargeSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.CapChargeSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def CapChargeMinRatio(self) -> float:
		return self._Entity.CapChargeMinRatio

	@property
	def CapChargeMaxRatio(self) -> float:
		return self._Entity.CapChargeMaxRatio

	@property
	def CapCoverSetting(self) -> types.LaminateFamilySettingType:
		result = self._Entity.CapCoverSetting
		return types.LaminateFamilySettingType[result.ToString()] if result is not None else None

	@property
	def CapCoverMinRatio(self) -> float:
		return self._Entity.CapCoverMinRatio

	@property
	def CapCoverMaxRatio(self) -> float:
		return self._Entity.CapCoverMaxRatio

	@property
	def DropPattern(self) -> types.PlyDropPattern:
		result = self._Entity.DropPattern
		return types.PlyDropPattern[result.ToString()] if result is not None else None

	@property
	def LaminateStiffenerProfile(self) -> types.StiffenerProfile:
		result = self._Entity.LaminateStiffenerProfile
		return types.StiffenerProfile[result.ToString()] if result is not None else None


class LaminateLayerBase(ABC):
	def __init__(self, laminateLayerBase: _api.LaminateLayerBase):
		self._Entity = laminateLayerBase

	@property
	def LayerId(self) -> int:
		return self._Entity.LayerId

	@property
	def LayerMaterial(self) -> str:
		return self._Entity.LayerMaterial

	@property
	def LayerMaterialType(self) -> types.MaterialType:
		'''
		Represents a material's type.
		'''
		result = self._Entity.LayerMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	def SetThickness(self, thickness: float) -> None:
		'''
		Set the thickness of a layer.
		'''
		return self._Entity.SetThickness(thickness)

	@overload
	def SetMaterial(self, matId: int) -> bool: ...

	@overload
	def SetMaterial(self, matName: str) -> bool: ...

	@Angle.setter
	@abstractmethod
	def Angle(self, value: float) -> None:
		self._Entity.Angle = value

	def SetMaterial(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return self._Entity.SetMaterial(item1)

		if isinstance(item1, str):
			return self._Entity.SetMaterial(item1)

		return self._Entity.SetMaterial(item1)


class LaminateLayer(LaminateLayerBase):
	'''
	Layer in a non-stiffener laminate.
	'''
	def __init__(self, laminateLayer: _api.LaminateLayer):
		self._Entity = laminateLayer

	@property
	def LayerId(self) -> int:
		return self._Entity.LayerId

	@property
	def LayerMaterialType(self) -> types.MaterialType:
		'''
		Represents a material's type.
		'''
		result = self._Entity.LayerMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	@Angle.setter
	def Angle(self, value: float) -> None:
		self._Entity.Angle = value

	@overload
	def SetMaterial(self, matId: int) -> bool: ...

	@overload
	def SetMaterial(self, matName: str) -> bool: ...

	def SetMaterial(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return bool(super().SetMaterial(item1))

		if isinstance(item1, str):
			return bool(super().SetMaterial(item1))

		return self._Entity.SetMaterial(item1)


class Laminate(LaminateBase):
	'''
	Laminate
	'''
	def __init__(self, laminate: _api.Laminate):
		self._Entity = laminate

	@property
	def Layers(self) -> list[LaminateLayer]:
		return [LaminateLayer(laminateLayer) for laminateLayer in self._Entity.Layers]

	def AddLayer(self, materialName: str, angle: float, thickness: float = None) -> LaminateLayer:
		return LaminateLayer(self._Entity.AddLayer(materialName, angle, thickness))

	def InsertLayer(self, layerId: int, materialName: str, angle: float, thickness: float = None) -> LaminateLayer:
		return LaminateLayer(self._Entity.InsertLayer(layerId, materialName, angle, thickness))

	def RemoveLayer(self, layerId: int) -> bool:
		'''
		Removes a layer from the laminate.
		'''
		return self._Entity.RemoveLayer(layerId)

	def Save(self) -> None:
		'''
		Save any changes to this laminate material to the database.
		'''
		return self._Entity.Save()


class StiffenerLaminateLayer(LaminateLayerBase):
	'''
	Stiffener Laminate Layer
	'''
	def __init__(self, stiffenerLaminateLayer: _api.StiffenerLaminateLayer):
		self._Entity = stiffenerLaminateLayer

	@property
	def LayerLocations(self) -> list[types.StiffenerLaminateLayerLocation]:
		return [types.StiffenerLaminateLayerLocation[stiffenerLaminateLayerLocation.ToString()] for stiffenerLaminateLayerLocation in self._Entity.LayerLocations]

	@property
	def LayerId(self) -> int:
		return self._Entity.LayerId

	@property
	def LayerMaterialType(self) -> types.MaterialType:
		'''
		Represents a material's type.
		'''
		result = self._Entity.LayerMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	def AddLayerLocation(self, location: types.StiffenerLaminateLayerLocation) -> None:
		'''
		Add a layer location to this layer.
		'''
		return self._Entity.AddLayerLocation(_types.StiffenerLaminateLayerLocation(location.value))

	def RemoveLayerLocation(self, location: types.StiffenerLaminateLayerLocation) -> bool:
		'''
		Remove a layer location from LayerLocations.
		'''
		return self._Entity.RemoveLayerLocation(_types.StiffenerLaminateLayerLocation(location.value))

	@Angle.setter
	def Angle(self, value: float) -> None:
		self._Entity.Angle = value

	@overload
	def SetMaterial(self, matId: int) -> bool: ...

	@overload
	def SetMaterial(self, matName: str) -> bool: ...

	def SetMaterial(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return bool(super().SetMaterial(item1))

		if isinstance(item1, str):
			return bool(super().SetMaterial(item1))

		return self._Entity.SetMaterial(item1)


class StiffenerLaminate(LaminateBase):
	'''
	Stiffener Laminate
	'''
	def __init__(self, stiffenerLaminate: _api.StiffenerLaminate):
		self._Entity = stiffenerLaminate

	@property
	def Layers(self) -> list[StiffenerLaminateLayer]:
		return [StiffenerLaminateLayer(stiffenerLaminateLayer) for stiffenerLaminateLayer in self._Entity.Layers]

	@property
	def LaminateStiffenerProfile(self) -> types.StiffenerProfile:
		result = self._Entity.LaminateStiffenerProfile
		return types.StiffenerProfile[result.ToString()] if result is not None else None

	@overload
	def AddLayer(self, location: types.StiffenerLaminateLayerLocation, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer: ...

	@overload
	def InsertLayer(self, location: types.StiffenerLaminateLayerLocation, layerId: int, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer: ...

	@overload
	def AddLayer(self, locations: tuple[types.StiffenerLaminateLayerLocation], materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer: ...

	@overload
	def InsertLayer(self, locations: tuple[types.StiffenerLaminateLayerLocation], layerId: int, materialName: str, angle: float, thickness: float = None) -> StiffenerLaminateLayer: ...

	def RemoveLayer(self, layerId: int) -> bool:
		'''
		Remove a layer by layerId.
            Note, layerId is 1 indexed.
		'''
		return self._Entity.RemoveLayer(layerId)

	def Save(self) -> None:
		'''
		Save laminate to database.
		'''
		return self._Entity.Save()

	def AddLayer(self, item1 = None, item2 = None, item3 = None, item4 = None) -> StiffenerLaminateLayer:
		if isinstance(item1, types.StiffenerLaminateLayerLocation) and isinstance(item2, str) and isinstance(item3, float) and (isinstance(item3, float) or isinstance(item3, int)) and isinstance(item4, float) and (isinstance(item4, float) or item4 is None or isinstance(item4, int)):
			return StiffenerLaminateLayer(self._Entity.AddLayer(_types.StiffenerLaminateLayerLocation(item1.value), item2, item3, item4))

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], types.StiffenerLaminateLayerLocation) and isinstance(item2, str) and isinstance(item3, float) and (isinstance(item3, float) or isinstance(item3, int)) and isinstance(item4, float) and (isinstance(item4, float) or item4 is None or isinstance(item4, int)):
			locationsList = List[_types.StiffenerLaminateLayerLocation]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						locationsList.Add(_types.StiffenerLaminateLayerLocation(thing.value))
			locationsEnumerable = IEnumerable(locationsList)
			return StiffenerLaminateLayer(self._Entity.AddLayer(locationsEnumerable, item2, item3, item4))

		return StiffenerLaminateLayer(self._Entity.AddLayer(_types.StiffenerLaminateLayerLocation(item1.value), item2, item3, item4))

	def InsertLayer(self, item1 = None, item2 = None, item3 = None, item4 = None, item5 = None) -> StiffenerLaminateLayer:
		if isinstance(item1, types.StiffenerLaminateLayerLocation) and isinstance(item2, int) and isinstance(item3, str) and isinstance(item4, float) and (isinstance(item4, float) or isinstance(item4, int)) and isinstance(item5, float) and (isinstance(item5, float) or item5 is None or isinstance(item5, int)):
			return StiffenerLaminateLayer(self._Entity.InsertLayer(_types.StiffenerLaminateLayerLocation(item1.value), item2, item3, item4, item5))

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], types.StiffenerLaminateLayerLocation) and isinstance(item2, int) and isinstance(item3, str) and isinstance(item4, float) and (isinstance(item4, float) or isinstance(item4, int)) and isinstance(item5, float) and (isinstance(item5, float) or item5 is None or isinstance(item5, int)):
			locationsList = List[_types.StiffenerLaminateLayerLocation]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						locationsList.Add(_types.StiffenerLaminateLayerLocation(thing.value))
			locationsEnumerable = IEnumerable(locationsList)
			return StiffenerLaminateLayer(self._Entity.InsertLayer(locationsEnumerable, item2, item3, item4, item5))

		return StiffenerLaminateLayer(self._Entity.InsertLayer(_types.StiffenerLaminateLayerLocation(item1.value), item2, item3, item4, item5))


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
		result = self._Entity.CorrectionId
		return types.CorrectionId[result.ToString()] if result is not None else None

	@property
	def PropertyId(self) -> types.CorrectionProperty:
		'''
		Property name for a correction factor. (Rows in HyperX)
		'''
		result = self._Entity.PropertyId
		return types.CorrectionProperty[result.ToString()] if result is not None else None


class OrthotropicCorrectionFactorPoint:
	'''
	Pointer to an Equation-based or Tabular Correction Factor.
	'''
	def __init__(self, orthotropicCorrectionFactorPoint: _api.OrthotropicCorrectionFactorPoint):
		self._Entity = orthotropicCorrectionFactorPoint

	def Create_OrthotropicCorrectionFactorPoint(property: types.CorrectionProperty, id: types.CorrectionId):
		return OrthotropicCorrectionFactorPoint(_api.OrthotropicCorrectionFactorPoint(_types.CorrectionProperty(property.value), _types.CorrectionId(id.value)))

	@property
	def CorrectionProperty(self) -> types.CorrectionProperty:
		'''
		Property name for a correction factor. (Rows in HyperX)
		'''
		result = self._Entity.CorrectionProperty
		return types.CorrectionProperty[result.ToString()] if result is not None else None

	@property
	def CorrectionId(self) -> types.CorrectionId:
		'''
		Correction ID for a correction factor. (Columns in HyperX)
		'''
		result = self._Entity.CorrectionId
		return types.CorrectionId[result.ToString()] if result is not None else None

	@overload
	def Equals(self, other) -> bool: ...

	@overload
	def Equals(self, obj: object) -> bool: ...

	def Equals(self, item1 = None) -> bool:
		if isinstance(item1, OrthotropicCorrectionFactorPoint):
			return self._Entity.Equals(item1._Entity)

		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		return self._Entity.Equals(item1._Entity)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class OrthotropicCorrectionFactorValue:
	'''
	Orthotropic material equation-based correction factor value. (NOT TABULAR)
	'''
	def __init__(self, orthotropicCorrectionFactorValue: _api.OrthotropicCorrectionFactorValue):
		self._Entity = orthotropicCorrectionFactorValue

	@property
	def Property(self) -> types.CorrectionProperty:
		'''
		Property name for a correction factor. (Rows in HyperX)
		'''
		result = self._Entity.Property
		return types.CorrectionProperty[result.ToString()] if result is not None else None

	@property
	def Correction(self) -> types.CorrectionId:
		'''
		Correction ID for a correction factor. (Columns in HyperX)
		'''
		result = self._Entity.Correction
		return types.CorrectionId[result.ToString()] if result is not None else None

	@property
	def Equation(self) -> types.CorrectionEquation:
		'''
		Equation for a correction factor.
		'''
		result = self._Entity.Equation
		return types.CorrectionEquation[result.ToString()] if result is not None else None

	@property
	def EquationParameter(self) -> types.EquationParameterId:
		'''
		Correction factor parameter names.
		'''
		result = self._Entity.EquationParameter
		return types.EquationParameterId[result.ToString()] if result is not None else None

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
		result = self._Entity.Equation
		return types.CorrectionEquation[result.ToString()] if result is not None else None

	@property
	def OrthotropicCorrectionValues(self) -> dict[types.EquationParameterId, OrthotropicCorrectionFactorValue]:
		orthotropicCorrectionValuesDict = {}
		for kvp in self._Entity.OrthotropicCorrectionValues:
			orthotropicCorrectionValuesDict[types.EquationParameterId[kvp.Key.ToString()]] = OrthotropicCorrectionFactorValue(kvp.Value)

		return orthotropicCorrectionValuesDict

	def AddCorrectionFactorValue(self, equationParameterName: types.EquationParameterId, valueToAdd: float) -> OrthotropicCorrectionFactorValue:
		'''
		Add a correction factor value for a given correction factor.
		:param equationParameterName: This represents the parameter of the equation that should be changed.
		:param valueToAdd: This is the value that will be assigned to the chosen parameter.
		'''
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
		result = self._Entity.ValueType
		return types.CorrectionValueType[result.ToString()] if result is not None else None


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
		independentValuesDict = {}
		for kvp in self._Entity.IndependentValues:
			independentValuesDict[types.CorrectionIndependentDefinition[kvp.Key.ToString()]] = TabularCorrectionFactorIndependentValue(kvp.Value)

		return independentValuesDict


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
		return {types.CorrectionIndependentDefinition[correctionIndependentDefinition.ToString()] for correctionIndependentDefinition in self._Entity.CorrectionIndependentDefinitions}

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: float) -> None: ...

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: bool) -> None: ...

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: int) -> None: ...

	def SetKValue(self, correctionPointId: int, value: float) -> None:
		'''
		Set the dependent value for a specified row.
		'''
		return self._Entity.SetKValue(correctionPointId, value)

	def SetIndependentValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, float) and (isinstance(item3, float) or isinstance(item3, int)):
			return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(item2.value), item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, bool):
			return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(item2.value), item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, int):
			return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(item2.value), item3)

		return self._Entity.SetIndependentValue(item1, _types.CorrectionIndependentDefinition(item2.value), item3)


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
		result = self._Entity.Property_ID
		return types.AllowablePropertyName[result.ToString()] if result is not None else None

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
		result = self._Entity.Property_ID
		return types.AllowablePropertyName[result.ToString()] if result is not None else None

	@property
	def Method_ID(self) -> types.AllowableMethodName:
		'''
		Method name for a laminate allowable.
		'''
		result = self._Entity.Method_ID
		return types.AllowableMethodName[result.ToString()] if result is not None else None

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

	def AddCurvePoint(self, property: types.AllowablePropertyName, x: float, y: float) -> OrthotropicAllowableCurvePoint:
		'''
		Add a curve point to a laminate allowable curve.
		:param x: x represents an x-value (for a non-polynomial method) or an allowable polynomial coefficient (represented by an enum).
		'''
		return OrthotropicAllowableCurvePoint(self._Entity.AddCurvePoint(_types.AllowablePropertyName(property.value), x, y))

	def DeleteCurvePoint(self, property: types.AllowablePropertyName, x: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		:param x: x represents an x-value (for a non-polynomial method) or an allowable polynomial coefficient (represented by an enum).
		'''
		return self._Entity.DeleteCurvePoint(_types.AllowablePropertyName(property.value), x)

	def GetCurvePoint(self, property: types.AllowablePropertyName, x: float) -> OrthotropicAllowableCurvePoint:
		'''
		Retrieve an allowable curve point from this temperature's allowable curve points.
		:param x: x represents an x-value (for a non-polynomial method) or an allowable polynomial coefficient (represented by an enum).
		'''
		return OrthotropicAllowableCurvePoint(self._Entity.GetCurvePoint(_types.AllowablePropertyName(property.value), x))

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
	def Id(self) -> int:
		return self._Entity.Id

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
		result = self._Entity.OrthotropicEffectiveLaminate
		return OrthotropicEffectiveLaminate(result) if result is not None else None

	@property
	def OrthotropicEquationCorrectionFactors(self) -> dict[OrthotropicCorrectionFactorPoint, OrthotropicEquationCorrectionFactor]:
		orthotropicEquationCorrectionFactorsDict = {}
		for kvp in self._Entity.OrthotropicEquationCorrectionFactors:
			orthotropicEquationCorrectionFactorsDict[OrthotropicCorrectionFactorPoint(kvp.Key)] = OrthotropicEquationCorrectionFactor(kvp.Value)

		return orthotropicEquationCorrectionFactorsDict

	@property
	def OrthotropicTabularCorrectionFactors(self) -> dict[OrthotropicCorrectionFactorPoint, OrthotropicTabularCorrectionFactor]:
		orthotropicTabularCorrectionFactorsDict = {}
		for kvp in self._Entity.OrthotropicTabularCorrectionFactors:
			orthotropicTabularCorrectionFactorsDict[OrthotropicCorrectionFactorPoint(kvp.Key)] = OrthotropicTabularCorrectionFactor(kvp.Value)

		return orthotropicTabularCorrectionFactorsDict

	def AddTemperatureProperty(self, temperature: float, et1: float, et2: float, vt12: float, ec1: float, ec2: float, vc12: float, g12: float, ftu1: float, ftu2: float, fcu1: float, fcu2: float, fsu12: float, alpha1: float, alpha2: float, etu1: float, etu2: float, ecu1: float, ecu2: float, esu12: float) -> OrthotropicTemperature:
		'''
		Adds a temperature-dependent property for a material.
		'''
		return OrthotropicTemperature(self._Entity.AddTemperatureProperty(temperature, et1, et2, vt12, ec1, ec2, vc12, g12, ftu1, ftu2, fcu1, fcu2, fsu12, alpha1, alpha2, etu1, etu2, ecu1, ecu2, esu12))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		'''
		Deletes a temperature-dependent property for a material.
		'''
		return self._Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> OrthotropicTemperature:
		'''
		Retrieve a Temperature from this material's temperature-dependent properties. Allows a degree of tolerance to avoid issues with floating point numbers.
		:param LookupTemperature: Temperature to search for.
		'''
		return OrthotropicTemperature(self._Entity.GetTemperature(lookupTemperature))

	def IsEffectiveLaminate(self) -> bool:
		'''
		Returns true if this material is an effective laminate.
		'''
		return self._Entity.IsEffectiveLaminate()

	def HasLaminateAllowable(self, property: types.AllowablePropertyName) -> bool:
		'''
		Returns true if this material has a specified laminate allowable property.
		'''
		return self._Entity.HasLaminateAllowable(_types.AllowablePropertyName(property.value))

	def AddLaminateAllowable(self, property: types.AllowablePropertyName, method: types.AllowableMethodName) -> OrthotropicLaminateAllowable:
		'''
		Adds a laminate allowable to this material.
            An orthotropic material can only have one laminate allowable of each property (as specified by the property argument).
		:param property: The strain or stress property for a laminate allowable.
		:param method: The method for a laminate allowable (AML, Percent 0/45, Polynomial).
		'''
		return OrthotropicLaminateAllowable(self._Entity.AddLaminateAllowable(_types.AllowablePropertyName(property.value), _types.AllowableMethodName(method.value)))

	def GetLaminateAllowable(self, lookupAllowableProperty: types.AllowablePropertyName) -> OrthotropicLaminateAllowable:
		'''
		Retrieve a Laminate allowable from this material's laminate allowables.
		:param LookupAllowableProperty: Laminate allowable property to search for.
		'''
		return OrthotropicLaminateAllowable(self._Entity.GetLaminateAllowable(_types.AllowablePropertyName(lookupAllowableProperty.value)))

	def AddEquationCorrectionFactor(self, propertyId: types.CorrectionProperty, correctionId: types.CorrectionId, equationId: types.CorrectionEquation) -> OrthotropicEquationCorrectionFactor:
		'''
		Adds an equation-based correction factor for this material.
		:param propertyId: The ID of the property to be affected by the correction factor. Specified with a CorrectionPropertyName enum.
		:param correctionId: The ID for the type of correction factor to be applied. Specified with a CorrectionIDName enum.
		:param equationId: The ID for the type of correction factor equation to use. Specified with a CorrectionEquationName enum.
		'''
		return OrthotropicEquationCorrectionFactor(self._Entity.AddEquationCorrectionFactor(_types.CorrectionProperty(propertyId.value), _types.CorrectionId(correctionId.value), _types.CorrectionEquation(equationId.value)))

	def GetEquationCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicEquationCorrectionFactor:
		'''
		Retrieve a Correction Factor from this material's correction factors.
		:param property: CorrectionPropertyName to search for.
		:param correction: CorrectionIDName to search for.
		'''
		return OrthotropicEquationCorrectionFactor(self._Entity.GetEquationCorrectionFactor(_types.CorrectionProperty(property.value), _types.CorrectionId(correction.value)))

	def GetTabularCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicTabularCorrectionFactor:
		'''
		Retrieve a Correction Factor from this material's correction factors.
		:param property: CorrectionPropertyName to search for.
		:param correction: CorrectionIDName to search for.
		'''
		return OrthotropicTabularCorrectionFactor(self._Entity.GetTabularCorrectionFactor(_types.CorrectionProperty(property.value), _types.CorrectionId(correction.value)))

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
	def Equals(self, obj: object) -> bool: ...

	def Equals(self, item1 = None) -> bool:
		if isinstance(item1, Vector2d):
			return self._Entity.Equals(item1._Entity)

		if isinstance(item1, object):
			return self._Entity.Equals(item1)

		return self._Entity.Equals(item1._Entity)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)

	def __hash__(self) -> int:
		return self._Entity.GetHashCode()


class ElementSet(IdNameEntity):
	'''
	A set of elements defined in the input file.
	'''
	def __init__(self, elementSet: _api.ElementSet):
		self._Entity = elementSet

	@property
	def Elements(self) -> ElementCol:
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None


class FemProperty(IdNameEntity):
	'''
	A property description.
	'''
	def __init__(self, femProperty: _api.FemProperty):
		self._Entity = femProperty

	@property
	def Elements(self) -> ElementCol:
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

	@property
	def FemType(self) -> types.FemType:
		result = self._Entity.FemType
		return types.FemType[result.ToString()] if result is not None else None


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
		result = self._Entity.FemProperties
		return FemPropertyCol(result) if result is not None else None

	@property
	def ElementSets(self) -> ElementSetCol:
		result = self._Entity.ElementSets
		return ElementSetCol(result) if result is not None else None


class PluginPackage(IdNameEntity):
	def __init__(self, pluginPackage: _api.PluginPackage):
		self._Entity = pluginPackage

	@property
	def FilePath(self) -> str:
		return self._Entity.FilePath

	@property
	def Version(self) -> str:
		return self._Entity.Version

	@property
	def Description(self) -> str:
		return self._Entity.Description

	@property
	def ModificationDate(self) -> DateTime:
		return self._Entity.ModificationDate


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
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

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
		'''
		The rundeck's input file path will point to the provided file path
		:param filepath: The path to the rundeck
		'''
		return RundeckUpdateStatus[self._Entity.SetInputFilePath(filepath).ToString()]

	def SetResultFilePath(self, filepath: str) -> RundeckUpdateStatus:
		'''
		The rundeck's result file path will point to the provided file path
		:param filepath: The path to the result file
		'''
		return RundeckUpdateStatus[self._Entity.SetResultFilePath(filepath).ToString()]


class RundeckPathPair:
	def __init__(self, rundeckPathPair: _api.RundeckPathPair):
		self._Entity = rundeckPathPair

	@property
	def InputFilePath(self) -> str:
		return self._Entity.InputFilePath

	@property
	def ResultFilePath(self) -> str:
		return self._Entity.ResultFilePath

	@InputFilePath.setter
	def InputFilePath(self, value: str) -> None:
		self._Entity.InputFilePath = value

	@ResultFilePath.setter
	def ResultFilePath(self, value: str) -> None:
		self._Entity.ResultFilePath = value


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
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def ReferencePoint(self) -> types.SectionCutPropertyLocation:
		'''
		Centroid vs Origin
		'''
		result = self._Entity.ReferencePoint
		return types.SectionCutPropertyLocation[result.ToString()] if result is not None else None

	@property
	def HorizontalVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		result = self._Entity.HorizontalVector
		return Vector3d(result) if result is not None else None

	@property
	def NormalVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		result = self._Entity.NormalVector
		return Vector3d(result) if result is not None else None

	@property
	def OriginVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		result = self._Entity.OriginVector
		return Vector3d(result) if result is not None else None

	@property
	def VerticalVector(self) -> Vector3d:
		'''
		Represents a readonly 3D vector.
		'''
		result = self._Entity.VerticalVector
		return Vector3d(result) if result is not None else None

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
		result = self._Entity.CG
		return Vector2d(result) if result is not None else None

	@property
	def CN(self) -> Vector2d:
		'''
		Represents a readonly 2D vector.
		'''
		result = self._Entity.CN
		return Vector2d(result) if result is not None else None

	@property
	def CQ(self) -> Vector2d:
		'''
		Represents a readonly 2D vector.
		'''
		result = self._Entity.CQ
		return Vector2d(result) if result is not None else None

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
		result = self._Entity.Elements
		return ElementCol(result) if result is not None else None

	@property
	def PlateElements(self) -> ElementCol:
		result = self._Entity.PlateElements
		return ElementCol(result) if result is not None else None

	@property
	def BeamElements(self) -> ElementCol:
		result = self._Entity.BeamElements
		return ElementCol(result) if result is not None else None

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

	@ReferencePoint.setter
	def ReferencePoint(self, value: types.SectionCutPropertyLocation) -> None:
		self._Entity.ReferencePoint = _types.SectionCutPropertyLocation(value.value)

	def SetHorizontalVector(self, vector: Vector3d) -> None:
		return self._Entity.SetHorizontalVector(vector._Entity)

	def SetNormalVector(self, vector: Vector3d) -> None:
		return self._Entity.SetNormalVector(vector._Entity)

	def SetOrigin(self, vector: Vector3d) -> None:
		return self._Entity.SetOrigin(vector._Entity)

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

	def GetBeamLoads(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> BeamLoads:
		return BeamLoads(self._Entity.GetBeamLoads(loadCaseId, _types.LoadSubCaseFactor(factor.value)))

	def InclinationAngle(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return float(self._Entity.InclinationAngle(loadCaseId, _types.LoadSubCaseFactor(factor.value)))

	def HorizontalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return float(self._Entity.HorizontalIntercept(loadCaseId, _types.LoadSubCaseFactor(factor.value)))

	def VerticalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return float(self._Entity.VerticalIntercept(loadCaseId, _types.LoadSubCaseFactor(factor.value)))

	def SetElements(self, elements: list[int]) -> bool:
		elementsList = MakeCSharpIntList(elements)
		return self._Entity.SetElements(elementsList)

	def SetElementsByIntersection(self) -> None:
		return self._Entity.SetElementsByIntersection()


class Set(ZoneJointContainer):
	def __init__(self, set: _api.Set):
		self._Entity = set

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

	@property
	def Zones(self) -> ZoneCol:
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus: ...

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
	def RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def AddZones(self, ids: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus: ...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddJoint(item1))

		return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddPanelSegment(item1))

		return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

	def AddZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Zone):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.AddZones(zonesEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			return CollectionModificationStatus(super().AddZones(item1))

		return CollectionModificationStatus[self._Entity.AddZones(item1).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Joint):
			return CollectionModificationStatus(super().RemoveJoints(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoints(item1).ToString()]

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegments(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegments(item1).ToString()]

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Zone):
			return CollectionModificationStatus(super().RemoveZones(item1))

		return CollectionModificationStatus[self._Entity.RemoveZones(item1).ToString()]

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		if isinstance(item1, Joint):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().AddZone(item1))

		return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().RemoveZone(item1))

		return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]


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
		'''
		This feature is in development and may not work as expected. Use at your own risk!
		'''
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

		return Ply(self._Entity.Get(item1))

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
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	@property
	def Plies(self) -> PlyCol:
		result = self._Entity.Plies
		return PlyCol(result) if result is not None else None

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

	@property
	def Zones(self) -> ZoneCol:
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	def ExportVCP(self, fileName: str) -> None:
		'''
		Export VCP with this structure's element centroids.
		'''
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
	def AddZones(self, zones: tuple[Zone]) -> CollectionModificationStatus: ...

	def CreateZone(self, elementIds: tuple[int], name: str = None) -> Zone:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		result = self._Entity.CreateZone(elementIdsEnumerable, name)
		thisClass = type(result).__name__
		givenClass = Zone
		for subclass in Zone.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def CreatePanelSegment(self, discreteTechnique: types.DiscreteTechnique, discreteElementLkp: dict[types.DiscreteDefinitionType, list[int]], name: str = None) -> PanelSegment:
		discreteElementLkpDict = Dictionary[_types.DiscreteDefinitionType, List[int]]()
		for kvp in discreteElementLkp:
			dictValue = discreteElementLkp[kvp]
			dictValueList = MakeCSharpIntList(dictValue)
			discreteElementLkpDict.Add(_types.DiscreteDefinitionType(kvp.value), dictValueList)
		return PanelSegment(self._Entity.CreatePanelSegment(_types.DiscreteTechnique(discreteTechnique.value), discreteElementLkpDict, name))

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
	def RemoveJoints(self, joints: tuple[Joint]) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def AddZones(self, ids: tuple[int]) -> CollectionModificationStatus: ...

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus: ...

	@overload
	def RemoveZones(self, zones: tuple[Zone]) -> CollectionModificationStatus: ...

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus: ...

	@overload
	def RemovePanelSegments(self, segments: tuple[PanelSegment]) -> CollectionModificationStatus: ...

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddJoint(item1))

		return CollectionModificationStatus[self._Entity.AddJoint(item1._Entity).ToString()]

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddPanelSegment(item1))

		return CollectionModificationStatus[self._Entity.AddPanelSegment(item1._Entity).ToString()]

	def AddZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Zone):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return CollectionModificationStatus[self._Entity.AddZones(zonesEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			return CollectionModificationStatus(super().AddZones(item1))

		return CollectionModificationStatus[self._Entity.AddZones(item1).ToString()]

	def Remove(self, item1 = None, item2 = None, item3 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int) and isinstance(item2, tuple) and item2 and isinstance(item2[0], int) and isinstance(item3, tuple) and item3 and isinstance(item3[0], int):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = MakeCSharpIntList(item2)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			panelSegmentIdsList = MakeCSharpIntList(item3)
			panelSegmentIdsEnumerable = IEnumerable(panelSegmentIdsList)
			return CollectionModificationStatus[self._Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable, panelSegmentIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int) and isinstance(item2, tuple) and item2 and isinstance(item2[0], int):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = MakeCSharpIntList(item2)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable).ToString()]

		return CollectionModificationStatus[self._Entity.Remove(item1, item2, item3).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			jointIdsList = MakeCSharpIntList(item1)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self._Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Joint):
			return CollectionModificationStatus(super().RemoveJoints(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoints(item1).ToString()]

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			segmentIdsList = MakeCSharpIntList(item1)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self._Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegments(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegments(item1).ToString()]

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self._Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], Zone):
			return CollectionModificationStatus(super().RemoveZones(item1))

		return CollectionModificationStatus[self._Entity.RemoveZones(item1).ToString()]

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		if isinstance(item1, Joint):
			return CollectionModificationStatus(super().RemoveJoint(item1))

		return CollectionModificationStatus[self._Entity.RemoveJoint(item1).ToString()]

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().AddZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().AddZone(item1))

		return CollectionModificationStatus[self._Entity.AddZone(item1).ToString()]

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemoveZone(item1))

		if isinstance(item1, Zone):
			return CollectionModificationStatus(super().RemoveZone(item1))

		return CollectionModificationStatus[self._Entity.RemoveZone(item1).ToString()]

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus(super().RemovePanelSegment(item1))

		return CollectionModificationStatus[self._Entity.RemovePanelSegment(item1).ToString()]


class AnalysisPropertyCol(IdNameEntityCol[AnalysisProperty]):
	def __init__(self, analysisPropertyCol: _api.AnalysisPropertyCol):
		self._Entity = analysisPropertyCol
		self._CollectedClass = AnalysisProperty

	@property
	def AnalysisPropertyColList(self) -> tuple[AnalysisProperty]:
		return tuple([AnalysisProperty(analysisPropertyCol) for analysisPropertyCol in self._Entity])

	def CreateAnalysisProperty(self, type: types.FamilyCategory, name: str = None) -> AnalysisProperty:
		'''
		Create an AnalysisProperty.
		'''
		return AnalysisProperty(self._Entity.CreateAnalysisProperty(_types.FamilyCategory(type.value), name))

	@overload
	def DeleteAnalysisProperty(self, name: str) -> bool: ...

	@overload
	def DeleteAnalysisProperty(self, id: int) -> bool: ...

	@overload
	def Get(self, name: str) -> AnalysisProperty: ...

	@overload
	def Get(self, id: int) -> AnalysisProperty: ...

	def DeleteAnalysisProperty(self, item1 = None) -> bool:
		if isinstance(item1, str):
			return self._Entity.DeleteAnalysisProperty(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteAnalysisProperty(item1)

		return self._Entity.DeleteAnalysisProperty(item1)

	def Get(self, item1 = None) -> AnalysisProperty:
		if isinstance(item1, str):
			return AnalysisProperty(super().Get(item1))

		if isinstance(item1, int):
			return AnalysisProperty(super().Get(item1))

		return AnalysisProperty(self._Entity.Get(item1))

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

	def CreateDesignProperty(self, familyConcept: types.FamilyConceptUID, materialMode: types.MaterialMode = types.MaterialMode.Any, name: str = None) -> DesignProperty:
		'''
		Create a DesignProperty.
		'''
		result = self._Entity.CreateDesignProperty(_types.FamilyConceptUID(familyConcept.value), _types.MaterialMode(materialMode.value), name)
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in DesignProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@overload
	def Get(self, name: str) -> DesignProperty: ...

	@overload
	def Get(self, id: int) -> DesignProperty: ...

	def Get(self, item1 = None) -> DesignProperty:
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = DesignProperty
			for subclass in DesignProperty.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = DesignProperty
			for subclass in DesignProperty.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = DesignProperty
		for subclass in DesignProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

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

	def CreateLoadProperty(self, loadPropertyType: types.LoadPropertyType, category: types.FamilyCategory, name: str = None) -> LoadProperty:
		'''
		Create a new load property.
		'''
		result = self._Entity.CreateLoadProperty(_types.LoadPropertyType(loadPropertyType.value), _types.FamilyCategory(category.value), name)
		thisClass = type(result).__name__
		givenClass = LoadProperty
		for subclass in LoadProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@overload
	def DeleteLoadProperty(self, id: int) -> bool: ...

	@overload
	def DeleteLoadProperty(self, name: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadProperty: ...

	@overload
	def Get(self, id: int) -> LoadProperty: ...

	def DeleteLoadProperty(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return self._Entity.DeleteLoadProperty(item1)

		if isinstance(item1, str):
			return self._Entity.DeleteLoadProperty(item1)

		return self._Entity.DeleteLoadProperty(item1)

	def Get(self, item1 = None) -> LoadProperty:
		if isinstance(item1, str):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = LoadProperty
			for subclass in LoadProperty.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		if isinstance(item1, int):
			result = super().Get(item1)
			thisClass = type(result).__name__
			givenClass = LoadProperty
			for subclass in LoadProperty.__subclasses__():
				if subclass.__name__ == thisClass:
					givenClass = subclass
			return givenClass(result) if result is not None else None

		result = self._Entity.Get(item1)
		thisClass = type(result).__name__
		givenClass = LoadProperty
		for subclass in LoadProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

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

		return DesignLoad(self._Entity.Get(item1))

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

	def Create(self, entityType: types.DiscreteFieldPhysicalEntityType, dataType: types.DiscreteFieldDataType, name: str = None) -> DiscreteField:
		'''
		Create a new DiscreteField.
		'''
		return DiscreteField(self._Entity.Create(_types.DiscreteFieldPhysicalEntityType(entityType.value), _types.DiscreteFieldDataType(dataType.value), name))

	def CreateFromVCP(self, filepath: str) -> list[DiscreteField]:
		'''
		Create a list of DiscreteFields from VCP.
		'''
		return [DiscreteField(discreteField) for discreteField in self._Entity.CreateFromVCP(filepath)]

	def Delete(self, id: int) -> CollectionModificationStatus:
		'''
		In the event of getting a CollectionModificationStatus.EntityMissingRemovalFailure,
            note that the discrete field is associated with a ply, and therefore cannot be deleted.
		'''
		return CollectionModificationStatus[self._Entity.Delete(id).ToString()]

	def CreateByPointMapToElements(self, elementIds: tuple[int], discreteFieldIds: tuple[int], suffix: str = None, tolerance: float = None) -> list[DiscreteField]:
		elementIdsList = MakeCSharpIntList(elementIds)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		discreteFieldIdsList = MakeCSharpIntList(discreteFieldIds)
		discreteFieldIdsEnumerable = IEnumerable(discreteFieldIdsList)
		return [DiscreteField(discreteField) for discreteField in self._Entity.CreateByPointMapToElements(elementIdsEnumerable, discreteFieldIdsEnumerable, suffix, tolerance)]

	@overload
	def Get(self, name: str) -> DiscreteField: ...

	@overload
	def Get(self, id: int) -> DiscreteField: ...

	def Get(self, item1 = None) -> DiscreteField:
		if isinstance(item1, str):
			return DiscreteField(super().Get(item1))

		if isinstance(item1, int):
			return DiscreteField(super().Get(item1))

		return DiscreteField(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.DiscreteFieldColList[index]

	def __iter__(self):
		yield from self.DiscreteFieldColList

	def __len__(self):
		return len(self.DiscreteFieldColList)


class FolderCol(IdNameEntityCol[Folder]):
	def __init__(self, folderCol: _api.FolderCol):
		self._Entity = folderCol
		self._CollectedClass = Folder

	@property
	def FolderColList(self) -> tuple[Folder]:
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = Folder
		for subclass in Folder.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(folderCol) for folderCol in self._Entity])

	@property
	def ParentFolder(self) -> Folder:
		result = self._Entity.ParentFolder
		return Folder(result) if result is not None else None

	def AddFolder(self, name: str) -> Folder:
		return Folder(self._Entity.AddFolder(name))

	def AddFolders(self, names: tuple[str]) -> tuple[Folder]:
		namesList = List[str]()
		if names is not None:
			for thing in names:
				if thing is not None:
					namesList.Add(thing)
		namesEnumerable = IEnumerable(namesList)
		result = self._Entity.AddFolders(namesEnumerable)
		thisClass = type(result).__name__
		givenClass = tuple[Folder]
		for subclass in tuple[Folder].__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def DeleteFolder(self, folder: Folder) -> bool:
		return self._Entity.DeleteFolder(folder._Entity)

	def DeleteFolders(self, folders: tuple[Folder]) -> bool:
		foldersList = List[_api.Folder]()
		if folders is not None:
			for thing in folders:
				if thing is not None:
					foldersList.Add(thing._Entity)
		foldersEnumerable = IEnumerable(foldersList)
		return self._Entity.DeleteFolders(foldersEnumerable)

	@overload
	def Get(self, name: str) -> Folder: ...

	@overload
	def Get(self, id: int) -> Folder: ...

	def Get(self, item1 = None) -> Folder:
		if isinstance(item1, str):
			return Folder(super().Get(item1))

		if isinstance(item1, int):
			return Folder(super().Get(item1))

		return Folder(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.FolderColList[index]

	def __iter__(self):
		yield from self.FolderColList

	def __len__(self):
		return len(self.FolderColList)


class ZoneJointContainerCol(IdNameEntityCol, Generic[T]):
	def __init__(self, zoneJointContainerCol: _api.ZoneJointContainerCol):
		self._Entity = zoneJointContainerCol
		self._CollectedClass = T

	@property
	def ZoneJointContainerColList(self) -> tuple[T]:
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = T
		for subclass in T.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(zoneJointContainerCol) for zoneJointContainerCol in self._Entity])

	@abstractmethod
	def Create(self, name: str) -> ZoneJointContainer:
		return self._Entity.Create(name)

	@overload
	def Get(self, name: str) -> ZoneJointContainer: ...

	@overload
	def Get(self, id: int) -> ZoneJointContainer: ...

	def Get(self, item1 = None) -> ZoneJointContainer:
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

	def AddRundeck(self, inputPath: str, resultPath: str = None) -> Rundeck:
		'''
		The specified rundeck at the given filepath will be added to the project's
            collection of rundecks
		:param inputPath: The path to the rundeck
		:param resultPath: The path to the rundeck's corresponding result file
		'''
		return Rundeck(self._Entity.AddRundeck(inputPath, resultPath))

	def ReassignPrimary(self, id: int) -> RundeckUpdateStatus:
		'''
		The specified rundeck will be updated to become the new primary rundeck.
		'''
		return RundeckUpdateStatus[self._Entity.ReassignPrimary(id).ToString()]

	def RemoveRundeck(self, id: int) -> RundeckRemoveStatus:
		'''
		The specified rundeck at the given filepath will be removed from the project's
            collection of rundecks
		:param id: The id of the rundeck to remove
		'''
		return RundeckRemoveStatus[self._Entity.RemoveRundeck(id).ToString()]

	def UpdateAllRundecks(self, newPaths: tuple[RundeckPathPair]) -> RundeckBulkUpdateStatus:
		newPathsList = List[_api.RundeckPathPair]()
		if newPaths is not None:
			for thing in newPaths:
				if thing is not None:
					newPathsList.Add(thing._Entity)
		newPathsEnumerable = IEnumerable(newPathsList)
		return RundeckBulkUpdateStatus[self._Entity.UpdateAllRundecks(newPathsEnumerable).ToString()]

	def GetRundeckPathSetters(self) -> list[RundeckPathPair]:
		'''
		Get RundeckPathSetters to be edited and input to UpdateAllRundecks.
		'''
		return [RundeckPathPair(rundeckPathPair) for rundeckPathPair in self._Entity.GetRundeckPathSetters()]

	def ReplaceStringInAllPaths(self, stringToReplace: str, newString: str) -> RundeckBulkUpdateStatus:
		'''
		Replace a given string with a new string in every rundeck path. This is useful when pointing to rundecks of the same name in a new directory.
		'''
		return RundeckBulkUpdateStatus[self._Entity.ReplaceStringInAllPaths(stringToReplace, newString).ToString()]

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

	@property
	def Folders(self) -> FolderCol:
		result = self._Entity.Folders
		return FolderCol(result) if result is not None else None

	def Create(self, origin: Vector3d, normal: Vector3d, horizontal: Vector3d, name: str = None) -> SectionCut:
		return SectionCut(self._Entity.Create(origin._Entity, normal._Entity, horizontal._Entity, name))

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

		return SectionCut(self._Entity.Get(item1))

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

	@property
	def Folders(self) -> FolderCol:
		result = self._Entity.Folders
		return FolderCol(result) if result is not None else None

	def Create(self, name: str = None) -> Set:
		'''
		Attempt to create a new Set.
		:param name: The name of the set to be created.
		'''
		return Set(self._Entity.Create(name))

	@overload
	def Get(self, name: str) -> Set: ...

	@overload
	def Get(self, id: int) -> Set: ...

	def Get(self, item1 = None) -> Set:
		if isinstance(item1, str):
			return Set(super().Get(item1))

		if isinstance(item1, int):
			return Set(super().Get(item1))

		return Set(self._Entity.Get(item1))

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

	@property
	def Folders(self) -> FolderCol:
		result = self._Entity.Folders
		return FolderCol(result) if result is not None else None

	def Create(self, name: str = None) -> Structure:
		'''
		Attempt to create a new structure.
            If the specified name is already used, it will be deconflicted.
		:param name: The name of the structure to be created.
		'''
		return Structure(self._Entity.Create(name))

	@overload
	def DeleteStructure(self, structure: Structure) -> bool: ...

	@overload
	def DeleteStructure(self, name: str) -> bool: ...

	@overload
	def DeleteStructure(self, id: int) -> bool: ...

	@overload
	def Get(self, name: str) -> Structure: ...

	@overload
	def Get(self, id: int) -> Structure: ...

	def DeleteStructure(self, item1 = None) -> bool:
		if isinstance(item1, Structure):
			return self._Entity.DeleteStructure(item1._Entity)

		if isinstance(item1, str):
			return self._Entity.DeleteStructure(item1)

		if isinstance(item1, int):
			return self._Entity.DeleteStructure(item1)

		return self._Entity.DeleteStructure(item1._Entity)

	def Get(self, item1 = None) -> Structure:
		if isinstance(item1, str):
			return Structure(super().Get(item1))

		if isinstance(item1, int):
			return Structure(super().Get(item1))

		return Structure(self._Entity.Get(item1))

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
	def HyperFea(self) -> HyperFea:
		result = self._Entity.HyperFea
		return HyperFea(result) if result is not None else None

	@property
	def WorkingFolder(self) -> str:
		return self._Entity.WorkingFolder

	@property
	def FemDataSet(self) -> FemDataSet:
		result = self._Entity.FemDataSet
		return FemDataSet(result) if result is not None else None

	@property
	def Beams(self) -> ZoneCol:
		result = self._Entity.Beams
		return ZoneCol(result) if result is not None else None

	@property
	def Id(self) -> int:
		return self._Entity.Id

	@property
	def Joints(self) -> JointCol:
		result = self._Entity.Joints
		return JointCol(result) if result is not None else None

	@property
	def Name(self) -> str:
		return self._Entity.Name

	@property
	def Panels(self) -> ZoneCol:
		result = self._Entity.Panels
		return ZoneCol(result) if result is not None else None

	@property
	def Rundecks(self) -> RundeckCol:
		result = self._Entity.Rundecks
		return RundeckCol(result) if result is not None else None

	@property
	def Sets(self) -> SetCol:
		result = self._Entity.Sets
		return SetCol(result) if result is not None else None

	@property
	def Structures(self) -> StructureCol:
		result = self._Entity.Structures
		return StructureCol(result) if result is not None else None

	@property
	def Zones(self) -> ZoneCol:
		result = self._Entity.Zones
		return ZoneCol(result) if result is not None else None

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		result = self._Entity.PanelSegments
		return PanelSegmentCol(result) if result is not None else None

	@property
	def SectionCuts(self) -> SectionCutCol:
		result = self._Entity.SectionCuts
		return SectionCutCol(result) if result is not None else None

	@property
	def DesignLoads(self) -> DesignLoadCol:
		result = self._Entity.DesignLoads
		return DesignLoadCol(result) if result is not None else None

	@property
	def DiscreteFieldTables(self) -> DiscreteFieldCol:
		result = self._Entity.DiscreteFieldTables
		return DiscreteFieldCol(result) if result is not None else None

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		result = self._Entity.AnalysisProperties
		return AnalysisPropertyCol(result) if result is not None else None

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		result = self._Entity.DesignProperties
		return DesignPropertyCol(result) if result is not None else None

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		result = self._Entity.LoadProperties
		return LoadPropertyCol(result) if result is not None else None

	@property
	def FemFormat(self) -> types.ProjectModelFormat:
		result = self._Entity.FemFormat
		return types.ProjectModelFormat[result.ToString()] if result is not None else None

	def Upload(self, uploadSetName: str, company: str, program: str, tags: tuple[str], notes: str, zoneIds: set[int], jointIds: set[int]) -> bool:
		tagsList = List[str]()
		if tags is not None:
			for thing in tags:
				if thing is not None:
					tagsList.Add(thing)
		tagsEnumerable = IEnumerable(tagsList)
		zoneIdsSet = HashSet[int]()
		if zoneIds is not None:
			for thing in zoneIds:
				if thing is not None:
					zoneIdsSet.Add(thing)
		jointIdsSet = HashSet[int]()
		if jointIds is not None:
			for thing in jointIds:
				if thing is not None:
					jointIdsSet.Add(thing)
		return self._Entity.Upload(uploadSetName, company, program, tagsEnumerable, notes, zoneIdsSet, jointIdsSet)

	def GetDashboardCompanies(self) -> list[str]:
		'''
		This method fetches an array of Dashboard company names that are available to the user who is currently logged in. The URL and authentication token are taken from the last
            Dashboard login made through HyperX.
		'''
		return list[str](self._Entity.GetDashboardCompanies())

	def GetDashboardPrograms(self, companyName: str) -> list[str]:
		'''
		This method fetches an array of Dashboard program names that are available to the user who is currently logged in. The URL and authentication token are taken from the last
            Dashboard login made through HyperX.
		'''
		return list[str](self._Entity.GetDashboardPrograms(companyName))

	def GetDashboardTags(self, companyName: str) -> list[str]:
		'''
		This method fetches an array of Dashboard tags that are available to the user who is currently logged in. The URL and authentication token are taken from the last
            Dashboard login made through HyperX.
		'''
		return list[str](self._Entity.GetDashboardTags(companyName))

	def GenerateSolverSizingInputFile(self, inputFile: str = None, zones: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None) -> str:
		zonesSet = HashSet[int]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesSet.Add(thing)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for thing in sectionCuts:
				if thing is not None:
					sectionCutsSet.Add(thing)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for thing in panelSegments:
				if thing is not None:
					panelSegmentsSet.Add(thing)
		return self._Entity.GenerateSolverSizingInputFile(inputFile, zones if zones is None else zonesSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet)

	def GenerateSolverAnalysisInputFile(self, inputFile: str = None, zones: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None) -> str:
		zonesSet = HashSet[int]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesSet.Add(thing)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for thing in sectionCuts:
				if thing is not None:
					sectionCutsSet.Add(thing)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for thing in panelSegments:
				if thing is not None:
					panelSegmentsSet.Add(thing)
		return self._Entity.GenerateSolverAnalysisInputFile(inputFile, zones if zones is None else zonesSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet)

	def FullRunSolverSizing(self, inputFile: str = None, outputFile: str = None, zones: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None, nThreads: int = None) -> bool:
		zonesSet = HashSet[int]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesSet.Add(thing)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for thing in sectionCuts:
				if thing is not None:
					sectionCutsSet.Add(thing)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for thing in panelSegments:
				if thing is not None:
					panelSegmentsSet.Add(thing)
		return self._Entity.FullRunSolverSizing(inputFile, outputFile, zones if zones is None else zonesSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet, nThreads)

	def FullRunSolverAnalysis(self, inputFile: str = None, outputFile: str = None, zones: set[int] = None, sectionCuts: set[int] = None, panelSegments: set[int] = None, nThreads: int = None) -> bool:
		zonesSet = HashSet[int]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesSet.Add(thing)
		sectionCutsSet = HashSet[int]()
		if sectionCuts is not None:
			for thing in sectionCuts:
				if thing is not None:
					sectionCutsSet.Add(thing)
		panelSegmentsSet = HashSet[int]()
		if panelSegments is not None:
			for thing in panelSegments:
				if thing is not None:
					panelSegmentsSet.Add(thing)
		return self._Entity.FullRunSolverAnalysis(inputFile, outputFile, zones if zones is None else zonesSet, sectionCuts if sectionCuts is None else sectionCutsSet, panelSegments if panelSegments is None else panelSegmentsSet, nThreads)

	def RunSolver(self, inputFile: str, outputFile: str = None, nThreads: int = None) -> bool:
		return self._Entity.RunSolver(inputFile, outputFile, nThreads)

	def Dispose(self) -> None:
		return self._Entity.Dispose()

	def PackageProject(self, destinationFilePath: str, includeFemInputFiles: bool = True, includeFemOutputFiles: bool = True, includeWorkingFolder: bool = True, includeLoadFiles: bool = True, includePluginPackages: bool = False, removeAllOtherProjects: bool = False, deleteUnusedPropertiesAndMaterials: bool = False, mapFemFilesToRelativePaths: bool = True, additionalFiles: tuple[str] = None) -> types.SimpleStatus:
		additionalFilesList = List[str]()
		if additionalFiles is not None:
			for thing in additionalFiles:
				if thing is not None:
					additionalFilesList.Add(thing)
		additionalFilesEnumerable = IEnumerable(additionalFilesList)
		return types.SimpleStatus(self._Entity.PackageProject(destinationFilePath, includeFemInputFiles, includeFemOutputFiles, includeWorkingFolder, includeLoadFiles, includePluginPackages, removeAllOtherProjects, deleteUnusedPropertiesAndMaterials, mapFemFilesToRelativePaths, additionalFiles if additionalFiles is None else additionalFilesEnumerable))

	def ImportFem(self) -> None:
		return self._Entity.ImportFem()

	def ImportFeaResults(self, alwaysImport: bool = False) -> str:
		'''
		Manually import design loads.
		:param alwaysImport: If true, loads are imported even if loads have already previously been imported.
		'''
		return self._Entity.ImportFeaResults(alwaysImport)

	def SetFemFormat(self, femFormat: types.ProjectModelFormat) -> None:
		return self._Entity.SetFemFormat(_types.ProjectModelFormat(femFormat.value))

	def SetFemUnits(self, femForceId: DbForceUnit, femLengthId: DbLengthUnit, femMassId: DbMassUnit, femTemperatureId: DbTemperatureUnit) -> SetUnitsStatus:
		return SetUnitsStatus[self._Entity.SetFemUnits(_api.DbForceUnit(femForceId.value), _api.DbLengthUnit(femLengthId.value), _api.DbMassUnit(femMassId.value), _api.DbTemperatureUnit(femTemperatureId.value)).ToString()]

	def SizeJoints(self, joints: tuple[Joint] = None) -> types.SimpleStatus:
		jointsList = List[_api.Joint]()
		if joints is not None:
			for thing in joints:
				if thing is not None:
					jointsList.Add(thing._Entity)
		jointsEnumerable = IEnumerable(jointsList)
		return types.SimpleStatus(self._Entity.SizeJoints(joints if joints is None else jointsEnumerable))

	def GetJointsWithoutResults(self, joints: tuple[Joint]) -> set[int]:
		jointsList = List[_api.Joint]()
		if joints is not None:
			for thing in joints:
				if thing is not None:
					jointsList.Add(thing._Entity)
		jointsEnumerable = IEnumerable(jointsList)
		return set[int](self._Entity.GetJointsWithoutResults(jointsEnumerable))

	@overload
	def AnalyzeZones(self, zones: tuple[ZoneBase] = None) -> types.TernaryStatus: ...

	@overload
	def AnalyzeZones(self, zoneIds: tuple[int]) -> types.TernaryStatus: ...

	@overload
	def SizeZones(self, zones: tuple[ZoneBase] = None) -> types.TernaryStatus: ...

	@overload
	def SizeZones(self, zoneIds: tuple[int]) -> types.TernaryStatus: ...

	def CreateNonFeaZone(self, category: types.FamilyCategory, name: str = None) -> Zone:
		'''
		Create a non-FEA zone by name and category.
		'''
		result = self._Entity.CreateNonFeaZone(_types.FamilyCategory(category.value), name)
		thisClass = type(result).__name__
		givenClass = Zone
		for subclass in Zone.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def ReturnToUnusedFem(self, zoneNumbers: tuple[int] = None, jointIds: tuple[int] = None) -> None:
		zoneNumbersList = MakeCSharpIntList(zoneNumbers)
		zoneNumbersEnumerable = IEnumerable(zoneNumbersList)
		jointIdsList = MakeCSharpIntList(jointIds)
		jointIdsEnumerable = IEnumerable(jointIdsList)
		return self._Entity.ReturnToUnusedFem(zoneNumbers if zoneNumbers is None else zoneNumbersEnumerable, jointIds if jointIds is None else jointIdsEnumerable)

	def UnimportFemAsync(self) -> Task:
		return Task(self._Entity.UnimportFemAsync())

	def ExportFem(self, destinationFolder: str) -> None:
		return self._Entity.ExportFem(destinationFolder)

	def ImportCad(self, filePath: str) -> None:
		'''
		Import CAD from a file.
		'''
		return self._Entity.ImportCad(filePath)

	@overload
	def ExportCad(self, filePath: str) -> None: ...

	@overload
	def ExportCad(self, cadIds: tuple[int], filePath: str) -> None: ...

	def RegeneratePfem(self) -> None:
		'''
		Regenerates and displays the preview FEM. If running a script outside of the Script Runner,
            do not call this method
		'''
		return self._Entity.RegeneratePfem()

	def AnalyzeZones(self, item1 = None) -> types.TernaryStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], ZoneBase):
			zonesList = List[_api.ZoneBase]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return types.TernaryStatus(self._Entity.AnalyzeZones(item1 if item1 is None else zonesEnumerable))

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return types.TernaryStatus(self._Entity.AnalyzeZones(zoneIdsEnumerable))

		return types.TernaryStatus(self._Entity.AnalyzeZones(item1))

	def SizeZones(self, item1 = None) -> types.TernaryStatus:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], ZoneBase):
			zonesList = List[_api.ZoneBase]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing._Entity)
			zonesEnumerable = IEnumerable(zonesList)
			return types.TernaryStatus(self._Entity.SizeZones(item1 if item1 is None else zonesEnumerable))

		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int):
			zoneIdsList = MakeCSharpIntList(item1)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return types.TernaryStatus(self._Entity.SizeZones(zoneIdsEnumerable))

		return types.TernaryStatus(self._Entity.SizeZones(item1))

	def ExportCad(self, item1 = None, item2 = None) -> None:
		if isinstance(item1, tuple) and item1 and isinstance(item1[0], int) and isinstance(item2, str):
			cadIdsList = MakeCSharpIntList(item1)
			cadIdsEnumerable = IEnumerable(cadIdsList)
			return self._Entity.ExportCad(cadIdsEnumerable, item2)

		if isinstance(item1, str):
			return self._Entity.ExportCad(item1)

		return self._Entity.ExportCad(item1, item2)


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

		return FailureModeCategory(self._Entity.Get(item1))

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
		'''
		Look up an Foam material by its name.
		'''
		return Foam(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an foam material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, density: float, newMaterialName: str = None, femId: int = None) -> Foam:
		return Foam(self._Entity.Create(materialFamilyName, density, newMaterialName, femId))

	def Copy(self, fmToCopyName: str, newMaterialName: str = None, femId: int = None) -> Foam:
		return Foam(self._Entity.Copy(fmToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete a foam material by name.
            Returns false if the method the material is not found.
		'''
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
		'''
		Look up an Honeycomb material by its name.
		'''
		return Honeycomb(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an honeycomb material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, density: float, newMaterialName: str = None, femId: int = None) -> Honeycomb:
		return Honeycomb(self._Entity.Create(materialFamilyName, density, newMaterialName, femId))

	def Copy(self, honeyToCopyName: str, newMaterialName: str = None, femId: int = None) -> Honeycomb:
		return Honeycomb(self._Entity.Copy(honeyToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete a honeycomb material by name.
            Returns false if the method the material is not found.
		'''
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
		'''
		Look up an Isotropic material by its name.
		'''
		return Isotropic(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an isotropic material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, density: float, newMaterialName: str = None, femId: int = None) -> Isotropic:
		return Isotropic(self._Entity.Create(materialFamilyName, density, newMaterialName, femId))

	def Copy(self, isoToCopyName: str, newMaterialName: str = None, femId: int = None) -> Isotropic:
		return Isotropic(self._Entity.Copy(isoToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete an isotropic material by name.
            Returns false if the method the material is not found.
		'''
		return self._Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.IsotropicColList[index]

	def __iter__(self):
		yield from self.IsotropicColList

	def __len__(self):
		return len(self.IsotropicColList)


class LaminateFamilyCol(IdNameEntityCol[LaminateFamily]):
	def __init__(self, laminateFamilyCol: _api.LaminateFamilyCol):
		self._Entity = laminateFamilyCol
		self._CollectedClass = LaminateFamily

	@property
	def LaminateFamilyColList(self) -> tuple[LaminateFamily]:
		return tuple([LaminateFamily(laminateFamilyCol) for laminateFamilyCol in self._Entity])

	@overload
	def Get(self, name: str) -> LaminateFamily: ...

	@overload
	def Get(self, id: int) -> LaminateFamily: ...

	def Get(self, item1 = None) -> LaminateFamily:
		if isinstance(item1, str):
			return LaminateFamily(super().Get(item1))

		if isinstance(item1, int):
			return LaminateFamily(super().Get(item1))

		return LaminateFamily(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LaminateFamilyColList[index]

	def __iter__(self):
		yield from self.LaminateFamilyColList

	def __len__(self):
		return len(self.LaminateFamilyColList)


class LaminateCol(Generic[T]):
	def __init__(self, laminateCol: _api.LaminateCol):
		self._Entity = laminateCol

	@property
	def LaminateColList(self) -> tuple[Laminate]:
		return tuple([Laminate(laminateCol) for laminateCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, laminateName: str) -> LaminateBase:
		'''
		Look up a Laminate by its name.
		'''
		result = self._Entity.Get(laminateName)
		thisClass = type(result).__name__
		givenClass = LaminateBase
		for subclass in LaminateBase.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def Contains(self, laminateName: str) -> bool:
		return self._Entity.Contains(laminateName)

	def CreateLaminate(self, materialFamily: str, laminateName: str = None) -> Laminate:
		'''
		Create laminate.
		'''
		return Laminate(self._Entity.CreateLaminate(materialFamily, laminateName))

	def CreateStiffenerLaminate(self, materialFamily: str, stiffenerProfile: types.StiffenerProfile, laminateName: str = None) -> StiffenerLaminate:
		'''
		Create a stiffener laminate.
		'''
		return StiffenerLaminate(self._Entity.CreateStiffenerLaminate(materialFamily, _types.StiffenerProfile(stiffenerProfile.value), laminateName))

	def Copy(self, laminateToCopyName: str, newLaminateName: str = None) -> LaminateBase:
		'''
		Copy a laminate material by name.
		'''
		result = self._Entity.Copy(laminateToCopyName, newLaminateName)
		thisClass = type(result).__name__
		givenClass = LaminateBase
		for subclass in LaminateBase.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def Delete(self, name: str) -> bool:
		'''
		Delete a laminate material by name.
            Returns false if the material is not found or removed.
		'''
		return self._Entity.Delete(name)

	def GetLaminate(self, name: str) -> Laminate:
		'''
		Get a laminate by name.
		'''
		return Laminate(self._Entity.GetLaminate(name))

	def GetStiffenerLaminate(self, name: str) -> StiffenerLaminate:
		'''
		Get a stiffener laminate by name.
		'''
		return StiffenerLaminate(self._Entity.GetStiffenerLaminate(name))

	def __getitem__(self, index: int):
		return self.LaminateColList[index]

	def __iter__(self):
		yield from self.LaminateColList

	def __len__(self):
		return len(self.LaminateColList)


class OrthotropicCol(Generic[T]):
	def __init__(self, orthotropicCol: _api.OrthotropicCol):
		self._Entity = orthotropicCol

	@property
	def OrthotropicColList(self) -> tuple[Orthotropic]:
		return tuple([Orthotropic(orthotropicCol) for orthotropicCol in self._Entity])

	def Count(self) -> int:
		return self._Entity.Count()

	def Get(self, materialName: str) -> Orthotropic:
		'''
		Look up an Orthotropic material by its name.
		'''
		return Orthotropic(self._Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		'''
		Check if an orthotropic material exists in this collection.
		'''
		return self._Entity.Contains(materialName)

	def Create(self, materialFamilyName: str, thickness: float, density: float, newMaterialName: str = None, femId: int = None) -> Orthotropic:
		return Orthotropic(self._Entity.Create(materialFamilyName, thickness, density, newMaterialName, femId))

	def Copy(self, orthoToCopyName: str, newMaterialName: str = None, femId: int = None) -> Orthotropic:
		return Orthotropic(self._Entity.Copy(orthoToCopyName, newMaterialName, femId))

	def Delete(self, materialName: str) -> bool:
		'''
		Delete an orthotropic material by name.
            Returns false if the method the material is not found.
		'''
		return self._Entity.Delete(materialName)

	def GenerateEffectiveLaminates(self, tapeMaterialId: int, fabricMaterialId: int, namePrefix: str, minTape0: int = 10, maxTape0: int = 50, stepTape0: int = 10, minTape45: int = 20, maxTape45: int = 60, stepTape45: int = 20, minTape90: int = 10, maxTape90: int = 50, stepTape90: int = 10, minFabric0: int = 10, maxFabric0: int = 50, stepFabric0: int = 10, minFabric45: int = 20, maxFabric45: int = 60, stepFabric45: int = 10, minFabric90: int = 10, maxFabric90: int = 50, stepFabric90: int = 10) -> list[Orthotropic]:
		return [Orthotropic(orthotropic) for orthotropic in self._Entity.GenerateEffectiveLaminates(tapeMaterialId, fabricMaterialId, namePrefix, minTape0, maxTape0, stepTape0, minTape45, maxTape45, stepTape45, minTape90, maxTape90, stepTape90, minFabric0, maxFabric0, stepFabric0, minFabric45, maxFabric45, stepFabric45, minFabric90, maxFabric90, stepFabric90)]

	def CreateEffectiveLaminate(self, tapeMaterialId: int, fabricMaterialId: int, namePrefix: str, tape0: int, tape45: int, tape90: int, fabric0: int, fabric45: int, fabric90: int) -> Orthotropic:
		return Orthotropic(self._Entity.CreateEffectiveLaminate(tapeMaterialId, fabricMaterialId, namePrefix, tape0, tape45, tape90, fabric0, fabric45, fabric90))

	def __getitem__(self, index: int):
		return self.OrthotropicColList[index]

	def __iter__(self):
		yield from self.OrthotropicColList

	def __len__(self):
		return len(self.OrthotropicColList)


class PluginPackageCol(IdNameEntityCol[PluginPackage]):
	def __init__(self, pluginPackageCol: _api.PluginPackageCol):
		self._Entity = pluginPackageCol
		self._CollectedClass = PluginPackage

	@property
	def PluginPackageColList(self) -> tuple[PluginPackage]:
		return tuple([PluginPackage(pluginPackageCol) for pluginPackageCol in self._Entity])

	def AddPluginPackage(self, path: str) -> PluginPackage:
		'''
		Add a plugin package by path.
		'''
		return PluginPackage(self._Entity.AddPluginPackage(path))

	@overload
	def RemovePluginPackage(self, name: str) -> bool: ...

	@overload
	def RemovePluginPackage(self, id: int) -> bool: ...

	def ClearAllPluginPackages(self) -> None:
		'''
		Clears all packages out of the database
		'''
		return self._Entity.ClearAllPluginPackages()

	def GetPluginPackages(self) -> list[PluginPackage]:
		'''
		Gets a list of package info
            Includes name, id, file path, version, description, and modification date
		'''
		return [PluginPackage(pluginPackage) for pluginPackage in self._Entity.GetPluginPackages()]

	@overload
	def Get(self, name: str) -> PluginPackage: ...

	@overload
	def Get(self, id: int) -> PluginPackage: ...

	def RemovePluginPackage(self, item1 = None) -> bool:
		if isinstance(item1, str):
			return self._Entity.RemovePluginPackage(item1)

		if isinstance(item1, int):
			return self._Entity.RemovePluginPackage(item1)

		return self._Entity.RemovePluginPackage(item1)

	def Get(self, item1 = None) -> PluginPackage:
		if isinstance(item1, str):
			return PluginPackage(super().Get(item1))

		if isinstance(item1, int):
			return PluginPackage(super().Get(item1))

		return PluginPackage(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.PluginPackageColList[index]

	def __iter__(self):
		yield from self.PluginPackageColList

	def __len__(self):
		return len(self.PluginPackageColList)


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

		return ProjectInfo(self._Entity.Get(item1))

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
		if isinstance(application, Application):
			self._Entity = application._Entity
		else:
			self._Entity = application

	@property
	def UnitSystem(self) -> UnitSystem:
		'''
		Unit system specified when starting a scripting Application.
		'''
		result = self._Entity.UnitSystem
		return UnitSystem[result.ToString()] if result is not None else None

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
		result = self._Entity.ActiveProject
		return Project(result) if result is not None else None

	@property
	def UiRunnerMode(self) -> bool:
		return self._Entity.UiRunnerMode

	@property
	def Version(self) -> str:
		return self._Entity.Version

	@property
	def FailureModeCategories(self) -> FailureModeCategoryCol:
		result = self._Entity.FailureModeCategories
		return FailureModeCategoryCol(result) if result is not None else None

	@property
	def FailureModes(self) -> FailureModeCol:
		result = self._Entity.FailureModes
		return FailureModeCol(result) if result is not None else None

	@property
	def Packages(self) -> PluginPackageCol:
		result = self._Entity.Packages
		return PluginPackageCol(result) if result is not None else None

	@property
	def Foams(self) -> FoamCol:
		'''
		Contains a set of all foam materials in a database.
		'''
		result = self._Entity.Foams
		return FoamCol(result) if result is not None else None

	@property
	def Honeycombs(self) -> HoneycombCol:
		'''
		Contains a set of all honeycomb materials in a database.
		'''
		result = self._Entity.Honeycombs
		return HoneycombCol(result) if result is not None else None

	@property
	def Isotropics(self) -> IsotropicCol:
		'''
		Contains a set of all isotropic materials in a database.
		'''
		result = self._Entity.Isotropics
		return IsotropicCol(result) if result is not None else None

	@property
	def Laminates(self) -> LaminateCol:
		result = self._Entity.Laminates
		return LaminateCol(result) if result is not None else None

	@property
	def LaminateFamilies(self) -> LaminateFamilyCol:
		result = self._Entity.LaminateFamilies
		return LaminateFamilyCol(result) if result is not None else None

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		result = self._Entity.AnalysisProperties
		return AnalysisPropertyCol(result) if result is not None else None

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		result = self._Entity.DesignProperties
		return DesignPropertyCol(result) if result is not None else None

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		result = self._Entity.LoadProperties
		return LoadPropertyCol(result) if result is not None else None

	@property
	def Orthotropics(self) -> OrthotropicCol:
		'''
		Contains a set of all orthotropic materials in a database.
		'''
		result = self._Entity.Orthotropics
		return OrthotropicCol(result) if result is not None else None

	@property
	def ProjectInfos(self) -> ProjectInfoCol:
		'''
		Contains a set of all projects in a database.
		'''
		result = self._Entity.ProjectInfos
		return ProjectInfoCol(result) if result is not None else None

	@property
	def UserName(self) -> str:
		return self._Entity.UserName

	@UserName.setter
	def UserName(self, value: str) -> None:
		self._Entity.UserName = value

	def PauseUpdates(self) -> None:
		'''
		Pause the sending of updates as items are created.  Once resumed, all updates will be
            processed.
		'''
		return self._Entity.PauseUpdates()

	def ResumeUpdates(self) -> None:
		'''
		Resume the sending of updates.  Any paused updates will be processed.
		'''
		return self._Entity.ResumeUpdates()

	def UnpackageProject(self, sourcePackagePath: str, destinationFolder: str = None, includeFemInputOutputFiles: bool = True, includeWorkingFolder: bool = True, includeLoadFiles: bool = True, includeAdditionalFiles: bool = True) -> types.SimpleStatus:
		'''
		Unpackage the source .hxp package into the destination folder. Note, the destination folder should be empty.
		'''
		return types.SimpleStatus(self._Entity.UnpackageProject(sourcePackagePath, destinationFolder, includeFemInputOutputFiles, includeWorkingFolder, includeLoadFiles, includeAdditionalFiles))

	def CompareDatabases(self, outputPath: str, originalDatabasePath: str, modifiedDatabasePath: str, originalProject: str = None, modifiedProject: str = None, compareAssignableProperties: bool = True, compareMaterialsFastenersAndRivets: bool = True, compareProjectSetup: bool = False) -> types.SimpleStatus:
		return types.SimpleStatus(self._Entity.CompareDatabases(outputPath, originalDatabasePath, modifiedDatabasePath, originalProject, modifiedProject, compareAssignableProperties, compareMaterialsFastenersAndRivets, compareProjectSetup))

	def CloseDatabase(self, delay: int = 1) -> None:
		'''
		Close the currently open database if one exists.
		:param delay: Delay closing the connection for this many seconds.
		'''
		return self._Entity.CloseDatabase(delay)

	def CopyProject(self, projectId: int, newName: str = None, copyDesignProperties: bool = True, copyAnalysisProperties: bool = True, copyLoadProperties: bool = True, copyWorkingFolder: bool = True) -> ProjectInfo:
		'''
		Copy a project
		:param projectId: Id of the project to copy
		:param newName: Name for the new project
		:param copyDesignProperties: Flag indicating whether design properties should be copied in the new project
		:param copyAnalysisProperties: Flag indicating whether analysis properties should be copied in the new project
		:param copyLoadProperties: Flag indicating whether load properties should be copied in the new project
		:param copyWorkingFolder: Flag indicating whether working folder should be copied
		'''
		return ProjectInfo(self._Entity.CopyProject(projectId, newName, copyDesignProperties, copyAnalysisProperties, copyLoadProperties, copyWorkingFolder))

	def CreateDatabaseFromTemplate(self, templateName: str, newPath: str) -> None:
		'''
		Create a new database.
		:param templateName: The name of the template to base this database on.
		:param newPath: The path to the new database.
		'''
		return self._Entity.CreateDatabaseFromTemplate(templateName, newPath)

	def CreateProject(self, projectName: str = None) -> ProjectInfo:
		'''
		Create a Project.
		'''
		return ProjectInfo(self._Entity.CreateProject(projectName))

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
		Get all Analysis Definitions in the database.
		'''
		return dict[int, AnalysisDefinition](self._Entity.GetAnalyses())

	def Login(self, userName: str, password: str = "") -> None:
		'''
		Login to the Scripting API with a specified username and password.
		:param userName: Username to login with.
		:param password: Password to log in with
		'''
		return self._Entity.Login(userName, password)

	def Migrate(self, databasePath: str) -> str:
		'''
		Migrate the database to the latest version.
		'''
		return self._Entity.Migrate(databasePath)

	def CheckDatabaseIsUpToDate(self, databasePath: str) -> bool:
		'''
		Returns true if the database version matches the version of this scripting API.
            Otherwise returns false.
		'''
		return self._Entity.CheckDatabaseIsUpToDate(databasePath)

	def OpenDatabase(self, databasePath: str) -> None:
		'''
		Open a database to manipulate with the API.
		:param databasePath: File path to the DB.
		'''
		return self._Entity.OpenDatabase(databasePath)

	def SelectProject(self, projectName: str) -> Project:
		'''
		Select the active project.
            Activating a project will deactivate the current project (if present).
		'''
		return Project(self._Entity.SelectProject(projectName))

	def ImportMaterialsFromExcel(self, filePath: str, deletePlies: bool = False, updateMaterialsInUseInOtherProjects: bool = False) -> types.SimpleStatus:
		'''
		Import materials from an Excel spreadsheet. Returns true on successful import.
		:param deletePlies: Determines whether to update laminate or laminate families with changes that will delete plies in structures.
		:param updateMaterialsInUseInOtherProjects: Determines whether to update materials in use by projects outside the active project.
		'''
		return types.SimpleStatus(self._Entity.ImportMaterialsFromExcel(filePath, deletePlies, updateMaterialsInUseInOtherProjects))


class JointDesignProperty(DesignProperty):
	def __init__(self, jointDesignProperty: _api.JointDesignProperty):
		self._Entity = jointDesignProperty


class SizingMaterial(IdEntity):
	def __init__(self, sizingMaterial: _api.SizingMaterial):
		self._Entity = sizingMaterial

	@property
	def MaterialId(self) -> int:
		return self._Entity.MaterialId

	@property
	def MaterialType(self) -> types.MaterialType:
		'''
		Represents a material's type.
		'''
		result = self._Entity.MaterialType
		return types.MaterialType[result.ToString()] if result is not None else None


class SizingMaterialCol(IdEntityCol[SizingMaterial]):
	def __init__(self, sizingMaterialCol: _api.SizingMaterialCol):
		self._Entity = sizingMaterialCol
		self._CollectedClass = SizingMaterial

	@property
	def SizingMaterialColList(self) -> tuple[SizingMaterial]:
		return tuple([SizingMaterial(sizingMaterialCol) for sizingMaterialCol in self._Entity])

	@overload
	def Get(self, name: str) -> SizingMaterial: ...

	@overload
	def Contains(self, name: str) -> bool: ...

	@overload
	def AddSizingMaterial(self, materialId: int) -> bool: ...

	@overload
	def AddSizingMaterial(self, name: str) -> bool: ...

	@overload
	def RemoveSizingMaterial(self, materialId: int) -> bool: ...

	@overload
	def RemoveSizingMaterial(self, name: str) -> bool: ...

	@overload
	def Contains(self, id: int) -> bool: ...

	@overload
	def Get(self, id: int) -> SizingMaterial: ...

	def Get(self, item1 = None) -> SizingMaterial:
		if isinstance(item1, str):
			return SizingMaterial(self._Entity.Get(item1))

		if isinstance(item1, int):
			return SizingMaterial(super().Get(item1))

		return SizingMaterial(self._Entity.Get(item1))

	def Contains(self, item1 = None) -> bool:
		if isinstance(item1, str):
			return self._Entity.Contains(item1)

		if isinstance(item1, int):
			return bool(super().Contains(item1))

		return self._Entity.Contains(item1)

	def AddSizingMaterial(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return self._Entity.AddSizingMaterial(item1)

		if isinstance(item1, str):
			return self._Entity.AddSizingMaterial(item1)

		return self._Entity.AddSizingMaterial(item1)

	def RemoveSizingMaterial(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return self._Entity.RemoveSizingMaterial(item1)

		if isinstance(item1, str):
			return self._Entity.RemoveSizingMaterial(item1)

		return self._Entity.RemoveSizingMaterial(item1)

	def __getitem__(self, index: int):
		return self.SizingMaterialColList[index]

	def __iter__(self):
		yield from self.SizingMaterialColList

	def __len__(self):
		return len(self.SizingMaterialColList)


class ZoneOverride(IdEntity):
	def __init__(self, zoneOverride: _api.ZoneOverride):
		self._Entity = zoneOverride

	@property
	def AllowMaterials(self) -> bool:
		return self._Entity.AllowMaterials

	@property
	def ProjectId(self) -> int:
		return self._Entity.ProjectId

	@property
	def DesignId(self) -> int:
		return self._Entity.DesignId

	@property
	def FamilyId(self) -> types.BeamPanelFamily:
		result = self._Entity.FamilyId
		return types.BeamPanelFamily[result.ToString()] if result is not None else None

	@property
	def ConceptId(self) -> int:
		return self._Entity.ConceptId

	@property
	def VariableId(self) -> int:
		return self._Entity.VariableId

	@property
	def MinBound(self) -> float:
		return self._Entity.MinBound

	@property
	def MaxBound(self) -> float:
		return self._Entity.MaxBound

	@property
	def StepSize(self) -> float:
		return self._Entity.StepSize

	@property
	def MinPlies(self) -> int:
		return self._Entity.MinPlies

	@property
	def MaxPlies(self) -> int:
		return self._Entity.MaxPlies

	@property
	def PlyStepSize(self) -> int:
		return self._Entity.PlyStepSize

	@property
	def InputMode(self) -> types.VariableInputMode:
		result = self._Entity.InputMode
		return types.VariableInputMode[result.ToString()] if result is not None else None

	@property
	def SizingMaterials(self) -> SizingMaterialCol:
		result = self._Entity.SizingMaterials
		return SizingMaterialCol(result) if result is not None else None

	@property
	def AnalysisValue(self) -> float:
		return self._Entity.AnalysisValue

	@property
	def AnalysisMaterial(self) -> str:
		return self._Entity.AnalysisMaterial

	@property
	def AnalysisMaterialType(self) -> types.MaterialType:
		result = self._Entity.AnalysisMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@MinBound.setter
	def MinBound(self, value: float) -> None:
		self._Entity.MinBound = value

	@MaxBound.setter
	def MaxBound(self, value: float) -> None:
		self._Entity.MaxBound = value

	@StepSize.setter
	def StepSize(self, value: float) -> None:
		self._Entity.StepSize = value

	@MinPlies.setter
	def MinPlies(self, value: int) -> None:
		self._Entity.MinPlies = value

	@MaxPlies.setter
	def MaxPlies(self, value: int) -> None:
		self._Entity.MaxPlies = value

	@PlyStepSize.setter
	def PlyStepSize(self, value: int) -> None:
		self._Entity.PlyStepSize = value

	@AnalysisValue.setter
	def AnalysisValue(self, value: float) -> None:
		self._Entity.AnalysisValue = value

	@AnalysisMaterial.setter
	def AnalysisMaterial(self, value: str) -> None:
		self._Entity.AnalysisMaterial = value


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
		result = self._Entity.ToolingSelectionType
		return types.ToolingSelectionType[result.ToString()] if result is not None else None

	def SetToAnyValue(self) -> None:
		return self._Entity.SetToAnyValue()

	def SetToInequality(self, value: float) -> None:
		return self._Entity.SetToInequality(value)

	def SetToRange(self, min: float, max: float) -> None:
		return self._Entity.SetToRange(min, max)

	def SetToValue(self, value: float) -> None:
		return self._Entity.SetToValue(value)


class ZoneOverrideCol(IdEntityCol[ZoneOverride]):
	def __init__(self, zoneOverrideCol: _api.ZoneOverrideCol):
		self._Entity = zoneOverrideCol
		self._CollectedClass = ZoneOverride

	@property
	def ZoneOverrideColList(self) -> tuple[ZoneOverride]:
		return tuple([ZoneOverride(zoneOverrideCol) for zoneOverrideCol in self._Entity])

	def Get(self, zoneNumber: int) -> ZoneOverride:
		'''
		Get override for a zone by the zone number
		'''
		return ZoneOverride(self._Entity.Get(zoneNumber))

	def __getitem__(self, index: int):
		return self.ZoneOverrideColList[index]

	def __iter__(self):
		yield from self.ZoneOverrideColList

	def __len__(self):
		return len(self.ZoneOverrideColList)


class DesignVariable(IdEntity):
	'''
	Holds design variable data.
            Min, max, steps, materials.
	'''
	def __init__(self, designVariable: _api.DesignVariable):
		self._Entity = designVariable

	@property
	def VariableParameter(self) -> types.VariableParameter:
		result = self._Entity.VariableParameter
		return types.VariableParameter[result.ToString()] if result is not None else None

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

	@property
	def AnalysisMaterial(self) -> str:
		return self._Entity.AnalysisMaterial

	@property
	def AnalysisMaterialType(self) -> types.MaterialType:
		result = self._Entity.AnalysisMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def SizingMaterialType(self) -> types.MaterialType:
		result = self._Entity.SizingMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def AnalysisValue(self) -> float:
		return self._Entity.AnalysisValue

	@property
	def Overrides(self) -> ZoneOverrideCol:
		result = self._Entity.Overrides
		return ZoneOverrideCol(result) if result is not None else None

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

	@AnalysisMaterial.setter
	def AnalysisMaterial(self, value: str) -> None:
		self._Entity.AnalysisMaterial = value

	@AnalysisValue.setter
	def AnalysisValue(self, value: float) -> None:
		self._Entity.AnalysisValue = value

	@overload
	def AddMaterials(self, materialIds: set[int]) -> None: ...

	@overload
	def AddMaterials(self, materialNames: set[str]) -> None: ...

	def GetSizingMaterials(self) -> list[int]:
		'''
		Get a list of materials used for sizing, if they exist.
		'''
		return [int32 for int32 in self._Entity.GetSizingMaterials()]

	def RemoveSizingMaterials(self, materialIds: tuple[int] = None) -> None:
		materialIdsList = MakeCSharpIntList(materialIds)
		materialIdsEnumerable = IEnumerable(materialIdsList)
		return self._Entity.RemoveSizingMaterials(materialIds if materialIds is None else materialIdsEnumerable)

	def GetAnalysisMaterial(self) -> int:
		'''
		Get the material used for analysis, if it exists.
		'''
		return int(self._Entity.GetAnalysisMaterial())

	def RemoveAnalysisMaterial(self) -> None:
		'''
		Remove the analysis material assigned to this variable.
		'''
		return self._Entity.RemoveAnalysisMaterial()

	def AddMaterials(self, item1 = None) -> None:
		if isinstance(item1, set) and item1 and isinstance(list(item1)[0], int):
			materialIdsSet = HashSet[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						materialIdsSet.Add(thing)
			return self._Entity.AddMaterials(materialIdsSet)

		if isinstance(item1, set) and item1 and isinstance(list(item1)[0], str):
			materialNamesSet = HashSet[str]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						materialNamesSet.Add(thing)
			return self._Entity.AddMaterials(materialNamesSet)

		return self._Entity.AddMaterials(item1)


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

		return ToolingConstraint(self._Entity.Get(item1))

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

	@overload
	def Get(self, parameterId: types.VariableParameter) -> DesignVariable: ...

	@overload
	def Get(self, id: int) -> DesignVariable: ...

	def Get(self, item1 = None) -> DesignVariable:
		if isinstance(item1, types.VariableParameter):
			return DesignVariable(self._Entity.Get(_types.VariableParameter(item1.value)))

		if isinstance(item1, int):
			return DesignVariable(super().Get(item1))

		return DesignVariable(self._Entity.Get(_types.VariableParameter(item1.value)))

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
	def FamilyId(self) -> types.BeamPanelFamily:
		result = self._Entity.FamilyId
		return types.BeamPanelFamily[result.ToString()] if result is not None else None

	@property
	def ConceptId(self) -> int:
		return self._Entity.ConceptId

	@property
	def FamilyConceptUID(self) -> types.FamilyConceptUID:
		result = self._Entity.FamilyConceptUID
		return types.FamilyConceptUID[result.ToString()] if result is not None else None

	@property
	def ToolingConstraints(self) -> ToolingConstraintCol:
		result = self._Entity.ToolingConstraints
		return ToolingConstraintCol(result) if result is not None else None

	@property
	def DesignVariables(self) -> DesignVariableCol:
		result = self._Entity.DesignVariables
		return DesignVariableCol(result) if result is not None else None


class BulkUpdaterBase(ABC):
	def __init__(self, bulkUpdaterBase: _api.BulkUpdaterBase):
		self._Entity = bulkUpdaterBase

	def Update(self, func: Action) -> None:
		entityType = self._Entity.GetType().BaseType.GenericTypeArguments[0]
		funcAction = Action[entityType](func)
		return self._Entity.Update(funcAction)


class LoadPropertyUserRowBulkUpdater(BulkUpdaterBase):
	def __init__(self, loadPropertyUserRowBulkUpdater: _api.LoadPropertyUserRowBulkUpdater):
		self._Entity = loadPropertyUserRowBulkUpdater


class LoadPropertyUserRow(IdNameEntity):
	def __init__(self, loadPropertyUserRow: _api.LoadPropertyUserRow):
		self._Entity = loadPropertyUserRow

	@property
	def LoadScenarioId(self) -> int:
		return self._Entity.LoadScenarioId

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def Type(self) -> types.LoadSetType:
		result = self._Entity.Type
		return types.LoadSetType[result.ToString()] if result is not None else None

	@property
	def ReferenceTemperature(self) -> float:
		return self._Entity.ReferenceTemperature

	@property
	def PressureOrTemperature(self) -> float:
		return self._Entity.PressureOrTemperature

	@property
	def LimitFactor(self) -> float:
		return self._Entity.LimitFactor

	@property
	def UltimateFactor(self) -> float:
		return self._Entity.UltimateFactor

	@ReferenceTemperature.setter
	def ReferenceTemperature(self, value: float) -> None:
		self._Entity.ReferenceTemperature = value

	@PressureOrTemperature.setter
	def PressureOrTemperature(self, value: float) -> None:
		self._Entity.PressureOrTemperature = value

	@LimitFactor.setter
	def LimitFactor(self, value: float) -> None:
		self._Entity.LimitFactor = value

	@UltimateFactor.setter
	def UltimateFactor(self, value: float) -> None:
		self._Entity.UltimateFactor = value


class LoadPropertyUserBeamRow(LoadPropertyUserRow):
	def __init__(self, loadPropertyUserBeamRow: _api.LoadPropertyUserBeamRow):
		self._Entity = loadPropertyUserBeamRow

	@property
	def M1A(self) -> float:
		return self._Entity.M1A

	@property
	def M2A(self) -> float:
		return self._Entity.M2A

	@property
	def M1B(self) -> float:
		return self._Entity.M1B

	@property
	def M2B(self) -> float:
		return self._Entity.M2B

	@property
	def V1(self) -> float:
		return self._Entity.V1

	@property
	def V2(self) -> float:
		return self._Entity.V2

	@property
	def Axial(self) -> float:
		return self._Entity.Axial

	@property
	def Torque(self) -> float:
		return self._Entity.Torque

	@M1A.setter
	def M1A(self, value: float) -> None:
		self._Entity.M1A = value

	@M2A.setter
	def M2A(self, value: float) -> None:
		self._Entity.M2A = value

	@M1B.setter
	def M1B(self, value: float) -> None:
		self._Entity.M1B = value

	@M2B.setter
	def M2B(self, value: float) -> None:
		self._Entity.M2B = value

	@V1.setter
	def V1(self, value: float) -> None:
		self._Entity.V1 = value

	@V2.setter
	def V2(self, value: float) -> None:
		self._Entity.V2 = value

	@Axial.setter
	def Axial(self, value: float) -> None:
		self._Entity.Axial = value

	@Torque.setter
	def Torque(self, value: float) -> None:
		self._Entity.Torque = value


class LoadPropertyUserFeaBeamRow(LoadPropertyUserBeamRow):
	def __init__(self, loadPropertyUserFeaBeamRow: _api.LoadPropertyUserFeaBeamRow):
		self._Entity = loadPropertyUserFeaBeamRow

	def SetName(self, name: str) -> None:
		'''
		Set the name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserFeaBeamRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserFeaBeamRowBulkUpdater: _api.LoadPropertyUserFeaBeamRowBulkUpdater):
		self._Entity = loadPropertyUserFeaBeamRowBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserFeaBeamRow]) -> LoadPropertyUserFeaBeamRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserFeaBeamRow]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserFeaBeamRowBulkUpdater(_api.LoadPropertyUserFeaBeamRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserPanelJointRow(LoadPropertyUserRow):
	def __init__(self, loadPropertyUserPanelJointRow: _api.LoadPropertyUserPanelJointRow):
		self._Entity = loadPropertyUserPanelJointRow

	@property
	def Nx(self) -> float:
		return self._Entity.Nx

	@property
	def Ny(self) -> float:
		return self._Entity.Ny

	@property
	def Nxy(self) -> float:
		return self._Entity.Nxy

	@property
	def Mx(self) -> float:
		return self._Entity.Mx

	@property
	def My(self) -> float:
		return self._Entity.My

	@property
	def Mxy(self) -> float:
		return self._Entity.Mxy

	@property
	def Qx(self) -> float:
		return self._Entity.Qx

	@property
	def Qy(self) -> float:
		return self._Entity.Qy

	@Nx.setter
	def Nx(self, value: float) -> None:
		self._Entity.Nx = value

	@Ny.setter
	def Ny(self, value: float) -> None:
		self._Entity.Ny = value

	@Nxy.setter
	def Nxy(self, value: float) -> None:
		self._Entity.Nxy = value

	@Mx.setter
	def Mx(self, value: float) -> None:
		self._Entity.Mx = value

	@My.setter
	def My(self, value: float) -> None:
		self._Entity.My = value

	@Mxy.setter
	def Mxy(self, value: float) -> None:
		self._Entity.Mxy = value

	@Qx.setter
	def Qx(self, value: float) -> None:
		self._Entity.Qx = value

	@Qy.setter
	def Qy(self, value: float) -> None:
		self._Entity.Qy = value


class LoadPropertyUserFeaJointRow(LoadPropertyUserPanelJointRow):
	def __init__(self, loadPropertyUserFeaJointRow: _api.LoadPropertyUserFeaJointRow):
		self._Entity = loadPropertyUserFeaJointRow

	def SetName(self, name: str) -> None:
		'''
		Set the name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserFeaJointRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserFeaJointRowBulkUpdater: _api.LoadPropertyUserFeaJointRowBulkUpdater):
		self._Entity = loadPropertyUserFeaJointRowBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserFeaJointRow]) -> LoadPropertyUserFeaJointRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserFeaJointRow]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserFeaJointRowBulkUpdater(_api.LoadPropertyUserFeaJointRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserFeaPanelRow(LoadPropertyUserPanelJointRow):
	def __init__(self, loadPropertyUserFeaPanelRow: _api.LoadPropertyUserFeaPanelRow):
		self._Entity = loadPropertyUserFeaPanelRow

	def SetName(self, name: str) -> None:
		'''
		Set the name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserFeaPanelRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserFeaPanelRowBulkUpdater: _api.LoadPropertyUserFeaPanelRowBulkUpdater):
		self._Entity = loadPropertyUserFeaPanelRowBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserFeaPanelRow]) -> LoadPropertyUserFeaPanelRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserFeaPanelRow]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserFeaPanelRowBulkUpdater(_api.LoadPropertyUserFeaPanelRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserGeneralBeamRow(LoadPropertyUserBeamRow):
	def __init__(self, loadPropertyUserGeneralBeamRow: _api.LoadPropertyUserGeneralBeamRow):
		self._Entity = loadPropertyUserGeneralBeamRow

	@property
	def M1A(self) -> float:
		return self._Entity.M1A

	@property
	def M2A(self) -> float:
		return self._Entity.M2A

	@property
	def M1B(self) -> float:
		return self._Entity.M1B

	@property
	def M2B(self) -> float:
		return self._Entity.M2B

	@property
	def V1(self) -> float:
		return self._Entity.V1

	@property
	def V2(self) -> float:
		return self._Entity.V2

	@property
	def Axial(self) -> float:
		return self._Entity.Axial

	@property
	def Torque(self) -> float:
		return self._Entity.Torque

	@property
	def M1AType(self) -> types.BoundaryConditionType:
		result = self._Entity.M1AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2AType(self) -> types.BoundaryConditionType:
		result = self._Entity.M2AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M1BType(self) -> types.BoundaryConditionType:
		result = self._Entity.M1BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2BType(self) -> types.BoundaryConditionType:
		result = self._Entity.M2BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V1Type(self) -> types.BoundaryConditionType:
		result = self._Entity.V1Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V2Type(self) -> types.BoundaryConditionType:
		result = self._Entity.V2Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def AxialType(self) -> types.BoundaryConditionType:
		result = self._Entity.AxialType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def TorqueType(self) -> types.BoundaryConditionType:
		result = self._Entity.TorqueType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@M1A.setter
	def M1A(self, value: float) -> None:
		self._Entity.M1A = value

	@M2A.setter
	def M2A(self, value: float) -> None:
		self._Entity.M2A = value

	@M1B.setter
	def M1B(self, value: float) -> None:
		self._Entity.M1B = value

	@M2B.setter
	def M2B(self, value: float) -> None:
		self._Entity.M2B = value

	@V1.setter
	def V1(self, value: float) -> None:
		self._Entity.V1 = value

	@V2.setter
	def V2(self, value: float) -> None:
		self._Entity.V2 = value

	@Axial.setter
	def Axial(self, value: float) -> None:
		self._Entity.Axial = value

	@Torque.setter
	def Torque(self, value: float) -> None:
		self._Entity.Torque = value


class LoadPropertyUserGeneralBeamRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserGeneralBeamRowBulkUpdater: _api.LoadPropertyUserGeneralBeamRowBulkUpdater):
		self._Entity = loadPropertyUserGeneralBeamRowBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserGeneralBeamRow]) -> LoadPropertyUserGeneralBeamRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserGeneralBeamRow]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserGeneralBeamRowBulkUpdater(_api.LoadPropertyUserGeneralBeamRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyUserGeneralPanelRow(LoadPropertyUserPanelJointRow):
	def __init__(self, loadPropertyUserGeneralPanelRow: _api.LoadPropertyUserGeneralPanelRow):
		self._Entity = loadPropertyUserGeneralPanelRow

	@property
	def Nx(self) -> float:
		return self._Entity.Nx

	@property
	def Ny(self) -> float:
		return self._Entity.Ny

	@property
	def Nxy(self) -> float:
		return self._Entity.Nxy

	@property
	def Mx(self) -> float:
		return self._Entity.Mx

	@property
	def My(self) -> float:
		return self._Entity.My

	@property
	def Mxy(self) -> float:
		return self._Entity.Mxy

	@property
	def Qx(self) -> float:
		return self._Entity.Qx

	@property
	def Qy(self) -> float:
		return self._Entity.Qy

	@property
	def NxType(self) -> types.BoundaryConditionType:
		result = self._Entity.NxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NyType(self) -> types.BoundaryConditionType:
		result = self._Entity.NyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NxyType(self) -> types.BoundaryConditionType:
		result = self._Entity.NxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxType(self) -> types.BoundaryConditionType:
		result = self._Entity.MxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MyType(self) -> types.BoundaryConditionType:
		result = self._Entity.MyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxyType(self) -> types.BoundaryConditionType:
		result = self._Entity.MxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QxType(self) -> types.BoundaryConditionType:
		result = self._Entity.QxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QyType(self) -> types.BoundaryConditionType:
		result = self._Entity.QyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@Nx.setter
	def Nx(self, value: float) -> None:
		self._Entity.Nx = value

	@Ny.setter
	def Ny(self, value: float) -> None:
		self._Entity.Ny = value

	@Nxy.setter
	def Nxy(self, value: float) -> None:
		self._Entity.Nxy = value

	@Mx.setter
	def Mx(self, value: float) -> None:
		self._Entity.Mx = value

	@My.setter
	def My(self, value: float) -> None:
		self._Entity.My = value

	@Mxy.setter
	def Mxy(self, value: float) -> None:
		self._Entity.Mxy = value

	@Qx.setter
	def Qx(self, value: float) -> None:
		self._Entity.Qx = value

	@Qy.setter
	def Qy(self, value: float) -> None:
		self._Entity.Qy = value


class LoadPropertyUserGeneralPanelRowBulkUpdater(LoadPropertyUserRowBulkUpdater):
	def __init__(self, loadPropertyUserGeneralPanelRowBulkUpdater: _api.LoadPropertyUserGeneralPanelRowBulkUpdater):
		self._Entity = loadPropertyUserGeneralPanelRowBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[LoadPropertyUserGeneralPanelRow]) -> LoadPropertyUserGeneralPanelRowBulkUpdater:
		itemsList = List[_api.LoadPropertyUserGeneralPanelRow]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return LoadPropertyUserGeneralPanelRowBulkUpdater(_api.LoadPropertyUserGeneralPanelRowBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class LoadPropertyFea(LoadProperty):
	def __init__(self, loadPropertyFea: _api.LoadPropertyFea):
		self._Entity = loadPropertyFea

	@property
	def HasNx(self) -> bool:
		return self._Entity.HasNx

	@property
	def HasNy(self) -> bool:
		return self._Entity.HasNy

	@property
	def HasNxy(self) -> bool:
		return self._Entity.HasNxy

	@property
	def HasMx(self) -> bool:
		return self._Entity.HasMx

	@property
	def HasMy(self) -> bool:
		return self._Entity.HasMy

	@property
	def HasMxy(self) -> bool:
		return self._Entity.HasMxy

	@property
	def HasQx(self) -> bool:
		return self._Entity.HasQx

	@property
	def HasQy(self) -> bool:
		return self._Entity.HasQy

	@property
	def HasM1a(self) -> bool:
		return self._Entity.HasM1a

	@property
	def HasM1b(self) -> bool:
		return self._Entity.HasM1b

	@property
	def M2a(self) -> bool:
		return self._Entity.M2a

	@property
	def V1(self) -> bool:
		return self._Entity.V1

	@property
	def V2(self) -> bool:
		return self._Entity.V2

	@property
	def Axial(self) -> bool:
		return self._Entity.Axial

	@property
	def Torque(self) -> bool:
		return self._Entity.Torque

	@property
	def Tension(self) -> bool:
		return self._Entity.Tension

	@property
	def Shear(self) -> bool:
		return self._Entity.Shear

	@property
	def Moment(self) -> bool:
		return self._Entity.Moment

	@HasNx.setter
	def HasNx(self, value: bool) -> None:
		self._Entity.HasNx = value

	@HasNy.setter
	def HasNy(self, value: bool) -> None:
		self._Entity.HasNy = value

	@HasNxy.setter
	def HasNxy(self, value: bool) -> None:
		self._Entity.HasNxy = value

	@HasMx.setter
	def HasMx(self, value: bool) -> None:
		self._Entity.HasMx = value

	@HasMy.setter
	def HasMy(self, value: bool) -> None:
		self._Entity.HasMy = value

	@HasMxy.setter
	def HasMxy(self, value: bool) -> None:
		self._Entity.HasMxy = value

	@HasQx.setter
	def HasQx(self, value: bool) -> None:
		self._Entity.HasQx = value

	@HasQy.setter
	def HasQy(self, value: bool) -> None:
		self._Entity.HasQy = value

	@HasM1a.setter
	def HasM1a(self, value: bool) -> None:
		self._Entity.HasM1a = value

	@HasM1b.setter
	def HasM1b(self, value: bool) -> None:
		self._Entity.HasM1b = value

	@M2a.setter
	def M2a(self, value: bool) -> None:
		self._Entity.M2a = value

	@V1.setter
	def V1(self, value: bool) -> None:
		self._Entity.V1 = value

	@V2.setter
	def V2(self, value: bool) -> None:
		self._Entity.V2 = value

	@Axial.setter
	def Axial(self, value: bool) -> None:
		self._Entity.Axial = value

	@Torque.setter
	def Torque(self, value: bool) -> None:
		self._Entity.Torque = value

	@Tension.setter
	def Tension(self, value: bool) -> None:
		self._Entity.Tension = value

	@Shear.setter
	def Shear(self, value: bool) -> None:
		self._Entity.Shear = value

	@Moment.setter
	def Moment(self, value: bool) -> None:
		self._Entity.Moment = value


class LoadPropertyAverage(LoadPropertyFea):
	def __init__(self, loadPropertyAverage: _api.LoadPropertyAverage):
		self._Entity = loadPropertyAverage

	@property
	def ElementType(self) -> types.LoadPropertyAverageElementType:
		result = self._Entity.ElementType
		return types.LoadPropertyAverageElementType[result.ToString()] if result is not None else None

	@ElementType.setter
	def ElementType(self, value: types.LoadPropertyAverageElementType) -> None:
		self._Entity.ElementType = _types.LoadPropertyAverageElementType(value.value)


class LoadPropertyElementBased(LoadPropertyFea):
	def __init__(self, loadPropertyElementBased: _api.LoadPropertyElementBased):
		self._Entity = loadPropertyElementBased


class LoadPropertyNeighborAverage(LoadPropertyFea):
	def __init__(self, loadPropertyNeighborAverage: _api.LoadPropertyNeighborAverage):
		self._Entity = loadPropertyNeighborAverage

	@property
	def NumberOfNeighborsPerSide(self) -> int:
		return self._Entity.NumberOfNeighborsPerSide

	@NumberOfNeighborsPerSide.setter
	def NumberOfNeighborsPerSide(self, value: int) -> None:
		self._Entity.NumberOfNeighborsPerSide = value


class LoadPropertyPeakLoad(LoadPropertyFea):
	def __init__(self, loadPropertyPeakLoad: _api.LoadPropertyPeakLoad):
		self._Entity = loadPropertyPeakLoad

	@property
	def ElementScope(self) -> types.LoadPropertyPeakElementScope:
		result = self._Entity.ElementScope
		return types.LoadPropertyPeakElementScope[result.ToString()] if result is not None else None

	@ElementScope.setter
	def ElementScope(self, value: types.LoadPropertyPeakElementScope) -> None:
		self._Entity.ElementScope = _types.LoadPropertyPeakElementScope(value.value)


class LoadPropertyStatistical(LoadPropertyFea):
	def __init__(self, loadPropertyStatistical: _api.LoadPropertyStatistical):
		self._Entity = loadPropertyStatistical

	@property
	def NSigma(self) -> int:
		return self._Entity.NSigma

	@NSigma.setter
	def NSigma(self, value: int) -> None:
		self._Entity.NSigma = value


class LoadPropertyUserFeaRowCol(IdNameEntityCol, Generic[T]):
	def __init__(self, loadPropertyUserFeaRowCol: _api.LoadPropertyUserFeaRowCol):
		self._Entity = loadPropertyUserFeaRowCol
		self._CollectedClass = T

	@property
	def LoadPropertyUserFeaRowColList(self) -> tuple[T]:
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = T
		for subclass in T.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(loadPropertyUserFeaRowCol) for loadPropertyUserFeaRowCol in self._Entity])

	def AddScenario(self, name: str = None) -> LoadPropertyUserRow:
		'''
		Adds a load scenario with default values.
		'''
		return self._Entity.AddScenario(name)

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool: ...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadPropertyUserRow: ...

	@overload
	def Get(self, id: int) -> LoadPropertyUserRow: ...

	def DeleteScenario(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return self._Entity.DeleteScenario(item1)

		if isinstance(item1, str):
			return self._Entity.DeleteScenario(item1)

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserRow:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.LoadPropertyUserFeaRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserFeaRowColList

	def __len__(self):
		return len(self.LoadPropertyUserFeaRowColList)


class LoadPropertyUserFeaBeamRowCol(LoadPropertyUserFeaRowCol[LoadPropertyUserFeaBeamRow]):
	def __init__(self, loadPropertyUserFeaBeamRowCol: _api.LoadPropertyUserFeaBeamRowCol):
		self._Entity = loadPropertyUserFeaBeamRowCol
		self._CollectedClass = LoadPropertyUserFeaBeamRow

	@property
	def LoadPropertyUserFeaBeamRowColList(self) -> tuple[LoadPropertyUserFeaBeamRow]:
		return tuple([LoadPropertyUserFeaBeamRow(loadPropertyUserFeaBeamRowCol) for loadPropertyUserFeaBeamRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool: ...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadPropertyUserFeaBeamRow: ...

	@overload
	def Get(self, id: int) -> LoadPropertyUserFeaBeamRow: ...

	def DeleteScenario(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserFeaBeamRow:
		if isinstance(item1, str):
			return LoadPropertyUserFeaBeamRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserFeaBeamRow(super().Get(item1))

		return LoadPropertyUserFeaBeamRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserFeaBeamRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserFeaBeamRowColList

	def __len__(self):
		return len(self.LoadPropertyUserFeaBeamRowColList)


class LoadPropertyUserFeaBeam(LoadProperty):
	def __init__(self, loadPropertyUserFeaBeam: _api.LoadPropertyUserFeaBeam):
		self._Entity = loadPropertyUserFeaBeam

	@property
	def UserFeaRows(self) -> LoadPropertyUserFeaBeamRowCol:
		result = self._Entity.UserFeaRows
		return LoadPropertyUserFeaBeamRowCol(result) if result is not None else None


class LoadPropertyUserFeaJointRowCol(LoadPropertyUserFeaRowCol[LoadPropertyUserFeaJointRow]):
	def __init__(self, loadPropertyUserFeaJointRowCol: _api.LoadPropertyUserFeaJointRowCol):
		self._Entity = loadPropertyUserFeaJointRowCol
		self._CollectedClass = LoadPropertyUserFeaJointRow

	@property
	def LoadPropertyUserFeaJointRowColList(self) -> tuple[LoadPropertyUserFeaJointRow]:
		return tuple([LoadPropertyUserFeaJointRow(loadPropertyUserFeaJointRowCol) for loadPropertyUserFeaJointRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool: ...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadPropertyUserFeaJointRow: ...

	@overload
	def Get(self, id: int) -> LoadPropertyUserFeaJointRow: ...

	def DeleteScenario(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserFeaJointRow:
		if isinstance(item1, str):
			return LoadPropertyUserFeaJointRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserFeaJointRow(super().Get(item1))

		return LoadPropertyUserFeaJointRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserFeaJointRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserFeaJointRowColList

	def __len__(self):
		return len(self.LoadPropertyUserFeaJointRowColList)


class LoadPropertyUserFeaJoint(LoadProperty):
	def __init__(self, loadPropertyUserFeaJoint: _api.LoadPropertyUserFeaJoint):
		self._Entity = loadPropertyUserFeaJoint

	@property
	def UserFeaRows(self) -> LoadPropertyUserFeaJointRowCol:
		result = self._Entity.UserFeaRows
		return LoadPropertyUserFeaJointRowCol(result) if result is not None else None


class LoadPropertyUserFeaPanelRowCol(LoadPropertyUserFeaRowCol[LoadPropertyUserFeaPanelRow]):
	def __init__(self, loadPropertyUserFeaPanelRowCol: _api.LoadPropertyUserFeaPanelRowCol):
		self._Entity = loadPropertyUserFeaPanelRowCol
		self._CollectedClass = LoadPropertyUserFeaPanelRow

	@property
	def LoadPropertyUserFeaPanelRowColList(self) -> tuple[LoadPropertyUserFeaPanelRow]:
		return tuple([LoadPropertyUserFeaPanelRow(loadPropertyUserFeaPanelRowCol) for loadPropertyUserFeaPanelRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool: ...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadPropertyUserFeaPanelRow: ...

	@overload
	def Get(self, id: int) -> LoadPropertyUserFeaPanelRow: ...

	def DeleteScenario(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserFeaPanelRow:
		if isinstance(item1, str):
			return LoadPropertyUserFeaPanelRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserFeaPanelRow(super().Get(item1))

		return LoadPropertyUserFeaPanelRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserFeaPanelRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserFeaPanelRowColList

	def __len__(self):
		return len(self.LoadPropertyUserFeaPanelRowColList)


class LoadPropertyUserFeaPanel(LoadProperty):
	def __init__(self, loadPropertyUserFeaPanel: _api.LoadPropertyUserFeaPanel):
		self._Entity = loadPropertyUserFeaPanel

	@property
	def UserFeaRows(self) -> LoadPropertyUserFeaPanelRowCol:
		result = self._Entity.UserFeaRows
		return LoadPropertyUserFeaPanelRowCol(result) if result is not None else None

	def SetIsZeroCurvature(self, isZeroCurvature: bool) -> None:
		'''
		Is there an enum for this?
		'''
		return self._Entity.SetIsZeroCurvature(isZeroCurvature)


class LoadPropertyUserGeneralDoubleRow(IdNameEntity):
	def __init__(self, loadPropertyUserGeneralDoubleRow: _api.LoadPropertyUserGeneralDoubleRow):
		self._Entity = loadPropertyUserGeneralDoubleRow

	@property
	def MechanicalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.MechanicalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in LoadPropertyUserRow.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def ThermalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.ThermalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in LoadPropertyUserRow.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	def SetName(self, name: str) -> None:
		'''
		Update name for the scenario
		'''
		return self._Entity.SetName(name)


class LoadPropertyUserGeneralBeamDoubleRow(LoadPropertyUserGeneralDoubleRow):
	def __init__(self, loadPropertyUserGeneralBeamDoubleRow: _api.LoadPropertyUserGeneralBeamDoubleRow):
		self._Entity = loadPropertyUserGeneralBeamDoubleRow

	@property
	def MechanicalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.MechanicalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in LoadPropertyUserRow.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def ThermalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.ThermalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in LoadPropertyUserRow.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def M1AType(self) -> types.BoundaryConditionType:
		result = self._Entity.M1AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2AType(self) -> types.BoundaryConditionType:
		result = self._Entity.M2AType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M1BType(self) -> types.BoundaryConditionType:
		result = self._Entity.M1BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def M2BType(self) -> types.BoundaryConditionType:
		result = self._Entity.M2BType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V1Type(self) -> types.BoundaryConditionType:
		result = self._Entity.V1Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def V2Type(self) -> types.BoundaryConditionType:
		result = self._Entity.V2Type
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def AxialType(self) -> types.BoundaryConditionType:
		result = self._Entity.AxialType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def TorqueType(self) -> types.BoundaryConditionType:
		result = self._Entity.TorqueType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	def SetM1AType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M1A type for the scenario
		'''
		return self._Entity.SetM1AType(_types.BoundaryConditionType(type.value))

	def SetM2AType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M2A type for the scenario
		'''
		return self._Entity.SetM2AType(_types.BoundaryConditionType(type.value))

	def SetM1BType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M1B type for the scenario
		'''
		return self._Entity.SetM1BType(_types.BoundaryConditionType(type.value))

	def SetM2BType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set M2B type for the scenario
		'''
		return self._Entity.SetM2BType(_types.BoundaryConditionType(type.value))

	def SetV1Type(self, type: types.BoundaryConditionType) -> None:
		'''
		Set V1 type for the scenario
		'''
		return self._Entity.SetV1Type(_types.BoundaryConditionType(type.value))

	def SetV2Type(self, type: types.BoundaryConditionType) -> None:
		'''
		Set V2 type for the scenario
		'''
		return self._Entity.SetV2Type(_types.BoundaryConditionType(type.value))

	def SetAxialType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Axial type for the scenario
		'''
		return self._Entity.SetAxialType(_types.BoundaryConditionType(type.value))

	def SetTorqueType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set torque type for the scenario
		'''
		return self._Entity.SetTorqueType(_types.BoundaryConditionType(type.value))


class LoadPropertyUserGeneralRowCol(IdNameEntityCol, Generic[T]):
	def __init__(self, loadPropertyUserGeneralRowCol: _api.LoadPropertyUserGeneralRowCol):
		self._Entity = loadPropertyUserGeneralRowCol
		self._CollectedClass = T

	@property
	def LoadPropertyUserGeneralRowColList(self) -> tuple[T]:
		if self._Entity.Count() <= 0:
			return ()
		thisClass = type(self._Entity._items[0]).__name__
		givenClass = T
		for subclass in T.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return tuple([givenClass(loadPropertyUserGeneralRowCol) for loadPropertyUserGeneralRowCol in self._Entity])

	def AddScenario(self, name: str = None) -> LoadPropertyUserGeneralDoubleRow:
		'''
		Add scenario.
		'''
		return self._Entity.AddScenario(name)

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool: ...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadPropertyUserGeneralDoubleRow: ...

	@overload
	def Get(self, id: int) -> LoadPropertyUserGeneralDoubleRow: ...

	def DeleteScenario(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return self._Entity.DeleteScenario(item1)

		if isinstance(item1, str):
			return self._Entity.DeleteScenario(item1)

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserGeneralDoubleRow:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

		return self._Entity.Get(item1)

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralRowColList)


class LoadPropertyUserGeneralBeamRowCol(LoadPropertyUserGeneralRowCol[LoadPropertyUserGeneralBeamDoubleRow]):
	def __init__(self, loadPropertyUserGeneralBeamRowCol: _api.LoadPropertyUserGeneralBeamRowCol):
		self._Entity = loadPropertyUserGeneralBeamRowCol
		self._CollectedClass = LoadPropertyUserGeneralBeamDoubleRow

	@property
	def LoadPropertyUserGeneralBeamRowColList(self) -> tuple[LoadPropertyUserGeneralBeamDoubleRow]:
		return tuple([LoadPropertyUserGeneralBeamDoubleRow(loadPropertyUserGeneralBeamRowCol) for loadPropertyUserGeneralBeamRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool: ...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadPropertyUserGeneralBeamDoubleRow: ...

	@overload
	def Get(self, id: int) -> LoadPropertyUserGeneralBeamDoubleRow: ...

	def DeleteScenario(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserGeneralBeamDoubleRow:
		if isinstance(item1, str):
			return LoadPropertyUserGeneralBeamDoubleRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserGeneralBeamDoubleRow(super().Get(item1))

		return LoadPropertyUserGeneralBeamDoubleRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralBeamRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralBeamRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralBeamRowColList)


class LoadPropertyUserGeneralBeam(LoadProperty):
	def __init__(self, loadPropertyUserGeneralBeam: _api.LoadPropertyUserGeneralBeam):
		self._Entity = loadPropertyUserGeneralBeam

	@property
	def UserGeneralRows(self) -> LoadPropertyUserGeneralBeamRowCol:
		result = self._Entity.UserGeneralRows
		return LoadPropertyUserGeneralBeamRowCol(result) if result is not None else None

	@property
	def IsIncludingThermal(self) -> bool:
		return self._Entity.IsIncludingThermal

	@IsIncludingThermal.setter
	def IsIncludingThermal(self, value: bool) -> None:
		self._Entity.IsIncludingThermal = value


class LoadPropertyUserGeneralBoltedRow(IdEntity):
	def __init__(self, loadPropertyUserGeneralBoltedRow: _api.LoadPropertyUserGeneralBoltedRow):
		self._Entity = loadPropertyUserGeneralBoltedRow

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def LoadScenarioId(self) -> int:
		return self._Entity.LoadScenarioId

	@property
	def Fx(self) -> float:
		return self._Entity.Fx

	@property
	def Fy(self) -> float:
		return self._Entity.Fy

	@property
	def Fz(self) -> float:
		return self._Entity.Fz

	@property
	def Mx(self) -> float:
		return self._Entity.Mx

	@property
	def My(self) -> float:
		return self._Entity.My

	@property
	def Mz(self) -> float:
		return self._Entity.Mz

	@property
	def NxBypass(self) -> float:
		return self._Entity.NxBypass

	@property
	def NyBypass(self) -> float:
		return self._Entity.NyBypass

	@property
	def NxyBypass(self) -> float:
		return self._Entity.NxyBypass

	@property
	def LimitFactor(self) -> float:
		return self._Entity.LimitFactor

	@property
	def UltimateFactor(self) -> float:
		return self._Entity.UltimateFactor

	@Fx.setter
	def Fx(self, value: float) -> None:
		self._Entity.Fx = value

	@Fy.setter
	def Fy(self, value: float) -> None:
		self._Entity.Fy = value

	@Fz.setter
	def Fz(self, value: float) -> None:
		self._Entity.Fz = value

	@Mx.setter
	def Mx(self, value: float) -> None:
		self._Entity.Mx = value

	@My.setter
	def My(self, value: float) -> None:
		self._Entity.My = value

	@Mz.setter
	def Mz(self, value: float) -> None:
		self._Entity.Mz = value

	@NxBypass.setter
	def NxBypass(self, value: float) -> None:
		self._Entity.NxBypass = value

	@NyBypass.setter
	def NyBypass(self, value: float) -> None:
		self._Entity.NyBypass = value

	@NxyBypass.setter
	def NxyBypass(self, value: float) -> None:
		self._Entity.NxyBypass = value

	@LimitFactor.setter
	def LimitFactor(self, value: float) -> None:
		self._Entity.LimitFactor = value

	@UltimateFactor.setter
	def UltimateFactor(self, value: float) -> None:
		self._Entity.UltimateFactor = value


class LoadPropertyUserGeneralBoltedRowCol(IdEntityCol[LoadPropertyUserGeneralBoltedRow]):
	def __init__(self, loadPropertyUserGeneralBoltedRowCol: _api.LoadPropertyUserGeneralBoltedRowCol):
		self._Entity = loadPropertyUserGeneralBoltedRowCol
		self._CollectedClass = LoadPropertyUserGeneralBoltedRow

	@property
	def LoadPropertyUserGeneralBoltedRowColList(self) -> tuple[LoadPropertyUserGeneralBoltedRow]:
		return tuple([LoadPropertyUserGeneralBoltedRow(loadPropertyUserGeneralBoltedRowCol) for loadPropertyUserGeneralBoltedRowCol in self._Entity])

	def AddScenario(self) -> None:
		'''
		Adds a load scenario with default values
		'''
		return self._Entity.AddScenario()

	def DeleteScenario(self, scenarioId: int) -> bool:
		'''
		Delete a load scenario by id
		'''
		return self._Entity.DeleteScenario(scenarioId)

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralBoltedRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralBoltedRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralBoltedRowColList)


class LoadPropertyUserGeneralBolted(LoadProperty):
	def __init__(self, loadPropertyUserGeneralBolted: _api.LoadPropertyUserGeneralBolted):
		self._Entity = loadPropertyUserGeneralBolted

	@property
	def UserGeneralBoltedRows(self) -> LoadPropertyUserGeneralBoltedRowCol:
		result = self._Entity.UserGeneralBoltedRows
		return LoadPropertyUserGeneralBoltedRowCol(result) if result is not None else None


class LoadPropertyUserGeneralBondedRow(IdEntity):
	def __init__(self, loadPropertyUserGeneralBondedRow: _api.LoadPropertyUserGeneralBondedRow):
		self._Entity = loadPropertyUserGeneralBondedRow

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def JointConceptId(self) -> types.JointConceptId:
		result = self._Entity.JointConceptId
		return types.JointConceptId[result.ToString()] if result is not None else None

	@property
	def BondedBcId(self) -> int:
		return self._Entity.BondedBcId

	@property
	def AxialType(self) -> types.BoundaryConditionType:
		result = self._Entity.AxialType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MomentType(self) -> types.BoundaryConditionType:
		result = self._Entity.MomentType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def TransverseType(self) -> types.BoundaryConditionType:
		result = self._Entity.TransverseType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def ShearType(self) -> types.BoundaryConditionType:
		result = self._Entity.ShearType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def Axial(self) -> float:
		return self._Entity.Axial

	@property
	def Moment(self) -> float:
		return self._Entity.Moment

	@property
	def Transverse(self) -> float:
		return self._Entity.Transverse

	@property
	def Shear(self) -> float:
		return self._Entity.Shear

	@AxialType.setter
	def AxialType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.AxialType = _types.BoundaryConditionType(value.value)

	@MomentType.setter
	def MomentType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.MomentType = _types.BoundaryConditionType(value.value)

	@TransverseType.setter
	def TransverseType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.TransverseType = _types.BoundaryConditionType(value.value)

	@ShearType.setter
	def ShearType(self, value: types.BoundaryConditionType) -> None:
		self._Entity.ShearType = _types.BoundaryConditionType(value.value)

	@Axial.setter
	def Axial(self, value: float) -> None:
		self._Entity.Axial = value

	@Moment.setter
	def Moment(self, value: float) -> None:
		self._Entity.Moment = value

	@Transverse.setter
	def Transverse(self, value: float) -> None:
		self._Entity.Transverse = value

	@Shear.setter
	def Shear(self, value: float) -> None:
		self._Entity.Shear = value

	def UpdateRow(self) -> None:
		return self._Entity.UpdateRow()


class LoadPropertyUserGeneralBondedRowCol(IdEntityCol[LoadPropertyUserGeneralBondedRow]):
	def __init__(self, loadPropertyUserGeneralBondedRowCol: _api.LoadPropertyUserGeneralBondedRowCol):
		self._Entity = loadPropertyUserGeneralBondedRowCol
		self._CollectedClass = LoadPropertyUserGeneralBondedRow

	@property
	def LoadPropertyUserGeneralBondedRowColList(self) -> tuple[LoadPropertyUserGeneralBondedRow]:
		return tuple([LoadPropertyUserGeneralBondedRow(loadPropertyUserGeneralBondedRowCol) for loadPropertyUserGeneralBondedRowCol in self._Entity])

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralBondedRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralBondedRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralBondedRowColList)


class LoadPropertyJoint(IdEntity):
	def __init__(self, loadPropertyJoint: _api.LoadPropertyJoint):
		self._Entity = loadPropertyJoint

	@property
	def UserGeneralBondedRows(self) -> LoadPropertyUserGeneralBondedRowCol:
		result = self._Entity.UserGeneralBondedRows
		return LoadPropertyUserGeneralBondedRowCol(result) if result is not None else None

	@property
	def LoadPropertyId(self) -> int:
		return self._Entity.LoadPropertyId

	@property
	def JConceptId(self) -> types.JointConceptId:
		result = self._Entity.JConceptId
		return types.JointConceptId[result.ToString()] if result is not None else None

	@property
	def Ex(self) -> float:
		return self._Entity.Ex

	@property
	def Kx(self) -> float:
		return self._Entity.Kx

	@property
	def Kxy(self) -> float:
		return self._Entity.Kxy

	@property
	def Temperature(self) -> float:
		return self._Entity.Temperature

	@JConceptId.setter
	def JConceptId(self, value: types.JointConceptId) -> None:
		self._Entity.JConceptId = _types.JointConceptId(value.value)

	@Ex.setter
	def Ex(self, value: float) -> None:
		self._Entity.Ex = value

	@Kx.setter
	def Kx(self, value: float) -> None:
		self._Entity.Kx = value

	@Kxy.setter
	def Kxy(self, value: float) -> None:
		self._Entity.Kxy = value

	@Temperature.setter
	def Temperature(self, value: float) -> None:
		self._Entity.Temperature = value


class LoadPropertyUserGeneralBonded(LoadProperty):
	def __init__(self, loadPropertyUserGeneralBonded: _api.LoadPropertyUserGeneralBonded):
		self._Entity = loadPropertyUserGeneralBonded

	@property
	def LoadPropertyJoint(self) -> LoadPropertyJoint:
		result = self._Entity.LoadPropertyJoint
		return LoadPropertyJoint(result) if result is not None else None


class LoadPropertyUserGeneralPanelDoubleRow(LoadPropertyUserGeneralDoubleRow):
	def __init__(self, loadPropertyUserGeneralPanelDoubleRow: _api.LoadPropertyUserGeneralPanelDoubleRow):
		self._Entity = loadPropertyUserGeneralPanelDoubleRow

	@property
	def MechanicalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.MechanicalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in LoadPropertyUserRow.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def ThermalRow(self) -> LoadPropertyUserRow:
		result = self._Entity.ThermalRow
		thisClass = type(result).__name__
		givenClass = LoadPropertyUserRow
		for subclass in LoadPropertyUserRow.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(result) if result is not None else None

	@property
	def NxType(self) -> types.BoundaryConditionType:
		result = self._Entity.NxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NyType(self) -> types.BoundaryConditionType:
		result = self._Entity.NyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def NxyType(self) -> types.BoundaryConditionType:
		result = self._Entity.NxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxType(self) -> types.BoundaryConditionType:
		result = self._Entity.MxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MyType(self) -> types.BoundaryConditionType:
		result = self._Entity.MyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def MxyType(self) -> types.BoundaryConditionType:
		result = self._Entity.MxyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QxType(self) -> types.BoundaryConditionType:
		result = self._Entity.QxType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	@property
	def QyType(self) -> types.BoundaryConditionType:
		result = self._Entity.QyType
		return types.BoundaryConditionType[result.ToString()] if result is not None else None

	def SetNxType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Nx type for the scenario
		'''
		return self._Entity.SetNxType(_types.BoundaryConditionType(type.value))

	def SetNyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Ny type for the scenario
		'''
		return self._Entity.SetNyType(_types.BoundaryConditionType(type.value))

	def SetNxyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Nxy type for the scenario
		'''
		return self._Entity.SetNxyType(_types.BoundaryConditionType(type.value))

	def SetMxType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Mx type for the scenario
		'''
		return self._Entity.SetMxType(_types.BoundaryConditionType(type.value))

	def SetMyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set My type for the scenario
		'''
		return self._Entity.SetMyType(_types.BoundaryConditionType(type.value))

	def SetMxyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Mxy type for the scenario
		'''
		return self._Entity.SetMxyType(_types.BoundaryConditionType(type.value))

	def SetQxType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Qx type for the scenario
		'''
		return self._Entity.SetQxType(_types.BoundaryConditionType(type.value))

	def SetQyType(self, type: types.BoundaryConditionType) -> None:
		'''
		Set Qy type for the scenario
		'''
		return self._Entity.SetQyType(_types.BoundaryConditionType(type.value))


class LoadPropertyUserGeneralPanelRowCol(LoadPropertyUserGeneralRowCol[LoadPropertyUserGeneralPanelDoubleRow]):
	def __init__(self, loadPropertyUserGeneralPanelRowCol: _api.LoadPropertyUserGeneralPanelRowCol):
		self._Entity = loadPropertyUserGeneralPanelRowCol
		self._CollectedClass = LoadPropertyUserGeneralPanelDoubleRow

	@property
	def LoadPropertyUserGeneralPanelRowColList(self) -> tuple[LoadPropertyUserGeneralPanelDoubleRow]:
		return tuple([LoadPropertyUserGeneralPanelDoubleRow(loadPropertyUserGeneralPanelRowCol) for loadPropertyUserGeneralPanelRowCol in self._Entity])

	@overload
	def DeleteScenario(self, scenarioId: int) -> bool: ...

	@overload
	def DeleteScenario(self, scenarioName: str) -> bool: ...

	@overload
	def Get(self, name: str) -> LoadPropertyUserGeneralPanelDoubleRow: ...

	@overload
	def Get(self, id: int) -> LoadPropertyUserGeneralPanelDoubleRow: ...

	def DeleteScenario(self, item1 = None) -> bool:
		if isinstance(item1, int):
			return bool(super().DeleteScenario(item1))

		if isinstance(item1, str):
			return bool(super().DeleteScenario(item1))

		return self._Entity.DeleteScenario(item1)

	def Get(self, item1 = None) -> LoadPropertyUserGeneralPanelDoubleRow:
		if isinstance(item1, str):
			return LoadPropertyUserGeneralPanelDoubleRow(super().Get(item1))

		if isinstance(item1, int):
			return LoadPropertyUserGeneralPanelDoubleRow(super().Get(item1))

		return LoadPropertyUserGeneralPanelDoubleRow(self._Entity.Get(item1))

	def __getitem__(self, index: int):
		return self.LoadPropertyUserGeneralPanelRowColList[index]

	def __iter__(self):
		yield from self.LoadPropertyUserGeneralPanelRowColList

	def __len__(self):
		return len(self.LoadPropertyUserGeneralPanelRowColList)


class LoadPropertyUserGeneralPanel(LoadProperty):
	def __init__(self, loadPropertyUserGeneralPanel: _api.LoadPropertyUserGeneralPanel):
		self._Entity = loadPropertyUserGeneralPanel

	@property
	def UserGeneralRows(self) -> LoadPropertyUserGeneralPanelRowCol:
		result = self._Entity.UserGeneralRows
		return LoadPropertyUserGeneralPanelRowCol(result) if result is not None else None

	@property
	def IsIncludingThermal(self) -> bool:
		return self._Entity.IsIncludingThermal

	@IsIncludingThermal.setter
	def IsIncludingThermal(self, value: bool) -> None:
		self._Entity.IsIncludingThermal = value

	def SetIsZeroCurvature(self, isZeroCurvature: bool) -> None:
		'''
		Is there an enum for this?
		'''
		return self._Entity.SetIsZeroCurvature(isZeroCurvature)


class JointSelectionDesignResult(JointDesignResult):
	def __init__(self, jointSelectionDesignResult: _api.JointSelectionDesignResult):
		self._Entity = jointSelectionDesignResult

	@property
	def JointSelectionId(self) -> types.JointSelectionId:
		result = self._Entity.JointSelectionId
		return types.JointSelectionId[result.ToString()] if result is not None else None


class JointFastenerDesignResult(JointSelectionDesignResult):
	def __init__(self, jointFastenerDesignResult: _api.JointFastenerDesignResult):
		self._Entity = jointFastenerDesignResult

	@property
	def FastenerBoltId(self) -> int:
		return self._Entity.FastenerBoltId

	@property
	def FastenerCodeId(self) -> int:
		return self._Entity.FastenerCodeId


class JointMaterialDesignResult(JointSelectionDesignResult):
	def __init__(self, jointMaterialDesignResult: _api.JointMaterialDesignResult):
		self._Entity = jointMaterialDesignResult

	@property
	def MaterialId(self) -> int:
		return self._Entity.MaterialId

	@property
	def MaterialType(self) -> types.MaterialType:
		'''
		Represents a material's type.
		'''
		result = self._Entity.MaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Material(self) -> str:
		return self._Entity.Material


class JointRangeDesignResult(JointDesignResult):
	def __init__(self, jointRangeDesignResult: _api.JointRangeDesignResult):
		self._Entity = jointRangeDesignResult

	@property
	def JointRangeId(self) -> types.JointRangeId:
		result = self._Entity.JointRangeId
		return types.JointRangeId[result.ToString()] if result is not None else None

	@property
	def JointRangeMode(self) -> types.JointRangeMode:
		result = self._Entity.JointRangeMode
		return types.JointRangeMode[result.ToString()] if result is not None else None

	@property
	def Value(self) -> float:
		return self._Entity.Value


class JointRivetDesignResult(JointSelectionDesignResult):
	def __init__(self, jointRivetDesignResult: _api.JointRivetDesignResult):
		self._Entity = jointRivetDesignResult

	@property
	def RivetId(self) -> int:
		return self._Entity.RivetId

	@property
	def RivetDiameterId(self) -> int:
		return self._Entity.RivetDiameterId


class Environment(ABC):
	'''
	Represents HyperX's execution environment (where HyperX is installed).
	'''
	def __init__(self, environment: _api.Environment):
		self._Entity = environment

	@property
	def InstallLocation(self) -> str:
		return self._Entity.InstallLocation

	def SetLocation(location: str) -> None:
		'''
		Set the directory location of the HyperX binaries.
            * This method is *not* required for Python and IronPython client application.
            * This method is required for C# and VB.NET clients as these applications
              need HyperX.Scripting.dll alongside its binaries.
		:param location: Path to the binaries.
		'''
		return _api.Environment.SetLocation(location)

	def Initialize() -> None:
		'''
		Initialize the HyperX scripting environment.
		'''
		return _api.Environment.Initialize()


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

	def NullableSingle(input: float) -> float:
		return _api.HelperFunctions.NullableSingle(input)

	def GetFamilyObjectForObjectId(familyId: types.BeamPanelFamily, objectId: int) -> types.FamilyObjectUID:
		return types.FamilyObjectUID(_api.HelperFunctions.GetFamilyObjectForObjectId(_types.BeamPanelFamily(familyId.value), objectId))


class IBulkUpdatableEntity:
	def __init__(self, iBulkUpdatableEntity: _api.IBulkUpdatableEntity):
		self._Entity = iBulkUpdatableEntity

	pass


class LaminatePlyData:
	'''
	Per ply data for Laminate materials
	'''
	def __init__(self, laminatePlyData: _api.LaminatePlyData):
		self._Entity = laminatePlyData

	@property
	def MaterialId(self) -> int:
		return self._Entity.MaterialId

	@property
	def PlyId(self) -> int:
		return self._Entity.PlyId

	@property
	def PlyMaterialId(self) -> int:
		return self._Entity.PlyMaterialId

	@property
	def PlyMaterialType(self) -> types.MaterialType:
		'''
		Represents a material's type.
		'''
		result = self._Entity.PlyMaterialType
		return types.MaterialType[result.ToString()] if result is not None else None

	@property
	def Angle(self) -> float:
		return self._Entity.Angle

	@property
	def Thickness(self) -> float:
		return self._Entity.Thickness

	@property
	def IsFabric(self) -> bool:
		return self._Entity.IsFabric

	@property
	def FamilyPlyId(self) -> int:
		return self._Entity.FamilyPlyId

	@property
	def OriginalPlyId(self) -> int:
		return self._Entity.OriginalPlyId

	@property
	def OriginalFamilyPlyId(self) -> int:
		return self._Entity.OriginalFamilyPlyId

	@property
	def DisplaySequenceId(self) -> int:
		return self._Entity.DisplaySequenceId

	@property
	def PlyStiffenerSubType(self) -> types.PlyStiffenerSubType:
		result = self._Entity.PlyStiffenerSubType
		return types.PlyStiffenerSubType[result.ToString()] if result is not None else None

	@property
	def Object1(self) -> bool:
		return self._Entity.Object1

	@property
	def Object2(self) -> bool:
		return self._Entity.Object2

	@property
	def Object3(self) -> bool:
		return self._Entity.Object3

	@property
	def IsInverted(self) -> bool:
		return self._Entity.IsInverted

	@property
	def IsFullStructure(self) -> bool:
		return self._Entity.IsFullStructure

	@property
	def UseTrueFiberDirection(self) -> bool:
		return self._Entity.UseTrueFiberDirection

	@property
	def IsInFoot(self) -> bool:
		return self._Entity.IsInFoot

	@property
	def IsInWeb(self) -> bool:
		return self._Entity.IsInWeb

	@property
	def IsInCap(self) -> bool:
		return self._Entity.IsInCap

	def SetMaterial(self, matId: int) -> bool:
		'''
		Sets the material of a ply to the matId. This includes: PlyMaterialId and PlyMaterialType, and updates Thickness and IsFabric
		'''
		return self._Entity.SetMaterial(matId)

	def SetAngle(self, angle: float) -> bool:
		'''
		Sets the angle of a ply
		'''
		return self._Entity.SetAngle(angle)


class Beam(Zone):
	def __init__(self, beam: _api.Beam):
		self._Entity = beam

	@property
	def Length(self) -> float:
		return self._Entity.Length

	@property
	def Phi(self) -> float:
		return self._Entity.Phi

	@property
	def K1(self) -> float:
		return self._Entity.K1

	@property
	def K2(self) -> float:
		return self._Entity.K2

	@property
	def ReferencePlane(self) -> types.ReferencePlaneBeam:
		result = self._Entity.ReferencePlane
		return types.ReferencePlaneBeam[result.ToString()] if result is not None else None

	@Phi.setter
	def Phi(self, value: float) -> None:
		self._Entity.Phi = value

	@K1.setter
	def K1(self, value: float) -> None:
		self._Entity.K1 = value

	@K2.setter
	def K2(self, value: float) -> None:
		self._Entity.K2 = value

	@ReferencePlane.setter
	def ReferencePlane(self, value: types.ReferencePlaneBeam) -> None:
		self._Entity.ReferencePlane = _types.ReferencePlaneBeam(value.value)


class ZoneBulkUpdaterBase(BulkUpdaterBase):
	def __init__(self, zoneBulkUpdaterBase: _api.ZoneBulkUpdaterBase):
		self._Entity = zoneBulkUpdaterBase


class BeamBulkUpdater(ZoneBulkUpdaterBase):
	def __init__(self, beamBulkUpdater: _api.BeamBulkUpdater):
		self._Entity = beamBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[Beam]) -> BeamBulkUpdater:
		itemsList = List[_api.Beam]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return BeamBulkUpdater(_api.BeamBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class Panel(Zone):
	def __init__(self, panel: _api.Panel):
		self._Entity = panel

	@property
	def Area(self) -> float:
		return self._Entity.Area

	@property
	def ReferencePlane(self) -> types.ReferencePlanePanel:
		result = self._Entity.ReferencePlane
		return types.ReferencePlanePanel[result.ToString()] if result is not None else None

	@property
	def AddedOffset(self) -> float:
		return self._Entity.AddedOffset

	@property
	def YSpan(self) -> float:
		return self._Entity.YSpan

	@property
	def IsCurved(self) -> bool:
		return self._Entity.IsCurved

	@property
	def Radius(self) -> float:
		return self._Entity.Radius

	@property
	def IsFullCylinder(self) -> bool:
		return self._Entity.IsFullCylinder

	@property
	def BucklingMode(self) -> types.ZoneBucklingMode:
		result = self._Entity.BucklingMode
		return types.ZoneBucklingMode[result.ToString()] if result is not None else None

	@property
	def PerformLocalPostbuckling(self) -> bool:
		return self._Entity.PerformLocalPostbuckling

	@property
	def A11Required(self) -> float:
		return self._Entity.A11Required

	@property
	def A22Required(self) -> float:
		return self._Entity.A22Required

	@property
	def A33Required(self) -> float:
		return self._Entity.A33Required

	@property
	def D11Required(self) -> float:
		return self._Entity.D11Required

	@property
	def D22Required(self) -> float:
		return self._Entity.D22Required

	@property
	def D33Required(self) -> float:
		return self._Entity.D33Required

	@property
	def A11Auto(self) -> float:
		return self._Entity.A11Auto

	@property
	def A22Auto(self) -> float:
		return self._Entity.A22Auto

	@property
	def A33Auto(self) -> float:
		return self._Entity.A33Auto

	@property
	def D11Auto(self) -> float:
		return self._Entity.D11Auto

	@property
	def D22Auto(self) -> float:
		return self._Entity.D22Auto

	@property
	def D33Auto(self) -> float:
		return self._Entity.D33Auto

	@property
	def Ey(self) -> float:
		return self._Entity.Ey

	@property
	def Kx(self) -> float:
		return self._Entity.Kx

	@property
	def Ky(self) -> float:
		return self._Entity.Ky

	@property
	def HoneycombCoreAngle(self) -> float:
		return self._Entity.HoneycombCoreAngle

	@ReferencePlane.setter
	def ReferencePlane(self, value: types.ReferencePlanePanel) -> None:
		self._Entity.ReferencePlane = _types.ReferencePlanePanel(value.value)

	@AddedOffset.setter
	def AddedOffset(self, value: float) -> None:
		self._Entity.AddedOffset = value

	@YSpan.setter
	def YSpan(self, value: float) -> None:
		self._Entity.YSpan = value

	@IsCurved.setter
	def IsCurved(self, value: bool) -> None:
		self._Entity.IsCurved = value

	@Radius.setter
	def Radius(self, value: float) -> None:
		self._Entity.Radius = value

	@IsFullCylinder.setter
	def IsFullCylinder(self, value: bool) -> None:
		self._Entity.IsFullCylinder = value

	@BucklingMode.setter
	def BucklingMode(self, value: types.ZoneBucklingMode) -> None:
		self._Entity.BucklingMode = _types.ZoneBucklingMode(value.value)

	@PerformLocalPostbuckling.setter
	def PerformLocalPostbuckling(self, value: bool) -> None:
		self._Entity.PerformLocalPostbuckling = value

	@A11Required.setter
	def A11Required(self, value: float) -> None:
		self._Entity.A11Required = value

	@A22Required.setter
	def A22Required(self, value: float) -> None:
		self._Entity.A22Required = value

	@A33Required.setter
	def A33Required(self, value: float) -> None:
		self._Entity.A33Required = value

	@D11Required.setter
	def D11Required(self, value: float) -> None:
		self._Entity.D11Required = value

	@D22Required.setter
	def D22Required(self, value: float) -> None:
		self._Entity.D22Required = value

	@D33Required.setter
	def D33Required(self, value: float) -> None:
		self._Entity.D33Required = value

	@Ey.setter
	def Ey(self, value: float) -> None:
		self._Entity.Ey = value

	@Kx.setter
	def Kx(self, value: float) -> None:
		self._Entity.Kx = value

	@Ky.setter
	def Ky(self, value: float) -> None:
		self._Entity.Ky = value

	@HoneycombCoreAngle.setter
	def HoneycombCoreAngle(self, value: float) -> None:
		self._Entity.HoneycombCoreAngle = value


class PanelBulkUpdater(ZoneBulkUpdaterBase):
	def __init__(self, panelBulkUpdater: _api.PanelBulkUpdater):
		self._Entity = panelBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[Panel]) -> PanelBulkUpdater:
		itemsList = List[_api.Panel]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return PanelBulkUpdater(_api.PanelBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class PanelSegmentBulkUpdater(ZoneBulkUpdaterBase):
	def __init__(self, panelSegmentBulkUpdater: _api.PanelSegmentBulkUpdater):
		self._Entity = panelSegmentBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[PanelSegment]) -> PanelSegmentBulkUpdater:
		itemsList = List[_api.PanelSegment]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return PanelSegmentBulkUpdater(_api.PanelSegmentBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))


class ZoneBulkUpdater(ZoneBulkUpdaterBase):
	def __init__(self, zoneBulkUpdater: _api.ZoneBulkUpdater):
		self._Entity = zoneBulkUpdater

	def GetBulkUpdater(application: Application, items: tuple[Zone]) -> ZoneBulkUpdater:
		itemsList = List[_api.Zone]()
		if items is not None:
			for thing in items:
				if thing is not None:
					itemsList.Add(thing._Entity)
		itemsEnumerable = IEnumerable(itemsList)
		return ZoneBulkUpdater(_api.ZoneBulkUpdater.GetBulkUpdater(application._Entity, itemsEnumerable))

