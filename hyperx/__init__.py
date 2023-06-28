#  /_/       _  _  ( /
# / / (/ /) (- /  / )
#     / /

"""
HyperX Scripting Library
~~~~~~~~~~~~~~~~~~~~~~~~

The HyperX python package is a library, written in python, for python developers.

Basic usage:

    >>> import hyperx
    >>> with hyperx.Open('mydatabase.hdb3') as hdb:
    >>>     print(f'Active project = {hdb.ActiveProject}')

The HyperX installation folder is found automatically if the installer was run.
Otherwise, the installation folder can be specified by setting the environment
variable `HyperXInstall`

    >>> import os
    >>> os.environ['HyperXInstall'] = 'C:/path/to/hyperx/installation'
    >>> import hyperx
"""

# TODO remove once encapsulated
from .library import _api, _types

from .api import Db, types
from .utils import Open, OpenWithDefault, WriteCsv
from typing import TypeVar, Generic, overload
from enum import Enum
from System.Collections.Generic import List, IEnumerable
from System.Threading.Tasks import Task
from System import Guid, DateTime

from abc import ABC, abstractmethod

T = TypeVar('T')

class AnalysisResultToReturn(Enum):
	Limit = 1
	Ultimate = 2
	Minimum = 3

class CollectionModificationStatus(Enum):
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
	Success = 1
	Failure = 2
	DuplicateNameFailure = 3

class ProjectDeletionStatus(Enum):
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
	English = 1
	SI = 2


class IdEntity(ABC):
	def __init__(self, idEntity: _api.IdEntity):
		self.Entity = idEntity

	@property
	def Id(self) -> int:
		return self.Entity.Id


class IdNameEntity(IdEntity):
	def __init__(self, idNameEntity: _api.IdNameEntity):
		self.Entity = idNameEntity

	@property
	def Name(self) -> str:
		return self.Entity.Name

class AnalysisDefinition(IdNameEntity):
	def __init__(self, analysisDefinition: _api.AnalysisDefinition):
		self.Entity = analysisDefinition

	@property
	def AnalysisId(self) -> int:
		return self.Entity.AnalysisId

	@property
	def Description(self) -> str:
		return self.Entity.Description


class Margin:
	def __init__(self, margin: _api.Margin):
		self.Entity = margin

	@property
	def AdjustedMargin(self) -> float:
		return self.Entity.AdjustedMargin

	@property
	def IsFailureCode(self) -> bool:
		return self.Entity.IsFailureCode

	@property
	def IsInformationalCode(self) -> bool:
		return self.Entity.IsInformationalCode

	@property
	def MarginCode(self) -> types.MarginCode:
		return types.MarginCode[self.Entity.MarginCode.ToString()]


class AnalysisResult(ABC):
	def __init__(self, analysisResult: _api.AnalysisResult):
		self.Entity = analysisResult

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		return types.LimitUltimate[self.Entity.LimitUltimate.ToString()]

	@property
	def LoadCaseId(self) -> int:
		return self.Entity.LoadCaseId

	@property
	def Margin(self) -> Margin:
		return Margin(self.Entity.Margin)

	@property
	def AnalysisDefinition(self) -> AnalysisDefinition:
		return AnalysisDefinition(self.Entity.AnalysisDefinition)


class JointAnalysisResult(AnalysisResult):
	def __init__(self, jointAnalysisResult: _api.JointAnalysisResult):
		self.Entity = jointAnalysisResult

	@property
	def ObjectId(self) -> types.JointObject:
		return types.JointObject[self.Entity.JointObject.ToString()]


class ZoneAnalysisConceptResult(AnalysisResult):
	def __init__(self, zoneAnalysisConceptResult: _api.ZoneAnalysisConceptResult):
		self.Entity = zoneAnalysisConceptResult

	@property
	def ConceptId(self) -> types.FamilyConceptUID:
		return types.FamilyConceptUID[self.Entity.FamilyConceptUID.ToString()]


class ZoneAnalysisObjectResult(AnalysisResult):
	def __init__(self, zoneAnalysisObjectResult: _api.ZoneAnalysisObjectResult):
		self.Entity = zoneAnalysisObjectResult

	@property
	def ObjectId(self) -> types.FamilyObjectUID:
		return types.FamilyObjectUID[self.Entity.FamilyObjectUID.ToString()]


class AssignableProperty(IdNameEntity):
	def __init__(self, assignableProperty: _api.AssignableProperty):
		self.Entity = assignableProperty


class AssignablePropertyWithFamilyCategory(AssignableProperty):
	def __init__(self, assignablePropertyWithFamilyCategory: _api.AssignablePropertyWithFamilyCategory):
		self.Entity = assignablePropertyWithFamilyCategory

	@property
	def FamilyCategory(self) -> types.FamilyCategory:
		return types.FamilyCategory[self.Entity.FamilyCategory.ToString()]


class FailureObjectGroup(IdNameEntity):
	def __init__(self, failureObjectGroup: _api.FailureObjectGroup):
		self.Entity = failureObjectGroup

	@property
	def IsEnabled(self) -> bool:
		return self.Entity.IsEnabled

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		return types.LimitUltimate[self.Entity.LimitUltimate.ToString()]

	@property
	def RequiredMargin(self) -> float:
		return self.Entity.RequiredMargin


class FailureSetting(IdNameEntity):
	def __init__(self, failureSetting: _api.FailureSetting):
		self.Entity = failureSetting

	@property
	def CategoryId(self) -> int:
		return self.Entity.CategoryId

	@property
	def DataType(self) -> types.UserConstantDataType:
		return types.UserConstantDataType[self.Entity.UserConstantDataType.ToString()]

	@property
	def DefaultValue(self) -> str:
		return self.Entity.DefaultValue

	@property
	def Description(self) -> str:
		return self.Entity.Description

	@property
	def EnumValues(self) -> dict[int, str]:
		enumValuesDict = {}
		for kvp in self.Entity.EnumValues:
			enumValuesDict[int[kvp.Key.ToString()]] = str(kvp.Value)

		return enumValuesDict

	@property
	def PackageId(self) -> int:
		return self.Entity.PackageId

	@property
	def PackageSettingId(self) -> int:
		return self.Entity.PackageSettingId

	@property
	def UID(self) -> Guid:
		return self.Entity.UID

	@property
	def Value(self) -> str:
		return self.Entity.Value


class IdEntityCol(Generic[T], ABC):
	def __init__(self, idEntityCol: _api.IdEntityCol):
		self.Entity = idEntityCol
		self.IdEntityColList = tuple([IdEntity(idEntityCol) for idEntityCol in self.Entity])

	def Contains(self, id: int) -> bool:
		return self.Entity.Contains(id)

	def Count(self) -> int:
		return self.Entity.Count()

	def Get(self, id: int) -> T:
		return self.Entity.Get(id)

	def GetEnumerator(self) -> tuple[T]:
		enumerator = self.Entity.GetEnumerator()
		tup = ()
		for item in enumerator:
			tup += (item)

		return tup

	def __getitem__(self, index: int):
		return self.IdEntityColList[index]

	def __iter__(self):
		yield from self.IdEntityColList

	def __len__(self):
		return len(self.IdEntityColList)


class IdNameEntityCol(IdEntityCol, Generic[T]):
	def __init__(self, idNameEntityCol: _api.IdNameEntityCol):
		self.Entity = idNameEntityCol
		self.CollectedClass = T
		self.IdNameEntityColList = tuple([T(idNameEntityCol) for idNameEntityCol in self.Entity])

	@overload
	def Get(self, name: str) -> T:
		pass

	@overload
	def Get(self, id: int) -> T:
		pass

	def Get(self, item1 = None) -> T:
		if isinstance(item1, str):
			return self.Entity.Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.IdNameEntityColList[index]

	def __iter__(self):
		yield from self.IdNameEntityColList

	def __len__(self):
		return len(self.IdNameEntityColList)


class FailureObjectGroupCol(IdNameEntityCol[FailureObjectGroup]):
	def __init__(self, failureObjectGroupCol: _api.FailureObjectGroupCol):
		self.Entity = failureObjectGroupCol
		self.CollectedClass = FailureObjectGroup
		self.FailureObjectGroupColList = tuple([FailureObjectGroup(failureObjectGroupCol) for failureObjectGroupCol in self.Entity])

	@overload
	def Get(self, name: str) -> FailureObjectGroup:
		pass

	@overload
	def Get(self, id: int) -> FailureObjectGroup:
		pass

	def Get(self, item1 = None) -> FailureObjectGroup:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.FailureObjectGroupColList[index]

	def __iter__(self):
		yield from self.FailureObjectGroupColList

	def __len__(self):
		return len(self.FailureObjectGroupColList)


class FailureSettingCol(IdNameEntityCol[FailureSetting]):
	def __init__(self, failureSettingCol: _api.FailureSettingCol):
		self.Entity = failureSettingCol
		self.CollectedClass = FailureSetting
		self.FailureSettingColList = tuple([FailureSetting(failureSettingCol) for failureSettingCol in self.Entity])

	@overload
	def Get(self, name: str) -> FailureSetting:
		pass

	@overload
	def Get(self, id: int) -> FailureSetting:
		pass

	def Get(self, item1 = None) -> FailureSetting:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.FailureSettingColList[index]

	def __iter__(self):
		yield from self.FailureSettingColList

	def __len__(self):
		return len(self.FailureSettingColList)


class FailureCriterion(IdNameEntity):
	def __init__(self, failureCriterion: _api.FailureCriterion):
		self.Entity = failureCriterion

	@property
	def Description(self) -> str:
		return self.Entity.Description

	@property
	def IsEnabled(self) -> bool:
		return self.Entity.IsEnabled

	@property
	def LimitUltimate(self) -> types.LimitUltimate:
		return types.LimitUltimate[self.Entity.LimitUltimate.ToString()]

	@property
	def ObjectGroups(self) -> FailureObjectGroupCol:
		return FailureObjectGroupCol(self.Entity.ObjectGroups)

	@property
	def RequiredMargin(self) -> float:
		return self.Entity.RequiredMargin

	@property
	def Settings(self) -> FailureSettingCol:
		return FailureSettingCol(self.Entity.Settings)


class IdNameEntityRenameable(IdNameEntity):
	def __init__(self, idNameEntityRenameable: _api.IdNameEntityRenameable):
		self.Entity = idNameEntityRenameable

	def Rename(self, name: str) -> None:
		return self.Entity.Rename(name)


class FailureCriterionCol(IdNameEntityCol[FailureCriterion]):
	def __init__(self, failureCriterionCol: _api.FailureCriterionCol):
		self.Entity = failureCriterionCol
		self.CollectedClass = FailureCriterion
		self.FailureCriterionColList = tuple([FailureCriterion(failureCriterionCol) for failureCriterionCol in self.Entity])

	@overload
	def Get(self, name: str) -> FailureCriterion:
		pass

	@overload
	def Get(self, id: int) -> FailureCriterion:
		pass

	def Get(self, item1 = None) -> FailureCriterion:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.FailureCriterionColList[index]

	def __iter__(self):
		yield from self.FailureCriterionColList

	def __len__(self):
		return len(self.FailureCriterionColList)


class FailureMode(IdNameEntityRenameable):
	def __init__(self, failureMode: _api.FailureMode):
		self.Entity = failureMode

	@property
	def AnalysisCategoryId(self) -> int:
		return self.Entity.AnalysisCategoryId

	@property
	def AnalysisCategoryName(self) -> str:
		return self.Entity.AnalysisCategoryName

	@property
	def Criteria(self) -> FailureCriterionCol:
		return FailureCriterionCol(self.Entity.Criteria)

	@property
	def Settings(self) -> FailureSettingCol:
		return FailureSettingCol(self.Entity.Settings)


class FailureModeCol(IdNameEntityCol[FailureMode]):
	def __init__(self, failureModeCol: _api.FailureModeCol):
		self.Entity = failureModeCol
		self.CollectedClass = FailureMode
		self.FailureModeColList = tuple([FailureMode(failureModeCol) for failureModeCol in self.Entity])

	@overload
	def Get(self, name: str) -> FailureMode:
		pass

	@overload
	def Get(self, id: int) -> FailureMode:
		pass

	def Get(self, item1 = None) -> FailureMode:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.FailureModeColList[index]

	def __iter__(self):
		yield from self.FailureModeColList

	def __len__(self):
		return len(self.FailureModeColList)


class AnalysisProperty(AssignablePropertyWithFamilyCategory):
	def __init__(self, analysisProperty: _api.AnalysisProperty):
		self.Entity = analysisProperty

	@property
	def FailureModes(self) -> FailureModeCol:
		return FailureModeCol(self.Entity.FailureModes)

	@overload
	def AddFailureMode(self, id: int) -> None:
		pass

	@overload
	def AddFailureMode(self, ids: tuple[int]) -> None:
		pass

	@overload
	def RemoveFailureMode(self, id: int) -> None:
		pass

	@overload
	def RemoveFailureMode(self, ids: tuple[int]) -> None:
		pass

	def AddFailureMode(self, item1 = None) -> None:
		if isinstance(item1, int):
			return self.Entity.AddFailureMode(item1)

		if isinstance(item1, tuple):
			idsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						idsList.Add(thing)
			idsEnumerable = IEnumerable(idsList)
			return self.Entity.AddFailureMode(idsEnumerable)

	def RemoveFailureMode(self, item1 = None) -> None:
		if isinstance(item1, int):
			return self.Entity.RemoveFailureMode(item1)

		if isinstance(item1, tuple):
			idsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						idsList.Add(thing)
			idsEnumerable = IEnumerable(idsList)
			return self.Entity.RemoveFailureMode(idsEnumerable)


class DesignProperty(AssignablePropertyWithFamilyCategory):
	def __init__(self, designProperty: _api.DesignProperty):
		self.Entity = designProperty

	def Copy(self, newName: str) -> int:
		return self.Entity.Copy(newName)


class LoadProperty(AssignableProperty):
	def __init__(self, loadProperty: _api.LoadProperty):
		self.Entity = loadProperty


class DesignLoadSubcase(IdNameEntity):
	def __init__(self, designLoadSubcase: _api.DesignLoadSubcase):
		self.Entity = designLoadSubcase

	@property
	def RunDeckId(self) -> int:
		return self.Entity.RunDeckId

	@property
	def IsThermal(self) -> bool:
		return self.Entity.IsThermal

	@property
	def IsEditable(self) -> bool:
		return self.Entity.IsEditable

	@property
	def Description(self) -> str:
		return self.Entity.Description

	@property
	def ModificationDate(self) -> DateTime:
		return self.Entity.ModificationDate

	@property
	def NastranSubcaseId(self) -> int:
		return self.Entity.NastranSubcaseId

	@property
	def NastranLoadId(self) -> int:
		return self.Entity.NastranLoadId

	@property
	def NastranSpcId(self) -> int:
		return self.Entity.NastranSpcId

	@property
	def AbaqusStepName(self) -> str:
		return self.Entity.AbaqusStepName

	@property
	def AbaqusLoadCaseName(self) -> str:
		return self.Entity.AbaqusLoadCaseName

	@property
	def AbaqusStepTime(self) -> float:
		return self.Entity.AbaqusStepTime

	@property
	def RunDeckOrder(self) -> int:
		return self.Entity.RunDeckOrder

	@property
	def SolutionType(self) -> types.FeaSolutionType:
		return types.FeaSolutionType[self.Entity.FeaSolutionType.ToString()]


class DesignLoadSubcaseMultiplier(IdNameEntity):
	def __init__(self, designLoadSubcaseMultiplier: _api.DesignLoadSubcaseMultiplier):
		self.Entity = designLoadSubcaseMultiplier

	@property
	def LimitFactor(self) -> float:
		return self.Entity.LimitFactor

	@property
	def Subcase(self) -> DesignLoadSubcase:
		return DesignLoadSubcase(self.Entity.Subcase)

	@property
	def UltimateFactor(self) -> float:
		return self.Entity.UltimateFactor

	@property
	def Value(self) -> float:
		return self.Entity.Value


class DesignLoadSubcaseTemperature(IdNameEntity):
	def __init__(self, designLoadSubcaseTemperature: _api.DesignLoadSubcaseTemperature):
		self.Entity = designLoadSubcaseTemperature

	@property
	def HasTemperatureSubcase(self) -> bool:
		return self.Entity.HasTemperatureSubcase

	@property
	def Subcase(self) -> DesignLoadSubcase:
		return DesignLoadSubcase(self.Entity.Subcase)

	@property
	def TemperatureChoiceType(self) -> types.TemperatureChoiceType:
		return types.TemperatureChoiceType[self.Entity.TemperatureChoiceType.ToString()]

	@property
	def Value(self) -> float:
		return self.Entity.Value


class DesignLoadSubcaseMultiplierCol(IdNameEntityCol[DesignLoadSubcaseMultiplier]):
	def __init__(self, designLoadSubcaseMultiplierCol: _api.DesignLoadSubcaseMultiplierCol):
		self.Entity = designLoadSubcaseMultiplierCol
		self.CollectedClass = DesignLoadSubcaseMultiplier
		self.DesignLoadSubcaseMultiplierColList = tuple([DesignLoadSubcaseMultiplier(designLoadSubcaseMultiplierCol) for designLoadSubcaseMultiplierCol in self.Entity])

	@overload
	def Get(self, name: str) -> DesignLoadSubcaseMultiplier:
		pass

	@overload
	def Get(self, id: int) -> DesignLoadSubcaseMultiplier:
		pass

	def Get(self, item1 = None) -> DesignLoadSubcaseMultiplier:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.DesignLoadSubcaseMultiplierColList[index]

	def __iter__(self):
		yield from self.DesignLoadSubcaseMultiplierColList

	def __len__(self):
		return len(self.DesignLoadSubcaseMultiplierColList)


class DesignLoad(IdNameEntity):
	def __init__(self, designLoad: _api.DesignLoad):
		self.Entity = designLoad

	@property
	def AnalysisTemperature(self) -> DesignLoadSubcaseTemperature:
		return DesignLoadSubcaseTemperature(self.Entity.AnalysisTemperature)

	@property
	def Description(self) -> str:
		return self.Entity.Description

	@property
	def InitialTemperature(self) -> DesignLoadSubcaseTemperature:
		return DesignLoadSubcaseTemperature(self.Entity.InitialTemperature)

	@property
	def IsActive(self) -> bool:
		return self.Entity.IsActive

	@property
	def IsEditable(self) -> bool:
		return self.Entity.IsEditable

	@property
	def IsVirtual(self) -> bool:
		return self.Entity.IsVirtual

	@property
	def ModificationDate(self) -> DateTime:
		return self.Entity.ModificationDate

	@property
	def SubcaseMultipliers(self) -> DesignLoadSubcaseMultiplierCol:
		return DesignLoadSubcaseMultiplierCol(self.Entity.SubcaseMultipliers)

	@property
	def Types(self) -> list[types.LoadCaseType]:
		return [types.LoadCaseType[loadCaseType.ToString()] for loadCaseType in self.Entity.Types]

	@property
	def UID(self) -> Guid:
		return self.Entity.UID


class Vector3d:
	def __init__(self, vector3d: _api.Vector3d):
		self.Entity = vector3d

	@property
	def X(self) -> float:
		return self.Entity.X

	@property
	def Y(self) -> float:
		return self.Entity.Y

	@property
	def Z(self) -> float:
		return self.Entity.Z

	@overload
	def Equals(self, other) -> bool:
		pass

	@overload
	def Equals(self, obj) -> bool:
		pass

	def GetHashCode(self) -> int:
		return self.Entity.GetHashCode()

	def Equals(self, item1 = None) -> bool:
		if isinstance(item1, Vector3d):
			return self.Entity.Equals(item1)

		return self.Entity.Equals(item1)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)


class DiscreteFieldTable(IdNameEntityRenameable):
	def __init__(self, discreteFieldTable: _api.DiscreteFieldTable):
		self.Entity = discreteFieldTable

	@property
	def Columns(self) -> dict[int, str]:
		columnsDict = {}
		for kvp in self.Entity.Columns:
			columnsDict[int[kvp.Key.ToString()]] = str(kvp.Value)

		return columnsDict

	@property
	def ColumnCount(self) -> int:
		return self.Entity.ColumnCount

	@property
	def DataType(self) -> types.DiscreteFieldDataType:
		return types.DiscreteFieldDataType[self.Entity.DiscreteFieldDataType.ToString()]

	@property
	def PhysicalEntityType(self) -> types.DiscreteFieldPhysicalEntityType:
		return types.DiscreteFieldPhysicalEntityType[self.Entity.DiscreteFieldPhysicalEntityType.ToString()]

	@property
	def PointIds(self) -> list[Vector3d]:
		return [Vector3d[vector3d.ToString()] for vector3d in self.Entity.PointIds]

	@property
	def RowCount(self) -> int:
		return self.Entity.RowCount

	@property
	def RowIds(self) -> list[int]:
		return [int32 for int32 in self.Entity.RowIds]

	def AddColumn(self, name: str) -> int:
		return self.Entity.AddColumn(name)

	def AddPointRow(self, pointId: Vector3d) -> None:
		return self.Entity.AddPointRow(pointId.Entity)

	@overload
	def ReadNumericCell(self, entityId: int, columnId: int) -> float:
		pass

	@overload
	def ReadNumericCell(self, pointId: Vector3d, columnId: int) -> float:
		pass

	@overload
	def ReadStringCell(self, entityId: int, columnId: int) -> str:
		pass

	@overload
	def ReadStringCell(self, pointId: Vector3d, columnId: int) -> str:
		pass

	def SetColumnName(self, columnId: int, name: str) -> None:
		return self.Entity.SetColumnName(columnId, name)

	@overload
	def SetNumericValue(self, entityId: int, columnId: int, value: float) -> None:
		pass

	@overload
	def SetNumericValue(self, pointId: Vector3d, columnId: int, value: float) -> None:
		pass

	@overload
	def SetStringValue(self, entityId: int, columnId: int, value: str) -> None:
		pass

	@overload
	def SetStringValue(self, pointId: Vector3d, columnId: int, value: str) -> None:
		pass

	def DeleteAllRows(self) -> None:
		return self.Entity.DeleteAllRows()

	def DeleteColumn(self, columnId: int) -> None:
		return self.Entity.DeleteColumn(columnId)

	def DeletePointRow(self, pointId: Vector3d) -> None:
		return self.Entity.DeletePointRow(pointId.Entity)

	def DeleteRow(self, entityId: int) -> None:
		return self.Entity.DeleteRow(entityId)

	def DeleteRowsAndColumns(self) -> None:
		return self.Entity.DeleteRowsAndColumns()

	def ReadNumericCell(self, item1 = None, item2 = None) -> float:
		if isinstance(item1, int) and isinstance(item2, int):
			return self.Entity.ReadNumericCell(item1, item2)

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return self.Entity.ReadNumericCell(item1, item2)

	def ReadStringCell(self, item1 = None, item2 = None) -> str:
		if isinstance(item1, int) and isinstance(item2, int):
			return self.Entity.ReadStringCell(item1, item2)

		if isinstance(item1, Vector3d) and isinstance(item2, int):
			return self.Entity.ReadStringCell(item1, item2)

	def SetNumericValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, int) and isinstance(item3, float):
			return self.Entity.SetNumericValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and isinstance(item3, float):
			return self.Entity.SetNumericValue(item1, item2, item3)

	def SetStringValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, int) and isinstance(item3, str):
			return self.Entity.SetStringValue(item1, item2, item3)

		if isinstance(item1, Vector3d) and isinstance(item2, int) and isinstance(item3, str):
			return self.Entity.SetStringValue(item1, item2, item3)


class Centroid:
	def __init__(self, centroid: _api.Centroid):
		self.Entity = centroid

	@property
	def X(self) -> float:
		return self.Entity.X

	@property
	def Y(self) -> float:
		return self.Entity.Y

	@property
	def Z(self) -> float:
		return self.Entity.Z


class Element(IdEntity):
	def __init__(self, element: _api.Element):
		self.Entity = element

	@property
	def MarginOfSafety(self) -> float:
		return self.Entity.MarginOfSafety

	@property
	def Centroid(self) -> Centroid:
		return Centroid(self.Entity.Centroid)


class FailureModeCategory(IdNameEntity):
	def __init__(self, failureModeCategory: _api.FailureModeCategory):
		self.Entity = failureModeCategory

	@property
	def PackageId(self) -> int:
		return self.Entity.PackageId


class EntityWithAssignableProperties(IdNameEntityRenameable):
	def __init__(self, entityWithAssignableProperties: _api.EntityWithAssignableProperties):
		self.Entity = entityWithAssignableProperties

	@property
	def AssignedAnalysisProperty(self) -> AnalysisProperty:
		return AnalysisProperty(self.Entity.AssignedAnalysisProperty)

	@property
	def AssignedDesignProperty(self) -> DesignProperty:
		thisClass = type(self.Entity.AssignedDesignProperty).__name__
		givenClass = DesignProperty
		for subclass in DesignProperty.__subclasses__():
			if subclass.__name__ == thisClass:
				givenClass = subclass
		return givenClass(self.Entity.AssignedDesignProperty)

	@property
	def AssignedLoadProperty(self) -> LoadProperty:
		return LoadProperty(self.Entity.AssignedLoadProperty)

	def AssignAnalysisProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self.Entity.AssignAnalysisProperty(id).ToString()]

	def AssignDesignProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self.Entity.AssignDesignProperty(id).ToString()]

	def AssignLoadProperty(self, id: int) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self.Entity.AssignLoadProperty(id).ToString()]

	def AssignProperty(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self.Entity.AssignProperty(property.Entity).ToString()]


class AnalysisResultCol(Generic[T]):
	def __init__(self, analysisResultCol: _api.AnalysisResultCol):
		self.Entity = analysisResultCol
		self.AnalysisResultColList = tuple([AnalysisResult(analysisResultCol) for analysisResultCol in self.Entity])

	def Count(self) -> int:
		return self.Entity.Count()

	def GetEnumerator(self) -> tuple[T]:
		enumerator = self.Entity.GetEnumerator()
		tup = ()
		for item in enumerator:
			tup += (item)

		return tup

	def __getitem__(self, index: int):
		return self.AnalysisResultColList[index]

	def __iter__(self):
		yield from self.AnalysisResultColList

	def __len__(self):
		return len(self.AnalysisResultColList)


class ZoneJointEntity(EntityWithAssignableProperties):
	def __init__(self, zoneJointEntity: _api.ZoneJointEntity):
		self.Entity = zoneJointEntity

	@abstractmethod
	def GetMinimumMargin(self) -> Margin:
		return Margin(self.Entity.GetMinimumMargin())

	@abstractmethod
	def GetControllingResult(self) -> AnalysisResult:
		return AnalysisResult(self.Entity.GetControllingResult())

	@abstractmethod
	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self.Entity.GetAllResults())


class Joint(ZoneJointEntity):
	def __init__(self, joint: _api.Joint):
		self.Entity = joint

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self.Entity.GetAllResults())

	def GetControllingResult(self) -> AnalysisResult:
		return AnalysisResult(self.Entity.GetControllingResult())

	def GetMinimumMargin(self) -> Margin:
		return Margin(self.Entity.GetMinimumMargin())


class ZoneBase(ZoneJointEntity):
	def __init__(self, zoneBase: _api.ZoneBase):
		self.Entity = zoneBase

	@property
	def Centroid(self) -> Centroid:
		return Centroid(self.Entity.Centroid)

	@property
	def Id(self) -> int:
		return self.Entity.Id

	@property
	def Weight(self) -> float:
		return self.Entity.Weight

	def RenumberZone(self, newId: int) -> ZoneIdUpdateStatus:
		return ZoneIdUpdateStatus[self.Entity.RenumberZone(newId).ToString()]

	def GetAllResults(self) -> AnalysisResultCol:
		return AnalysisResultCol(self.Entity.GetAllResults())

	def GetControllingResult(self) -> AnalysisResult:
		return AnalysisResult(self.Entity.GetControllingResult())

	def GetMinimumMargin(self) -> Margin:
		return Margin(self.Entity.GetMinimumMargin())


class ElementCol(IdEntityCol[Element]):
	def __init__(self, elementCol: _api.ElementCol):
		self.Entity = elementCol
		self.CollectedClass = Element
		self.ElementColList = tuple([Element(elementCol) for elementCol in self.Entity])

	def __getitem__(self, index: int):
		return self.ElementColList[index]

	def __iter__(self):
		yield from self.ElementColList

	def __len__(self):
		return len(self.ElementColList)


class PanelSegment(ZoneBase):
	def __init__(self, panelSegment: _api.PanelSegment):
		self.Entity = panelSegment

	@property
	def ElementsByObjectOrSkin(self) -> dict[types.DiscreteDefinitionType, ElementCol]:
		elementsByObjectOrSkinDict = {}
		for kvp in self.Entity.ElementsByObjectOrSkin:
			elementsByObjectOrSkinDict[types.DiscreteDefinitionType[kvp.Key.ToString()]] = ElementCol(kvp.Value)

		return elementsByObjectOrSkinDict

	@property
	def Skins(self) -> tuple[types.DiscreteDefinitionType]:
		return tuple([types.DiscreteDefinitionType(discreteDefinitionType) for discreteDefinitionType in self.Entity.Skins])

	@property
	def Objects(self) -> tuple[types.DiscreteDefinitionType]:
		return tuple([types.DiscreteDefinitionType(discreteDefinitionType) for discreteDefinitionType in self.Entity.Objects])

	@property
	def DiscreteTechnique(self) -> types.DiscreteTechnique:
		return types.DiscreteTechnique[self.Entity.DiscreteTechnique.ToString()]

	@property
	def LeftSkinZoneId(self) -> int:
		return self.Entity.LeftSkinZoneId

	@property
	def RightSkinZoneId(self) -> int:
		return self.Entity.RightSkinZoneId

	def GetElements(self, discreteDefinitionType: types.DiscreteDefinitionType) -> ElementCol:
		return ElementCol(self.Entity.GetElements(_types.DiscreteDefinitionType(discreteDefinitionType.value)))

	def SetObjectElements(self, discreteDefinitionType: types.DiscreteDefinitionType, elementIds: tuple[int]) -> None:
		elementIdsList = List[int]()
		if elementIds is not None:
			for thing in elementIds:
				if thing is not None:
					elementIdsList.Add(thing)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self.Entity.SetObjectElements(_types.DiscreteDefinitionType(discreteDefinitionType.value), elementIdsEnumerable)


class Zone(ZoneBase):
	def __init__(self, zone: _api.Zone):
		self.Entity = zone

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self.Entity.Elements)

	def AddElements(self, elementIds: tuple[int]) -> None:
		elementIdsList = List[int]()
		if elementIds is not None:
			for thing in elementIds:
				if thing is not None:
					elementIdsList.Add(thing)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self.Entity.AddElements(elementIdsEnumerable)


class EntityWithAssignablePropertiesCol(IdNameEntityCol, Generic[T]):
	def __init__(self, entityWithAssignablePropertiesCol: _api.EntityWithAssignablePropertiesCol):
		self.Entity = entityWithAssignablePropertiesCol
		self.CollectedClass = T
		self.EntityWithAssignablePropertiesColList = tuple([T(entityWithAssignablePropertiesCol) for entityWithAssignablePropertiesCol in self.Entity])

	def AssignPropertyToAll(self, property: AssignableProperty) -> PropertyAssignmentStatus:
		return PropertyAssignmentStatus[self.Entity.AssignPropertyToAll(property.Entity).ToString()]

	@overload
	def Get(self, name: str) -> T:
		pass

	@overload
	def Get(self, id: int) -> T:
		pass

	def Get(self, item1 = None) -> T:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.EntityWithAssignablePropertiesColList[index]

	def __iter__(self):
		yield from self.EntityWithAssignablePropertiesColList

	def __len__(self):
		return len(self.EntityWithAssignablePropertiesColList)


class JointCol(EntityWithAssignablePropertiesCol[Joint]):
	def __init__(self, jointCol: _api.JointCol):
		self.Entity = jointCol
		self.CollectedClass = Joint
		self.JointColList = tuple([Joint(jointCol) for jointCol in self.Entity])

	@overload
	def Get(self, name: str) -> Joint:
		pass

	@overload
	def Get(self, id: int) -> Joint:
		pass

	def Get(self, item1 = None) -> Joint:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.JointColList[index]

	def __iter__(self):
		yield from self.JointColList

	def __len__(self):
		return len(self.JointColList)


class PanelSegmentCol(EntityWithAssignablePropertiesCol[PanelSegment]):
	def __init__(self, panelSegmentCol: _api.PanelSegmentCol):
		self.Entity = panelSegmentCol
		self.CollectedClass = PanelSegment
		self.PanelSegmentColList = tuple([PanelSegment(panelSegmentCol) for panelSegmentCol in self.Entity])

	@overload
	def Get(self, name: str) -> PanelSegment:
		pass

	@overload
	def Get(self, id: int) -> PanelSegment:
		pass

	def Get(self, item1 = None) -> PanelSegment:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.PanelSegmentColList[index]

	def __iter__(self):
		yield from self.PanelSegmentColList

	def __len__(self):
		return len(self.PanelSegmentColList)


class ZoneCol(EntityWithAssignablePropertiesCol[Zone]):
	def __init__(self, zoneCol: _api.ZoneCol):
		self.Entity = zoneCol
		self.CollectedClass = Zone
		self.ZoneColList = tuple([Zone(zoneCol) for zoneCol in self.Entity])

	@overload
	def Get(self, name: str) -> Zone:
		pass

	@overload
	def Get(self, id: int) -> Zone:
		pass

	def Get(self, item1 = None) -> Zone:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.ZoneColList[index]

	def __iter__(self):
		yield from self.ZoneColList

	def __len__(self):
		return len(self.ZoneColList)


class ZoneJointContainer(IdNameEntityRenameable):
	def __init__(self, zoneJointContainer: _api.ZoneJointContainer):
		self.Entity = zoneJointContainer

	@property
	def Centroid(self) -> Centroid:
		return Centroid(self.Entity.Centroid)

	@property
	def Joints(self) -> JointCol:
		return JointCol(self.Entity.Joints)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self.Entity.PanelSegments)

	@property
	def TotalBeamLength(self) -> float:
		return self.Entity.TotalBeamLength

	@property
	def TotalPanelArea(self) -> float:
		return self.Entity.TotalPanelArea

	@property
	def TotalZoneWeight(self) -> float:
		return self.Entity.TotalZoneWeight

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self.Entity.Zones)

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoints(self, joints: JointCol) -> CollectionModificationStatus:
		pass

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZones(self, zones: ZoneCol) -> CollectionModificationStatus:
		pass

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegments(self, segments: PanelSegmentCol) -> CollectionModificationStatus:
		pass

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self.Entity.AddJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self.Entity.AddJoint(item1).ToString()]

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self.Entity.RemoveJoint(item1).ToString()]

		if isinstance(item1, Joint):
			return CollectionModificationStatus[self.Entity.RemoveJoint(item1).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			jointIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						jointIdsList.Add(thing)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self.Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, JointCol):
			return CollectionModificationStatus[self.Entity.RemoveJoints(item1).ToString()]

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self.Entity.AddZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self.Entity.AddZone(item1).ToString()]

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self.Entity.RemoveZone(item1).ToString()]

		if isinstance(item1, Zone):
			return CollectionModificationStatus[self.Entity.RemoveZone(item1).ToString()]

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			zoneIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zoneIdsList.Add(thing)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self.Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, ZoneCol):
			return CollectionModificationStatus[self.Entity.RemoveZones(item1).ToString()]

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self.Entity.AddPanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self.Entity.AddPanelSegment(item1).ToString()]

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return CollectionModificationStatus[self.Entity.RemovePanelSegment(item1).ToString()]

		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self.Entity.RemovePanelSegment(item1).ToString()]

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			segmentIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						segmentIdsList.Add(thing)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self.Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, PanelSegmentCol):
			return CollectionModificationStatus[self.Entity.RemovePanelSegments(item1).ToString()]


class FoamTemperature:
	def __init__(self, foamTemperature: _api.FoamTemperature):
		self.Entity = foamTemperature

	@property
	def Temperature(self) -> float:
		return self.Entity.Temperature

	@property
	def Et(self) -> float:
		return self.Entity.Et

	@property
	def Ec(self) -> float:
		return self.Entity.Ec

	@property
	def G(self) -> float:
		return self.Entity.G

	@property
	def Ef(self) -> float:
		return self.Entity.Ef

	@property
	def Ftu(self) -> float:
		return self.Entity.Ftu

	@property
	def Fcu(self) -> float:
		return self.Entity.Fcu

	@property
	def Fsu(self) -> float:
		return self.Entity.Fsu

	@property
	def Ffu(self) -> float:
		return self.Entity.Ffu

	@property
	def K(self) -> float:
		return self.Entity.K

	@property
	def C(self) -> float:
		return self.Entity.C


class Foam:
	def __init__(self, foam: _api.Foam):
		self.Entity = foam

	@property
	def MaterialFamilyName(self) -> str:
		return self.Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self.Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self.Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self.Entity.Name

	@property
	def Wet(self) -> bool:
		return self.Entity.Wet

	@property
	def Density(self) -> float:
		return self.Entity.Density

	@property
	def Form(self) -> str:
		return self.Entity.Form

	@property
	def Specification(self) -> str:
		return self.Entity.Specification

	@property
	def MaterialDescription(self) -> str:
		return self.Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self.Entity.UserNote

	@property
	def FemMaterialId(self) -> int:
		return self.Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self.Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float:
		return self.Entity.BucklingStiffnessKnockdown

	@property
	def Absorption(self) -> float:
		return self.Entity.Absorption

	@property
	def Manufacturer(self) -> str:
		return self.Entity.Manufacturer

	def AddTemperatureProperty(self, temperature: float, et: float = None, ec: float = None, g: float = None, ef: float = None, ftu: float = None, fcu: float = None, fsu: float = None, ffu: float = None, k: float = None, c: float = None) -> FoamTemperature:
		return FoamTemperature(self.Entity.AddTemperatureProperty(temperature, et, ec, g, ef, ftu, fcu, fsu, ffu, k, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self.Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> FoamTemperature:
		return FoamTemperature(self.Entity.GetTemperature(lookupTemperature))

	def Save(self) -> None:
		return self.Entity.Save()


class HoneycombTemperature:
	def __init__(self, honeycombTemperature: _api.HoneycombTemperature):
		self.Entity = honeycombTemperature

	@property
	def Temperature(self) -> float:
		return self.Entity.Temperature

	@property
	def Et(self) -> float:
		return self.Entity.Et

	@property
	def Ec(self) -> float:
		return self.Entity.Ec

	@property
	def Gw(self) -> float:
		return self.Entity.Gw

	@property
	def Gl(self) -> float:
		return self.Entity.Gl

	@property
	def Ftu(self) -> float:
		return self.Entity.Ftu

	@property
	def Fcus(self) -> float:
		return self.Entity.Fcus

	@property
	def Fcub(self) -> float:
		return self.Entity.Fcub

	@property
	def Fcuc(self) -> float:
		return self.Entity.Fcuc

	@property
	def Fsuw(self) -> float:
		return self.Entity.Fsuw

	@property
	def Fsul(self) -> float:
		return self.Entity.Fsul

	@property
	def SScfl(self) -> float:
		return self.Entity.SScfl

	@property
	def SScfh(self) -> float:
		return self.Entity.SScfh

	@property
	def Kl(self) -> float:
		return self.Entity.Kl

	@property
	def Kw(self) -> float:
		return self.Entity.Kw

	@property
	def Kt(self) -> float:
		return self.Entity.Kt

	@property
	def C(self) -> float:
		return self.Entity.C


class Honeycomb:
	def __init__(self, honeycomb: _api.Honeycomb):
		self.Entity = honeycomb

	@property
	def MaterialFamilyName(self) -> str:
		return self.Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self.Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self.Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self.Entity.Name

	@property
	def Wet(self) -> bool:
		return self.Entity.Wet

	@property
	def Density(self) -> float:
		return self.Entity.Density

	@property
	def Form(self) -> str:
		return self.Entity.Form

	@property
	def Specification(self) -> str:
		return self.Entity.Specification

	@property
	def MaterialDescription(self) -> str:
		return self.Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self.Entity.UserNote

	@property
	def FemMaterialId(self) -> int:
		return self.Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self.Entity.Cost

	@property
	def CellSize(self) -> float:
		return self.Entity.CellSize

	@property
	def Manufacturer(self) -> str:
		return self.Entity.Manufacturer

	def AddTemperatureProperty(self, temperature: float, et: float = None, ec: float = None, gw: float = None, gl: float = None, ftu: float = None, fcus: float = None, fcub: float = None, fcuc: float = None, fsuw: float = None, fsul: float = None, sScfl: float = None, sScfh: float = None, k1: float = None, k2: float = None, k3: float = None, c: float = None) -> HoneycombTemperature:
		return HoneycombTemperature(self.Entity.AddTemperatureProperty(temperature, et, ec, gw, gl, ftu, fcus, fcub, fcuc, fsuw, fsul, sScfl, sScfh, k1, k2, k3, c))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self.Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> HoneycombTemperature:
		return HoneycombTemperature(self.Entity.GetTemperature(lookupTemperature))

	def Save(self) -> None:
		return self.Entity.Save()


class IsotropicTemperature:
	def __init__(self, isotropicTemperature: _api.IsotropicTemperature):
		self.Entity = isotropicTemperature

	@property
	def Temperature(self) -> float:
		return self.Entity.Temperature

	@property
	def Et(self) -> float:
		return self.Entity.Et

	@property
	def Ec(self) -> float:
		return self.Entity.Ec

	@property
	def G(self) -> float:
		return self.Entity.G

	@property
	def n(self) -> float:
		return self.Entity.n

	@property
	def F02(self) -> float:
		return self.Entity.F02

	@property
	def FtuL(self) -> float:
		return self.Entity.FtuL

	@property
	def FtyL(self) -> float:
		return self.Entity.FtyL

	@property
	def FcyL(self) -> float:
		return self.Entity.FcyL

	@property
	def FtuLT(self) -> float:
		return self.Entity.FtuLT

	@property
	def FtyLT(self) -> float:
		return self.Entity.FtyLT

	@property
	def FcyLT(self) -> float:
		return self.Entity.FcyLT

	@property
	def Fsu(self) -> float:
		return self.Entity.Fsu

	@property
	def Fbru15(self) -> float:
		return self.Entity.Fbru15

	@property
	def Fbry15(self) -> float:
		return self.Entity.Fbry15

	@property
	def Fbru20(self) -> float:
		return self.Entity.Fbru20

	@property
	def Fbry20(self) -> float:
		return self.Entity.Fbry20

	@property
	def alpha(self) -> float:
		return self.Entity.alpha

	@property
	def K(self) -> float:
		return self.Entity.K

	@property
	def C(self) -> float:
		return self.Entity.C

	@property
	def etyL(self) -> float:
		return self.Entity.etyL

	@property
	def ecyL(self) -> float:
		return self.Entity.ecyL

	@property
	def etyLT(self) -> float:
		return self.Entity.etyLT

	@property
	def ecyLT(self) -> float:
		return self.Entity.ecyLT

	@property
	def esu(self) -> float:
		return self.Entity.esu

	@property
	def Fpadh(self) -> float:
		return self.Entity.Fpadh

	@property
	def Fsadh(self) -> float:
		return self.Entity.Fsadh

	@property
	def esadh(self) -> float:
		return self.Entity.esadh

	@property
	def cd(self) -> float:
		return self.Entity.cd

	@property
	def Ffwt(self) -> float:
		return self.Entity.Ffwt

	@property
	def Ffxz(self) -> float:
		return self.Entity.Ffxz

	@property
	def Ffyz(self) -> float:
		return self.Entity.Ffyz

	@property
	def FtFatigue(self) -> float:
		return self.Entity.FtFatigue

	@property
	def FcFatigue(self) -> float:
		return self.Entity.FcFatigue


class Isotropic:
	def __init__(self, isotropic: _api.Isotropic):
		self.Entity = isotropic

	@property
	def MaterialFamilyName(self) -> str:
		return self.Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self.Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self.Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self.Entity.Name

	@property
	def Form(self) -> str:
		return self.Entity.Form

	@property
	def Specification(self) -> str:
		return self.Entity.Specification

	@property
	def Temper(self) -> str:
		return self.Entity.Temper

	@property
	def Basis(self) -> str:
		return self.Entity.Basis

	@property
	def Density(self) -> float:
		return self.Entity.Density

	@property
	def MaterialDescription(self) -> str:
		return self.Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self.Entity.UserNote

	@property
	def FemMaterialId(self) -> int:
		return self.Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self.Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float:
		return self.Entity.BucklingStiffnessKnockdown

	def AddTemperatureProperty(self, temperature: float, et: float = None, ec: float = None, g: float = None, n: float = None, f02: float = None, ftuL: float = None, ftyL: float = None, fcyL: float = None, ftuLT: float = None, ftyLT: float = None, fcyLT: float = None, fsu: float = None, fbru15: float = None, fbry15: float = None, fbru20: float = None, fbry20: float = None, alpha: float = None, k: float = None, c: float = None, etyL: float = None, ecyL: float = None, etyLT: float = None, ecyLT: float = None, esu: float = None, fpadh: float = None, fsadh: float = None, esadh: float = None, cd: float = None, ffwt: float = None, ffxz: float = None, ffyz: float = None, ftFatigue: float = None, fcFatigue: float = None) -> IsotropicTemperature:
		return IsotropicTemperature(self.Entity.AddTemperatureProperty(temperature, et, ec, g, n, f02, ftuL, ftyL, fcyL, ftuLT, ftyLT, fcyLT, fsu, fbru15, fbry15, fbru20, fbry20, alpha, k, c, etyL, ecyL, etyLT, ecyLT, esu, fpadh, fsadh, esadh, cd, ffwt, ffxz, ffyz, ftFatigue, fcFatigue))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self.Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> IsotropicTemperature:
		return IsotropicTemperature(self.Entity.GetTemperature(lookupTemperature))

	def Save(self) -> None:
		return self.Entity.Save()


class OrthotropicCorrectionFactorBase(ABC):
	def __init__(self, orthotropicCorrectionFactorBase: _api.OrthotropicCorrectionFactorBase):
		self.Entity = orthotropicCorrectionFactorBase

	@property
	def CorrectionId(self) -> types.CorrectionId:
		return types.CorrectionId[self.Entity.CorrectionId.ToString()]

	@property
	def PropertyId(self) -> types.CorrectionProperty:
		return types.CorrectionProperty[self.Entity.CorrectionProperty.ToString()]


class OrthotropicCorrectionFactorValue:
	def __init__(self, orthotropicCorrectionFactorValue: _api.OrthotropicCorrectionFactorValue):
		self.Entity = orthotropicCorrectionFactorValue

	@property
	def Property(self) -> types.CorrectionProperty:
		return types.CorrectionProperty[self.Entity.CorrectionProperty.ToString()]

	@property
	def Correction(self) -> types.CorrectionId:
		return types.CorrectionId[self.Entity.CorrectionId.ToString()]

	@property
	def Equation(self) -> types.CorrectionEquation:
		return types.CorrectionEquation[self.Entity.CorrectionEquation.ToString()]

	@property
	def EquationParameter(self) -> types.EquationParameterId:
		return types.EquationParameterId[self.Entity.EquationParameterId.ToString()]

	@property
	def Value(self) -> float:
		return self.Entity.Value


class OrthotropicEquationCorrectionFactor(OrthotropicCorrectionFactorBase):
	def __init__(self, orthotropicEquationCorrectionFactor: _api.OrthotropicEquationCorrectionFactor):
		self.Entity = orthotropicEquationCorrectionFactor

	@property
	def Equation(self) -> types.CorrectionEquation:
		return types.CorrectionEquation[self.Entity.CorrectionEquation.ToString()]

	def AddCorrectionFactorValue(self, equationParameterName: types.EquationParameterId, valueToAdd: float) -> OrthotropicCorrectionFactorValue:
		return OrthotropicCorrectionFactorValue(self.Entity.AddCorrectionFactorValue(_types.EquationParameterId(equationParameterName.value), valueToAdd))


class TabularCorrectionFactorRow:
	def __init__(self, tabularCorrectionFactorRow: _api.TabularCorrectionFactorRow):
		self.Entity = tabularCorrectionFactorRow

	@property
	def DependentValue(self) -> float:
		return self.Entity.DependentValue


class OrthotropicTabularCorrectionFactor(OrthotropicCorrectionFactorBase):
	def __init__(self, orthotropicTabularCorrectionFactor: _api.OrthotropicTabularCorrectionFactor):
		self.Entity = orthotropicTabularCorrectionFactor

	@property
	def CorrectionFactorRows(self) -> dict[int, TabularCorrectionFactorRow]:
		correctionFactorRowsDict = {}
		for kvp in self.Entity.CorrectionFactorRows:
			correctionFactorRowsDict[int[kvp.Key.ToString()]] = TabularCorrectionFactorRow(kvp.Value)

		return correctionFactorRowsDict

	@property
	def CorrectionIndependentDefinitions(self) -> set[types.CorrectionIndependentDefinition]:
		return {types.CorrectionIndependentDefinition(correctionIndependentDefinition) for correctionIndependentDefinition in self.Entity.CorrectionIndependentDefinitions}

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: float) -> None:
		pass

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: bool) -> None:
		pass

	@overload
	def SetIndependentValue(self, correctionPointId: int, cid: types.CorrectionIndependentDefinition, value: int) -> None:
		pass

	def SetKValue(self, correctionPointId: int, value: float) -> None:
		return self.Entity.SetKValue(correctionPointId, value)

	def SetIndependentValue(self, item1 = None, item2 = None, item3 = None) -> None:
		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, float):
			return self.Entity.SetIndependentValue(item1, item2, item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, bool):
			return self.Entity.SetIndependentValue(item1, item2, item3)

		if isinstance(item1, int) and isinstance(item2, types.CorrectionIndependentDefinition) and isinstance(item3, int):
			return self.Entity.SetIndependentValue(item1, item2, item3)


class OrthotropicAllowableCurvePoint:
	def __init__(self, orthotropicAllowableCurvePoint: _api.OrthotropicAllowableCurvePoint):
		self.Entity = orthotropicAllowableCurvePoint

	@property
	def Property_ID(self) -> types.AllowablePropertyName:
		return types.AllowablePropertyName[self.Entity.AllowablePropertyName.ToString()]

	@property
	def Temperature(self) -> float:
		return self.Entity.Temperature

	@property
	def X(self) -> float:
		return self.Entity.X

	@property
	def Y(self) -> float:
		return self.Entity.Y


class OrthotropicLaminateAllowable:
	def __init__(self, orthotropicLaminateAllowable: _api.OrthotropicLaminateAllowable):
		self.Entity = orthotropicLaminateAllowable

	@property
	def Property_ID(self) -> types.AllowablePropertyName:
		return types.AllowablePropertyName[self.Entity.AllowablePropertyName.ToString()]

	@property
	def Method_ID(self) -> types.AllowableMethodName:
		return types.AllowableMethodName[self.Entity.AllowableMethodName.ToString()]


class OrthotropicTemperature:
	def __init__(self, orthotropicTemperature: _api.OrthotropicTemperature):
		self.Entity = orthotropicTemperature

	@property
	def Temperature(self) -> float:
		return self.Entity.Temperature

	@property
	def Et1(self) -> float:
		return self.Entity.Et1

	@property
	def Et2(self) -> float:
		return self.Entity.Et2

	@property
	def vt12(self) -> float:
		return self.Entity.vt12

	@property
	def Ec1(self) -> float:
		return self.Entity.Ec1

	@property
	def Ec2(self) -> float:
		return self.Entity.Ec2

	@property
	def vc12(self) -> float:
		return self.Entity.vc12

	@property
	def G12(self) -> float:
		return self.Entity.G12

	@property
	def G13(self) -> float:
		return self.Entity.G13

	@property
	def G23(self) -> float:
		return self.Entity.G23

	@property
	def Ftu1(self) -> float:
		return self.Entity.Ftu1

	@property
	def Ftu2(self) -> float:
		return self.Entity.Ftu2

	@property
	def Fcu1(self) -> float:
		return self.Entity.Fcu1

	@property
	def Fcu2(self) -> float:
		return self.Entity.Fcu2

	@property
	def Fsu12(self) -> float:
		return self.Entity.Fsu12

	@property
	def Fsu13(self) -> float:
		return self.Entity.Fsu13

	@property
	def Fsu23(self) -> float:
		return self.Entity.Fsu23

	@property
	def GIc(self) -> float:
		return self.Entity.GIc

	@property
	def alpha1(self) -> float:
		return self.Entity.alpha1

	@property
	def alpha2(self) -> float:
		return self.Entity.alpha2

	@property
	def K1(self) -> float:
		return self.Entity.K1

	@property
	def K2(self) -> float:
		return self.Entity.K2

	@property
	def C(self) -> float:
		return self.Entity.C

	@property
	def etu1(self) -> float:
		return self.Entity.etu1

	@property
	def etu2(self) -> float:
		return self.Entity.etu2

	@property
	def ecu1(self) -> float:
		return self.Entity.ecu1

	@property
	def ecu2(self) -> float:
		return self.Entity.ecu2

	@property
	def ecuoh(self) -> float:
		return self.Entity.ecuoh

	@property
	def ecuai(self) -> float:
		return self.Entity.ecuai

	@property
	def esu12(self) -> float:
		return self.Entity.esu12

	@property
	def Ftu3(self) -> float:
		return self.Entity.Ftu3

	@property
	def GIIc(self) -> float:
		return self.Entity.GIIc

	@property
	def d0Tension(self) -> float:
		return self.Entity.d0Tension

	@property
	def cd(self) -> float:
		return self.Entity.cd

	@property
	def d0Compression(self) -> float:
		return self.Entity.d0Compression

	@property
	def TLt(self) -> float:
		return self.Entity.TLt

	@property
	def TLc(self) -> float:
		return self.Entity.TLc

	@property
	def TTt(self) -> float:
		return self.Entity.TTt

	@property
	def TTc(self) -> float:
		return self.Entity.TTc

	def AddCurvePoint(self, property: types.AllowablePropertyName, x: float, y: float) -> OrthotropicAllowableCurvePoint:
		return OrthotropicAllowableCurvePoint(self.Entity.AddCurvePoint(_types.AllowablePropertyName(property.value), x, y))

	def DeleteCurvePoint(self, property: types.AllowablePropertyName, x: float) -> bool:
		return self.Entity.DeleteCurvePoint(_types.AllowablePropertyName(property.value), x)

	def GetCurvePoint(self, property: types.AllowablePropertyName, x: float) -> OrthotropicAllowableCurvePoint:
		return OrthotropicAllowableCurvePoint(self.Entity.GetCurvePoint(_types.AllowablePropertyName(property.value), x))


class Orthotropic:
	def __init__(self, orthotropic: _api.Orthotropic):
		self.Entity = orthotropic

	@property
	def MaterialFamilyName(self) -> str:
		return self.Entity.MaterialFamilyName

	@property
	def CreationDate(self) -> DateTime:
		return self.Entity.CreationDate

	@property
	def ModificationDate(self) -> DateTime:
		return self.Entity.ModificationDate

	@property
	def Name(self) -> str:
		return self.Entity.Name

	@property
	def Form(self) -> str:
		return self.Entity.Form

	@property
	def Specification(self) -> str:
		return self.Entity.Specification

	@property
	def Basis(self) -> str:
		return self.Entity.Basis

	@property
	def Wet(self) -> bool:
		return self.Entity.Wet

	@property
	def Thickness(self) -> float:
		return self.Entity.Thickness

	@property
	def Density(self) -> float:
		return self.Entity.Density

	@property
	def FiberVolume(self) -> float:
		return self.Entity.FiberVolume

	@property
	def GlassTransition(self) -> float:
		return self.Entity.GlassTransition

	@property
	def Manufacturer(self) -> str:
		return self.Entity.Manufacturer

	@property
	def Processes(self) -> str:
		return self.Entity.Processes

	@property
	def MaterialDescription(self) -> str:
		return self.Entity.MaterialDescription

	@property
	def UserNote(self) -> str:
		return self.Entity.UserNote

	@property
	def BendingCorrectionFactor(self) -> float:
		return self.Entity.BendingCorrectionFactor

	@property
	def FemMaterialId(self) -> int:
		return self.Entity.FemMaterialId

	@property
	def Cost(self) -> float:
		return self.Entity.Cost

	@property
	def BucklingStiffnessKnockdown(self) -> float:
		return self.Entity.BucklingStiffnessKnockdown

	def AddTemperatureProperty(self, temperature: float, et1: float = None, et2: float = None, vt12: float = None, ec1: float = None, ec2: float = None, vc12: float = None, g12: float = None, ftu1: float = None, ftu2: float = None, fcu1: float = None, fcu2: float = None, fsu12: float = None, alpha1: float = None, alpha2: float = None, etu1: float = None, etu2: float = None, ecu1: float = None, ecu2: float = None, esu12: float = None) -> OrthotropicTemperature:
		return OrthotropicTemperature(self.Entity.AddTemperatureProperty(temperature, et1, et2, vt12, ec1, ec2, vc12, g12, ftu1, ftu2, fcu1, fcu2, fsu12, alpha1, alpha2, etu1, etu2, ecu1, ecu2, esu12))

	def DeleteTemperatureProperty(self, temperature: float) -> bool:
		return self.Entity.DeleteTemperatureProperty(temperature)

	def GetTemperature(self, lookupTemperature: float) -> OrthotropicTemperature:
		return OrthotropicTemperature(self.Entity.GetTemperature(lookupTemperature))

	def IsEffectiveLaminate(self) -> bool:
		return self.Entity.IsEffectiveLaminate()

	def HasLaminateAllowable(self, property: types.AllowablePropertyName) -> bool:
		return self.Entity.HasLaminateAllowable(_types.AllowablePropertyName(property.value))

	def AddLaminateAllowable(self, property: types.AllowablePropertyName, method: types.AllowableMethodName) -> OrthotropicLaminateAllowable:
		return OrthotropicLaminateAllowable(self.Entity.AddLaminateAllowable(_types.AllowablePropertyName(property.value), _types.AllowableMethodName(method.value)))

	def GetLaminateAllowable(self, lookupAllowableProperty: types.AllowablePropertyName) -> OrthotropicLaminateAllowable:
		return OrthotropicLaminateAllowable(self.Entity.GetLaminateAllowable(_types.AllowablePropertyName(lookupAllowableProperty.value)))

	def AddEquationCorrectionFactor(self, propertyId: types.CorrectionProperty, correctionId: types.CorrectionId, equationId: types.CorrectionEquation) -> OrthotropicEquationCorrectionFactor:
		return OrthotropicEquationCorrectionFactor(self.Entity.AddEquationCorrectionFactor(_types.CorrectionProperty(propertyId.value), _types.CorrectionId(correctionId.value), _types.CorrectionEquation(equationId.value)))

	def GetEquationCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicEquationCorrectionFactor:
		return OrthotropicEquationCorrectionFactor(self.Entity.GetEquationCorrectionFactor(_types.CorrectionProperty(property.value), _types.CorrectionId(correction.value)))

	def GetTabularCorrectionFactor(self, property: types.CorrectionProperty, correction: types.CorrectionId) -> OrthotropicTabularCorrectionFactor:
		return OrthotropicTabularCorrectionFactor(self.Entity.GetTabularCorrectionFactor(_types.CorrectionProperty(property.value), _types.CorrectionId(correction.value)))

	def Save(self) -> None:
		return self.Entity.Save()


class Vector2d:
	def __init__(self, vector2d: _api.Vector2d):
		self.Entity = vector2d

	@property
	def X(self) -> float:
		return self.Entity.X

	@property
	def Y(self) -> float:
		return self.Entity.Y

	@overload
	def Equals(self, other) -> bool:
		pass

	@overload
	def Equals(self, obj) -> bool:
		pass

	def GetHashCode(self) -> int:
		return self.Entity.GetHashCode()

	def Equals(self, item1 = None) -> bool:
		if isinstance(item1, Vector2d):
			return self.Entity.Equals(item1)

		return self.Entity.Equals(item1)

	def __eq__(self, other):
		return self.Equals(other)

	def __ne__(self, other):
		return not self.Equals(other)


class ElementSet(IdNameEntity):
	def __init__(self, elementSet: _api.ElementSet):
		self.Entity = elementSet

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self.Entity.Elements)


class FemProperty(IdNameEntity):
	def __init__(self, femProperty: _api.FemProperty):
		self.Entity = femProperty

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self.Entity.Elements)


class ElementSetCol(IdEntityCol[ElementSet]):
	def __init__(self, elementSetCol: _api.ElementSetCol):
		self.Entity = elementSetCol
		self.CollectedClass = ElementSet
		self.ElementSetColList = tuple([ElementSet(elementSetCol) for elementSetCol in self.Entity])

	def __getitem__(self, index: int):
		return self.ElementSetColList[index]

	def __iter__(self):
		yield from self.ElementSetColList

	def __len__(self):
		return len(self.ElementSetColList)


class FemPropertyCol(IdEntityCol[FemProperty]):
	def __init__(self, femPropertyCol: _api.FemPropertyCol):
		self.Entity = femPropertyCol
		self.CollectedClass = FemProperty
		self.FemPropertyColList = tuple([FemProperty(femPropertyCol) for femPropertyCol in self.Entity])

	def __getitem__(self, index: int):
		return self.FemPropertyColList[index]

	def __iter__(self):
		yield from self.FemPropertyColList

	def __len__(self):
		return len(self.FemPropertyColList)


class FemDataSet:
	def __init__(self, femDataSet: _api.FemDataSet):
		self.Entity = femDataSet

	@property
	def FemProperties(self) -> FemPropertyCol:
		return FemPropertyCol(self.Entity.FemProperties)

	@property
	def ElementSets(self) -> ElementSetCol:
		return ElementSetCol(self.Entity.ElementSets)


class Ply(IdNameEntity):
	def __init__(self, ply: _api.Ply):
		self.Entity = ply

	@property
	def InnerCurves(self) -> list[int]:
		return [int32 for int32 in self.Entity.InnerCurves]

	@property
	def OuterCurves(self) -> list[int]:
		return [int32 for int32 in self.Entity.OuterCurves]

	@property
	def FiberDirectionCurves(self) -> list[int]:
		return [int32 for int32 in self.Entity.FiberDirectionCurves]

	@property
	def Area(self) -> float:
		return self.Entity.Area

	@property
	def Description(self) -> str:
		return self.Entity.Description

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self.Entity.Elements)

	@property
	def MaterialId(self) -> int:
		return self.Entity.MaterialId

	@property
	def Orientation(self) -> int:
		return self.Entity.Orientation

	@property
	def Sequence(self) -> int:
		return self.Entity.Sequence

	@property
	def StructureId(self) -> int:
		return self.Entity.StructureId

	@property
	def Thickness(self) -> float:
		return self.Entity.Thickness


class Rundeck(IdEntity):
	def __init__(self, rundeck: _api.Rundeck):
		self.Entity = rundeck

	@property
	def InputFilePath(self) -> str:
		return self.Entity.InputFilePath

	@property
	def IsPrimary(self) -> bool:
		return self.Entity.IsPrimary

	@property
	def ResultFilePath(self) -> str:
		return self.Entity.ResultFilePath

	def SetInputFilePath(self, filepath: str) -> RundeckUpdateStatus:
		return RundeckUpdateStatus[self.Entity.SetInputFilePath(filepath).ToString()]

	def SetResultFilePath(self, filepath: str) -> RundeckUpdateStatus:
		return RundeckUpdateStatus[self.Entity.SetResultFilePath(filepath).ToString()]


class BeamLoads:
	def __init__(self, beamLoads: _api.BeamLoads):
		self.Entity = beamLoads

	@property
	def AxialForce(self) -> float:
		return self.Entity.AxialForce

	@property
	def MomentX(self) -> float:
		return self.Entity.MomentX

	@property
	def MomentY(self) -> float:
		return self.Entity.MomentY

	@property
	def ShearX(self) -> float:
		return self.Entity.ShearX

	@property
	def ShearY(self) -> float:
		return self.Entity.ShearY

	@property
	def Torque(self) -> float:
		return self.Entity.Torque


class SectionCut(IdNameEntity):
	def __init__(self, sectionCut: _api.SectionCut):
		self.Entity = sectionCut

	@property
	def ReferencePoint(self) -> types.SectionCutPropertyLocation:
		return types.SectionCutPropertyLocation[self.Entity.SectionCutPropertyLocation.ToString()]

	@property
	def HorizontalVector(self) -> Vector3d:
		return Vector3d(self.Entity.HorizontalVector)

	@property
	def NormalVector(self) -> Vector3d:
		return Vector3d(self.Entity.NormalVector)

	@property
	def OriginVector(self) -> Vector3d:
		return Vector3d(self.Entity.OriginVector)

	@property
	def VerticalVector(self) -> Vector3d:
		return Vector3d(self.Entity.VerticalVector)

	@property
	def MaxAngleBound(self) -> float:
		return self.Entity.MaxAngleBound

	@property
	def MinAngleBound(self) -> float:
		return self.Entity.MinAngleBound

	@property
	def MinStiffnessEihh(self) -> float:
		return self.Entity.MinStiffnessEihh

	@property
	def MinStiffnessEivv(self) -> float:
		return self.Entity.MinStiffnessEivv

	@property
	def MinStiffnessGJ(self) -> float:
		return self.Entity.MinStiffnessGJ

	@property
	def ZoneStiffnessDistribution(self) -> float:
		return self.Entity.ZoneStiffnessDistribution

	@property
	def CN_hmax(self) -> float:
		return self.Entity.CN_hmax

	@property
	def CN_hmin(self) -> float:
		return self.Entity.CN_hmin

	@property
	def CN_vmax(self) -> float:
		return self.Entity.CN_vmax

	@property
	def CN_vmin(self) -> float:
		return self.Entity.CN_vmin

	@property
	def CQ_hmax(self) -> float:
		return self.Entity.CQ_hmax

	@property
	def CQ_hmin(self) -> float:
		return self.Entity.CQ_hmin

	@property
	def CQ_vmax(self) -> float:
		return self.Entity.CQ_vmax

	@property
	def CQ_vmin(self) -> float:
		return self.Entity.CQ_vmin

	@property
	def CG(self) -> Vector2d:
		return Vector2d(self.Entity.CG)

	@property
	def CN(self) -> Vector2d:
		return Vector2d(self.Entity.CN)

	@property
	def CQ(self) -> Vector2d:
		return Vector2d(self.Entity.CQ)

	@property
	def EnclosedArea(self) -> float:
		return self.Entity.EnclosedArea

	@property
	def NumberOfCells(self) -> int:
		return self.Entity.NumberOfCells

	@property
	def EIhh(self) -> float:
		return self.Entity.EIhh

	@property
	def EIhv(self) -> float:
		return self.Entity.EIhv

	@property
	def EIvv(self) -> float:
		return self.Entity.EIvv

	@property
	def GJ(self) -> float:
		return self.Entity.GJ

	@property
	def EA(self) -> float:
		return self.Entity.EA

	@property
	def EImax(self) -> float:
		return self.Entity.EImax

	@property
	def EImin(self) -> float:
		return self.Entity.EImin

	@property
	def PrincipalAngle(self) -> float:
		return self.Entity.PrincipalAngle

	@property
	def Elements(self) -> ElementCol:
		return ElementCol(self.Entity.Elements)

	@property
	def PlateElements(self) -> ElementCol:
		return ElementCol(self.Entity.PlateElements)

	@property
	def BeamElements(self) -> ElementCol:
		return ElementCol(self.Entity.BeamElements)

	def AlignToHorizontalPrincipalAxes(self) -> None:
		return self.Entity.AlignToHorizontalPrincipalAxes()

	def AlignToVerticalPrincipalAxes(self) -> None:
		return self.Entity.AlignToVerticalPrincipalAxes()

	def SetHorizontalVector(self, vector: Vector3d) -> None:
		return self.Entity.SetHorizontalVector(vector.Entity)

	def SetNormalVector(self, vector: Vector3d) -> None:
		return self.Entity.SetNormalVector(vector.Entity)

	def SetOrigin(self, vector: Vector3d) -> None:
		return self.Entity.SetOrigin(vector.Entity)

	def GetBeamLoads(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> BeamLoads:
		return BeamLoads(self.Entity.GetBeamLoads(loadCaseId, _types.LoadSubCaseFactor(factor.value)))

	def InclinationAngle(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return self.Entity.InclinationAngle(loadCaseId, _types.LoadSubCaseFactor(factor.value))

	def HorizontalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return self.Entity.HorizontalIntercept(loadCaseId, _types.LoadSubCaseFactor(factor.value))

	def VerticalIntercept(self, loadCaseId: int, factor: types.LoadSubCaseFactor) -> float:
		return self.Entity.VerticalIntercept(loadCaseId, _types.LoadSubCaseFactor(factor.value))

	def SetElements(self, elements: list[int]) -> bool:
		elementsList = List[int]()
		if elements is not None:
			for thing in elements:
				if thing is not None:
					elementsList.Add(thing)
		return self.Entity.SetElements(elementsList)


class Set(ZoneJointContainer):
	def __init__(self, set: _api.Set):
		self.Entity = set

	@property
	def Joints(self) -> JointCol:
		return JointCol(self.Entity.Joints)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self.Entity.PanelSegments)

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self.Entity.Zones)

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus:
		pass

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		pass

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoints(self, joints: JointCol) -> CollectionModificationStatus:
		pass

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZones(self, zones: ZoneCol) -> CollectionModificationStatus:
		pass

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegments(self, segments: PanelSegmentCol) -> CollectionModificationStatus:
		pass

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self.Entity.AddJoint(item1).ToString()]

		if isinstance(item1, int):
			return super().AddJoint(item1)

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self.Entity.AddPanelSegment(item1).ToString()]

		if isinstance(item1, int):
			return super().AddPanelSegment(item1)

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Zone):
			return CollectionModificationStatus[self.Entity.AddZone(item1).ToString()]

		if isinstance(item1, int):
			return super().AddZone(item1)

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			jointIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						jointIdsList.Add(thing)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self.Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, JointCol):
			return super().RemoveJoints(item1)

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			segmentIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						segmentIdsList.Add(thing)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self.Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, PanelSegmentCol):
			return super().RemovePanelSegments(item1)

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			zoneIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zoneIdsList.Add(thing)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self.Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, ZoneCol):
			return super().RemoveZones(item1)

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return super().RemoveJoint(item1)

		if isinstance(item1, Joint):
			return super().RemoveJoint(item1)

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return super().RemoveZone(item1)

		if isinstance(item1, Zone):
			return super().RemoveZone(item1)

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return super().RemovePanelSegment(item1)

		if isinstance(item1, PanelSegment):
			return super().RemovePanelSegment(item1)


class PlyCol(IdNameEntityCol[Ply]):
	def __init__(self, plyCol: _api.PlyCol):
		self.Entity = plyCol
		self.CollectedClass = Ply
		self.PlyColList = tuple([Ply(plyCol) for plyCol in self.Entity])

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self.Entity.Delete(id).ToString()]

	def DeleteAll(self) -> None:
		return self.Entity.DeleteAll()

	def ExportToCSV(self, filepath: str) -> None:
		return self.Entity.ExportToCSV(filepath)

	def ImportCSV(self, filepath: str) -> None:
		return self.Entity.ImportCSV(filepath)

	@overload
	def Get(self, name: str) -> Ply:
		pass

	@overload
	def Get(self, id: int) -> Ply:
		pass

	def Get(self, item1 = None) -> Ply:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.PlyColList[index]

	def __iter__(self):
		yield from self.PlyColList

	def __len__(self):
		return len(self.PlyColList)


class Structure(ZoneJointContainer):
	def __init__(self, structure: _api.Structure):
		self.Entity = structure

	@property
	def Plies(self) -> PlyCol:
		return PlyCol(self.Entity.Plies)

	@property
	def Joints(self) -> JointCol:
		return JointCol(self.Entity.Joints)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self.Entity.PanelSegments)

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self.Entity.Zones)

	def ExportVCP(self, fileName: str) -> None:
		return self.Entity.ExportVCP(fileName)

	def AddElements(self, elementIds: tuple[int]) -> CollectionModificationStatus:
		elementIdsList = List[int]()
		if elementIds is not None:
			for thing in elementIds:
				if thing is not None:
					elementIdsList.Add(thing)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return CollectionModificationStatus[self.Entity.AddElements(elementIdsEnumerable).ToString()]

	@overload
	def AddJoint(self, joint: Joint) -> CollectionModificationStatus:
		pass

	@overload
	def AddPanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		pass

	def AddPfemProperties(self, pfemPropertyIds: tuple[int]) -> CollectionModificationStatus:
		pfemPropertyIdsList = List[int]()
		if pfemPropertyIds is not None:
			for thing in pfemPropertyIds:
				if thing is not None:
					pfemPropertyIdsList.Add(thing)
		pfemPropertyIdsEnumerable = IEnumerable(pfemPropertyIdsList)
		return CollectionModificationStatus[self.Entity.AddPfemProperties(pfemPropertyIdsEnumerable).ToString()]

	@overload
	def AddZone(self, zone: Zone) -> CollectionModificationStatus:
		pass

	def CreateZone(self, elementIds: tuple[int], name: str = None) -> None:
		elementIdsList = List[int]()
		if elementIds is not None:
			for thing in elementIds:
				if thing is not None:
					elementIdsList.Add(thing)
		elementIdsEnumerable = IEnumerable(elementIdsList)
		return self.Entity.CreateZone(elementIdsEnumerable, name)

	def CreatePanelSegment(self, discreteTechnique: types.DiscreteTechnique, discreteElementLkp: dict[types.DiscreteDefinitionType, list[int]], name: str = None) -> int:
		return self.Entity.CreatePanelSegment(_types.DiscreteTechnique(discreteTechnique.value), discreteElementLkp.Entity, name)

	@overload
	def Remove(self, zoneIds: tuple[int], jointIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def Remove(self, zoneIds: tuple[int], jointIds: tuple[int], panelSegmentIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoints(self, jointIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegments(self, segmentIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZones(self, zoneIds: tuple[int]) -> CollectionModificationStatus:
		pass

	@overload
	def AddJoint(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoint(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveJoints(self, joints: JointCol) -> CollectionModificationStatus:
		pass

	@overload
	def AddZone(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZone(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZone(self, zone: Zone) -> CollectionModificationStatus:
		pass

	@overload
	def RemoveZones(self, zones: ZoneCol) -> CollectionModificationStatus:
		pass

	@overload
	def AddPanelSegment(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegment(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegment(self, segment: PanelSegment) -> CollectionModificationStatus:
		pass

	@overload
	def RemovePanelSegments(self, segments: PanelSegmentCol) -> CollectionModificationStatus:
		pass

	def AddJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Joint):
			return CollectionModificationStatus[self.Entity.AddJoint(item1).ToString()]

		if isinstance(item1, int):
			return super().AddJoint(item1)

	def AddPanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, PanelSegment):
			return CollectionModificationStatus[self.Entity.AddPanelSegment(item1).ToString()]

		if isinstance(item1, int):
			return super().AddPanelSegment(item1)

	def AddZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Zone):
			return CollectionModificationStatus[self.Entity.AddZone(item1).ToString()]

		if isinstance(item1, int):
			return super().AddZone(item1)

	def Remove(self, item1 = None, item2 = None, item3 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple) and isinstance(item2, tuple):
			zoneIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zoneIdsList.Add(thing)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = List[int]()
			if item2 is not None:
				for thing in item2:
					if thing is not None:
						jointIdsList.Add(thing)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self.Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable).ToString()]

		if isinstance(item1, tuple) and isinstance(item2, tuple) and isinstance(item3, tuple):
			zoneIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zoneIdsList.Add(thing)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			jointIdsList = List[int]()
			if item2 is not None:
				for thing in item2:
					if thing is not None:
						jointIdsList.Add(thing)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			panelSegmentIdsList = List[int]()
			if item3 is not None:
				for thing in item3:
					if thing is not None:
						panelSegmentIdsList.Add(thing)
			panelSegmentIdsEnumerable = IEnumerable(panelSegmentIdsList)
			return CollectionModificationStatus[self.Entity.Remove(zoneIdsEnumerable, jointIdsEnumerable, panelSegmentIdsEnumerable).ToString()]

	def RemoveJoints(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			jointIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						jointIdsList.Add(thing)
			jointIdsEnumerable = IEnumerable(jointIdsList)
			return CollectionModificationStatus[self.Entity.RemoveJoints(jointIdsEnumerable).ToString()]

		if isinstance(item1, JointCol):
			return super().RemoveJoints(item1)

	def RemovePanelSegments(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			segmentIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						segmentIdsList.Add(thing)
			segmentIdsEnumerable = IEnumerable(segmentIdsList)
			return CollectionModificationStatus[self.Entity.RemovePanelSegments(segmentIdsEnumerable).ToString()]

		if isinstance(item1, PanelSegmentCol):
			return super().RemovePanelSegments(item1)

	def RemoveZones(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, tuple):
			zoneIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zoneIdsList.Add(thing)
			zoneIdsEnumerable = IEnumerable(zoneIdsList)
			return CollectionModificationStatus[self.Entity.RemoveZones(zoneIdsEnumerable).ToString()]

		if isinstance(item1, ZoneCol):
			return super().RemoveZones(item1)

	def RemoveJoint(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return super().RemoveJoint(item1)

		if isinstance(item1, Joint):
			return super().RemoveJoint(item1)

	def RemoveZone(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return super().RemoveZone(item1)

		if isinstance(item1, Zone):
			return super().RemoveZone(item1)

	def RemovePanelSegment(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, int):
			return super().RemovePanelSegment(item1)

		if isinstance(item1, PanelSegment):
			return super().RemovePanelSegment(item1)


class AnalysisPropertyCol(IdNameEntityCol[AnalysisProperty]):
	def __init__(self, analysisPropertyCol: _api.AnalysisPropertyCol):
		self.Entity = analysisPropertyCol
		self.CollectedClass = AnalysisProperty
		self.AnalysisPropertyColList = tuple([AnalysisProperty(analysisPropertyCol) for analysisPropertyCol in self.Entity])

	@overload
	def Get(self, name: str) -> AnalysisProperty:
		pass

	@overload
	def Get(self, id: int) -> AnalysisProperty:
		pass

	def Get(self, item1 = None) -> AnalysisProperty:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.AnalysisPropertyColList[index]

	def __iter__(self):
		yield from self.AnalysisPropertyColList

	def __len__(self):
		return len(self.AnalysisPropertyColList)


class DesignPropertyCol(IdNameEntityCol[DesignProperty]):
	def __init__(self, designPropertyCol: _api.DesignPropertyCol):
		self.Entity = designPropertyCol
		self.CollectedClass = DesignProperty
		self.DesignPropertyColList = tuple([DesignProperty(designPropertyCol) for designPropertyCol in self.Entity])

	@overload
	def Get(self, name: str) -> DesignProperty:
		pass

	@overload
	def Get(self, id: int) -> DesignProperty:
		pass

	def Get(self, item1 = None) -> DesignProperty:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.DesignPropertyColList[index]

	def __iter__(self):
		yield from self.DesignPropertyColList

	def __len__(self):
		return len(self.DesignPropertyColList)


class LoadPropertyCol(IdNameEntityCol[LoadProperty]):
	def __init__(self, loadPropertyCol: _api.LoadPropertyCol):
		self.Entity = loadPropertyCol
		self.CollectedClass = LoadProperty
		self.LoadPropertyColList = tuple([LoadProperty(loadPropertyCol) for loadPropertyCol in self.Entity])

	@overload
	def Get(self, name: str) -> LoadProperty:
		pass

	@overload
	def Get(self, id: int) -> LoadProperty:
		pass

	def Get(self, item1 = None) -> LoadProperty:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.LoadPropertyColList[index]

	def __iter__(self):
		yield from self.LoadPropertyColList

	def __len__(self):
		return len(self.LoadPropertyColList)


class DesignLoadCol(IdNameEntityCol[DesignLoad]):
	def __init__(self, designLoadCol: _api.DesignLoadCol):
		self.Entity = designLoadCol
		self.CollectedClass = DesignLoad
		self.DesignLoadColList = tuple([DesignLoad(designLoadCol) for designLoadCol in self.Entity])

	@overload
	def Get(self, name: str) -> DesignLoad:
		pass

	@overload
	def Get(self, id: int) -> DesignLoad:
		pass

	def Get(self, item1 = None) -> DesignLoad:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.DesignLoadColList[index]

	def __iter__(self):
		yield from self.DesignLoadColList

	def __len__(self):
		return len(self.DesignLoadColList)


class DiscreteFieldTableCol(IdNameEntityCol[DiscreteFieldTable]):
	def __init__(self, discreteFieldTableCol: _api.DiscreteFieldTableCol):
		self.Entity = discreteFieldTableCol
		self.CollectedClass = DiscreteFieldTable
		self.DiscreteFieldTableColList = tuple([DiscreteFieldTable(discreteFieldTableCol) for discreteFieldTableCol in self.Entity])

	def Create(self, name: str, entityType: types.DiscreteFieldPhysicalEntityType, dataType: types.DiscreteFieldDataType) -> int:
		return self.Entity.Create(name, _types.DiscreteFieldPhysicalEntityType(entityType.value), _types.DiscreteFieldDataType(dataType.value))

	def CreateFromVCP(self, filepath: str) -> list[int]:
		return list[int](self.Entity.CreateFromVCP(filepath))

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self.Entity.Delete(id).ToString()]

	def CreateByPointMapToElements(self, elementIds: list[int], discreteFieldIds: list[int], suffix: str = None, tolerance: float = None) -> None:
		elementIdsList = List[int]()
		if elementIds is not None:
			for thing in elementIds:
				if thing is not None:
					elementIdsList.Add(thing)
		discreteFieldIdsList = List[int]()
		if discreteFieldIds is not None:
			for thing in discreteFieldIds:
				if thing is not None:
					discreteFieldIdsList.Add(thing)
		return self.Entity.CreateByPointMapToElements(elementIdsList, discreteFieldIdsList, suffix, tolerance)

	@overload
	def Get(self, name: str) -> DiscreteFieldTable:
		pass

	@overload
	def Get(self, id: int) -> DiscreteFieldTable:
		pass

	def Get(self, item1 = None) -> DiscreteFieldTable:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.DiscreteFieldTableColList[index]

	def __iter__(self):
		yield from self.DiscreteFieldTableColList

	def __len__(self):
		return len(self.DiscreteFieldTableColList)


class ZoneJointContainerCol(IdNameEntityCol, Generic[T]):
	def __init__(self, zoneJointContainerCol: _api.ZoneJointContainerCol):
		self.Entity = zoneJointContainerCol
		self.CollectedClass = T
		self.ZoneJointContainerColList = tuple([T(zoneJointContainerCol) for zoneJointContainerCol in self.Entity])

	@abstractmethod
	def Create(self, name: str) -> bool:
		return self.Entity.Create(name)

	@overload
	def Get(self, name: str) -> T:
		pass

	@overload
	def Get(self, id: int) -> T:
		pass

	def Get(self, item1 = None) -> T:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.ZoneJointContainerColList[index]

	def __iter__(self):
		yield from self.ZoneJointContainerColList

	def __len__(self):
		return len(self.ZoneJointContainerColList)


class RundeckCol(IdEntityCol[Rundeck]):
	def __init__(self, rundeckCol: _api.RundeckCol):
		self.Entity = rundeckCol
		self.CollectedClass = Rundeck
		self.RundeckColList = tuple([Rundeck(rundeckCol) for rundeckCol in self.Entity])

	def AddRundeck(self, inputPath: str, resultPath: str = None) -> RundeckCreationStatus:
		return RundeckCreationStatus[self.Entity.AddRundeck(inputPath, resultPath).ToString()]

	def ReassignPrimary(self, id: int) -> RundeckUpdateStatus:
		return RundeckUpdateStatus[self.Entity.ReassignPrimary(id).ToString()]

	def RemoveRundeck(self, id: int) -> RundeckRemoveStatus:
		return RundeckRemoveStatus[self.Entity.RemoveRundeck(id).ToString()]

	def __getitem__(self, index: int):
		return self.RundeckColList[index]

	def __iter__(self):
		yield from self.RundeckColList

	def __len__(self):
		return len(self.RundeckColList)


class SectionCutCol(IdNameEntityCol[SectionCut]):
	def __init__(self, sectionCutCol: _api.SectionCutCol):
		self.Entity = sectionCutCol
		self.CollectedClass = SectionCut
		self.SectionCutColList = tuple([SectionCut(sectionCutCol) for sectionCutCol in self.Entity])

	def Create(self, name: str, origin: Vector3d, normal: Vector3d, horizontal: Vector3d) -> None:
		return self.Entity.Create(name, origin.Entity, normal.Entity, horizontal.Entity)

	def Delete(self, id: int) -> CollectionModificationStatus:
		return CollectionModificationStatus[self.Entity.Delete(id).ToString()]

	@overload
	def Get(self, name: str) -> SectionCut:
		pass

	@overload
	def Get(self, id: int) -> SectionCut:
		pass

	def Get(self, item1 = None) -> SectionCut:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.SectionCutColList[index]

	def __iter__(self):
		yield from self.SectionCutColList

	def __len__(self):
		return len(self.SectionCutColList)


class SetCol(ZoneJointContainerCol[Set]):
	def __init__(self, setCol: _api.SetCol):
		self.Entity = setCol
		self.CollectedClass = Set
		self.SetColList = tuple([Set(setCol) for setCol in self.Entity])

	def Create(self, name: str) -> bool:
		return self.Entity.Create(name)

	@overload
	def Get(self, name: str) -> Set:
		pass

	@overload
	def Get(self, id: int) -> Set:
		pass

	def Get(self, item1 = None) -> Set:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.SetColList[index]

	def __iter__(self):
		yield from self.SetColList

	def __len__(self):
		return len(self.SetColList)


class StructureCol(ZoneJointContainerCol[Structure]):
	def __init__(self, structureCol: _api.StructureCol):
		self.Entity = structureCol
		self.CollectedClass = Structure
		self.StructureColList = tuple([Structure(structureCol) for structureCol in self.Entity])

	def Create(self, name: str) -> bool:
		return self.Entity.Create(name)

	@overload
	def DeleteStructure(self, structure: Structure) -> CollectionModificationStatus:
		pass

	@overload
	def DeleteStructure(self, id: int) -> CollectionModificationStatus:
		pass

	@overload
	def Get(self, name: str) -> Structure:
		pass

	@overload
	def Get(self, id: int) -> Structure:
		pass

	def DeleteStructure(self, item1 = None) -> CollectionModificationStatus:
		if isinstance(item1, Structure):
			return CollectionModificationStatus[self.Entity.DeleteStructure(item1).ToString()]

		if isinstance(item1, int):
			return CollectionModificationStatus[self.Entity.DeleteStructure(item1).ToString()]

	def Get(self, item1 = None) -> Structure:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.StructureColList[index]

	def __iter__(self):
		yield from self.StructureColList

	def __len__(self):
		return len(self.StructureColList)


class Project:
	def __init__(self, project: _api.Project):
		self.Entity = project

	@property
	def WorkingFolder(self) -> str:
		return self.Entity.WorkingFolder

	@property
	def FemDataSet(self) -> FemDataSet:
		return FemDataSet(self.Entity.FemDataSet)

	@property
	def Beams(self) -> ZoneCol:
		return ZoneCol(self.Entity.Beams)

	@property
	def Id(self) -> int:
		return self.Entity.Id

	@property
	def Joints(self) -> JointCol:
		return JointCol(self.Entity.Joints)

	@property
	def Name(self) -> str:
		return self.Entity.Name

	@property
	def Panels(self) -> ZoneCol:
		return ZoneCol(self.Entity.Panels)

	@property
	def Rundecks(self) -> RundeckCol:
		return RundeckCol(self.Entity.Rundecks)

	@property
	def Sets(self) -> SetCol:
		return SetCol(self.Entity.Sets)

	@property
	def Structures(self) -> StructureCol:
		return StructureCol(self.Entity.Structures)

	@property
	def Zones(self) -> ZoneCol:
		return ZoneCol(self.Entity.Zones)

	@property
	def PanelSegments(self) -> PanelSegmentCol:
		return PanelSegmentCol(self.Entity.PanelSegments)

	@property
	def SectionCuts(self) -> SectionCutCol:
		return SectionCutCol(self.Entity.SectionCuts)

	@property
	def DesignLoads(self) -> DesignLoadCol:
		return DesignLoadCol(self.Entity.DesignLoads)

	@property
	def DiscreteFieldTables(self) -> DiscreteFieldTableCol:
		return DiscreteFieldTableCol(self.Entity.DiscreteFieldTables)

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		return AnalysisPropertyCol(self.Entity.AnalysisProperties)

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		return DesignPropertyCol(self.Entity.DesignProperties)

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		return LoadPropertyCol(self.Entity.LoadProperties)

	@property
	def FemFormat(self) -> types.ProjectModelFormat:
		return types.ProjectModelFormat[self.Entity.ProjectModelFormat.ToString()]

	def Upload(self, uploadSetName: str, company: str, program: str, tags: list[str], notes: str, zoneIds: set[int], jointIds: set[int]) -> bool:
		tagsList = List[str]()
		if tags is not None:
			for thing in tags:
				if thing is not None:
					tagsList.Add(thing)
		return self.Entity.Upload(uploadSetName, company, program, tagsList, notes, zoneIds.Entity, jointIds.Entity)

	def GetDashboardCompanies(self) -> list[str]:
		return list[str](self.Entity.GetDashboardCompanies())

	def GetDashboardPrograms(self, companyName: str) -> list[str]:
		return list[str](self.Entity.GetDashboardPrograms(companyName))

	def GetDashboardTags(self, companyName: str) -> list[str]:
		return list[str](self.Entity.GetDashboardTags(companyName))

	def Dispose(self) -> None:
		return self.Entity.Dispose()

	def GetConceptName(self, zoneId: int) -> str:
		return self.Entity.GetConceptName(zoneId)

	def GetJointAnalysisResults(self, joints: list[Joint] = None, analysisResultType: AnalysisResultToReturn = AnalysisResultToReturn.Minimum) -> dict[int, dict[types.JointObject, dict[types.AnalysisId, tuple[float, types.MarginCode]]]]:
		jointsList = List[_api.Joint]()
		if joints is not None:
			for thing in joints:
				if thing is not None:
					jointsList.Add(thing.Entity)
		return dict[int, dict[types.JointObject, dict[types.AnalysisId, tuple[float, types.MarginCode]]]](self.Entity.GetJointAnalysisResults(joints if joints is None else jointsList, _types.AnalysisResultToReturn(analysisResultType.value)))

	def GetObjectName(self, zoneId: int, objectId: int) -> str:
		return self.Entity.GetObjectName(zoneId, objectId)

	def GetZoneConceptAnalysisResults(self, zones: list[Zone] = None, analysisResultType: AnalysisResultToReturn = AnalysisResultToReturn.Minimum) -> dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]]:
		zonesList = List[_api.Zone]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesList.Add(thing.Entity)
		return dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]](self.Entity.GetZoneConceptAnalysisResults(zones if zones is None else zonesList, _types.AnalysisResultToReturn(analysisResultType.value)))

	def GetZoneObjectAnalysisResults(self, zones: list[Zone] = None, analysisResultType: AnalysisResultToReturn = AnalysisResultToReturn.Minimum) -> dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]]:
		zonesList = List[_api.Zone]()
		if zones is not None:
			for thing in zones:
				if thing is not None:
					zonesList.Add(thing.Entity)
		return dict[Zone, dict[tuple[int, int], tuple[float, types.MarginCode]]](self.Entity.GetZoneObjectAnalysisResults(zones if zones is None else zonesList, _types.AnalysisResultToReturn(analysisResultType.value)))

	def ImportFem(self) -> None:
		return self.Entity.ImportFem()

	def SetFemFormat(self, femFormat: types.ProjectModelFormat) -> None:
		return self.Entity.SetFemFormat(_types.ProjectModelFormat(femFormat.value))

	def SetFemUnits(self, femForceId: DbForceUnit, femLengthId: DbLengthUnit, femMassId: DbMassUnit, femTemperatureId: DbTemperatureUnit) -> SetUnitsStatus:
		return SetUnitsStatus[self.Entity.SetFemUnits(_types.DbForceUnit(femForceId.value), _types.DbLengthUnit(femLengthId.value), _types.DbMassUnit(femMassId.value), _types.DbTemperatureUnit(femTemperatureId.value)).ToString()]

	def SizeJoints(self, joints: list[Joint] = None) -> tuple[bool, str, set[int]]:
		jointsList = List[_api.Joint]()
		if joints is not None:
			for thing in joints:
				if thing is not None:
					jointsList.Add(thing.Entity)
		result = self.Entity.SizeJoints(joints if joints is None else jointsList)
		return tuple([result.Item1, result.Item2, result.Item3])

	@overload
	def AnalyzeZones(self, zones: list[Zone] = None) -> tuple[bool, str]:
		pass

	@overload
	def AnalyzeZones(self, zoneIds: list[int]) -> tuple[bool, str]:
		pass

	@overload
	def SizeZones(self, zones: list[Zone] = None) -> tuple[bool, str]:
		pass

	@overload
	def SizeZones(self, zoneIds: list[int]) -> tuple[bool, str]:
		pass

	def UnimportFemAsync(self) -> Task:
		return Task(self.Entity.UnimportFemAsync())

	def ExportFem(self, destinationFolder: str) -> None:
		return self.Entity.ExportFem(destinationFolder)

	def ImportCad(self, filePath: str) -> None:
		return self.Entity.ImportCad(filePath)

	@overload
	def ExportCad(self, filePath: str) -> None:
		pass

	@overload
	def ExportCad(self, cadIds: tuple[int], filePath: str) -> None:
		pass

	def AnalyzeZones(self, item1 = None) -> tuple[bool, str]:
		if isinstance(item1, list):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing.Entity)
			result = self.Entity.AnalyzeZones(item1 if item1 is None else zonesList)
			return tuple([result.Item1, result.Item2])

		if isinstance(item1, list):
			zoneIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zoneIdsList.Add(thing)
			result = self.Entity.AnalyzeZones(zoneIdsList)
			return tuple([result.Item1, result.Item2])

	def SizeZones(self, item1 = None) -> tuple[bool, str]:
		if isinstance(item1, list):
			zonesList = List[_api.Zone]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zonesList.Add(thing.Entity)
			result = self.Entity.SizeZones(item1 if item1 is None else zonesList)
			return tuple([result.Item1, result.Item2])

		if isinstance(item1, list):
			zoneIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						zoneIdsList.Add(thing)
			result = self.Entity.SizeZones(zoneIdsList)
			return tuple([result.Item1, result.Item2])

	def ExportCad(self, item1 = None, item2 = None) -> None:
		if isinstance(item1, str):
			return self.Entity.ExportCad(item1)

		if isinstance(item1, tuple) and isinstance(item2, str):
			cadIdsList = List[int]()
			if item1 is not None:
				for thing in item1:
					if thing is not None:
						cadIdsList.Add(thing)
			cadIdsEnumerable = IEnumerable(cadIdsList)
			return self.Entity.ExportCad(cadIdsEnumerable, item2)


class ProjectInfo(IdNameEntityRenameable):
	def __init__(self, projectInfo: _api.ProjectInfo):
		self.Entity = projectInfo


class FailureModeCategoryCol(IdNameEntityCol[FailureModeCategory]):
	def __init__(self, failureModeCategoryCol: _api.FailureModeCategoryCol):
		self.Entity = failureModeCategoryCol
		self.CollectedClass = FailureModeCategory
		self.FailureModeCategoryColList = tuple([FailureModeCategory(failureModeCategoryCol) for failureModeCategoryCol in self.Entity])

	@overload
	def Get(self, name: str) -> FailureModeCategory:
		pass

	@overload
	def Get(self, id: int) -> FailureModeCategory:
		pass

	def Get(self, item1 = None) -> FailureModeCategory:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.FailureModeCategoryColList[index]

	def __iter__(self):
		yield from self.FailureModeCategoryColList

	def __len__(self):
		return len(self.FailureModeCategoryColList)


class FoamCol(Generic[T]):
	def __init__(self, foamCol: _api.FoamCol):
		self.Entity = foamCol
		self.FoamColList = tuple([Foam(foamCol) for foamCol in self.Entity])

	def Count(self) -> int:
		return self.Entity.Count()

	def Get(self, materialName: str) -> Foam:
		return Foam(self.Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self.Entity.Contains(materialName)

	def GetEnumerator(self) -> tuple[T]:
		enumerator = self.Entity.GetEnumerator()
		tup = ()
		for item in enumerator:
			tup += (item)

		return tup

	def Create(self, newMaterialName: str, materialFamilyName: str, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Create(newMaterialName, materialFamilyName, density, femId).ToString()]

	def Copy(self, fmToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Copy(fmToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self.Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.FoamColList[index]

	def __iter__(self):
		yield from self.FoamColList

	def __len__(self):
		return len(self.FoamColList)


class HoneycombCol(Generic[T]):
	def __init__(self, honeycombCol: _api.HoneycombCol):
		self.Entity = honeycombCol
		self.HoneycombColList = tuple([Honeycomb(honeycombCol) for honeycombCol in self.Entity])

	def Count(self) -> int:
		return self.Entity.Count()

	def Get(self, materialName: str) -> Honeycomb:
		return Honeycomb(self.Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self.Entity.Contains(materialName)

	def GetEnumerator(self) -> tuple[T]:
		enumerator = self.Entity.GetEnumerator()
		tup = ()
		for item in enumerator:
			tup += (item)

		return tup

	def Create(self, newMaterialName: str, materialFamilyName: str, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Create(newMaterialName, materialFamilyName, density, femId).ToString()]

	def Copy(self, honeyToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Copy(honeyToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self.Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.HoneycombColList[index]

	def __iter__(self):
		yield from self.HoneycombColList

	def __len__(self):
		return len(self.HoneycombColList)


class IsotropicCol(Generic[T]):
	def __init__(self, isotropicCol: _api.IsotropicCol):
		self.Entity = isotropicCol
		self.IsotropicColList = tuple([Isotropic(isotropicCol) for isotropicCol in self.Entity])

	def Count(self) -> int:
		return self.Entity.Count()

	def Get(self, materialName: str) -> Isotropic:
		return Isotropic(self.Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self.Entity.Contains(materialName)

	def GetEnumerator(self) -> tuple[T]:
		enumerator = self.Entity.GetEnumerator()
		tup = ()
		for item in enumerator:
			tup += (item)

		return tup

	def Create(self, newMaterialName: str, materialFamilyName: str, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Create(newMaterialName, materialFamilyName, density, femId).ToString()]

	def Copy(self, isoToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Copy(isoToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self.Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.IsotropicColList[index]

	def __iter__(self):
		yield from self.IsotropicColList

	def __len__(self):
		return len(self.IsotropicColList)


class OrthotropicCol(Generic[T]):
	def __init__(self, orthotropicCol: _api.OrthotropicCol):
		self.Entity = orthotropicCol
		self.OrthotropicColList = tuple([Orthotropic(orthotropicCol) for orthotropicCol in self.Entity])

	def Count(self) -> int:
		return self.Entity.Count()

	def Get(self, materialName: str) -> Orthotropic:
		return Orthotropic(self.Entity.Get(materialName))

	def Contains(self, materialName: str) -> bool:
		return self.Entity.Contains(materialName)

	def GetEnumerator(self) -> tuple[T]:
		enumerator = self.Entity.GetEnumerator()
		tup = ()
		for item in enumerator:
			tup += (item)

		return tup

	def Create(self, newMaterialName: str, materialFamilyName: str, thickness: float, density: float, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Create(newMaterialName, materialFamilyName, thickness, density, femId).ToString()]

	def Copy(self, orthoToCopyName: str, newMaterialName: str, femId: int = 0) -> MaterialCreationStatus:
		return MaterialCreationStatus[self.Entity.Copy(orthoToCopyName, newMaterialName, femId).ToString()]

	def Delete(self, materialName: str) -> bool:
		return self.Entity.Delete(materialName)

	def __getitem__(self, index: int):
		return self.OrthotropicColList[index]

	def __iter__(self):
		yield from self.OrthotropicColList

	def __len__(self):
		return len(self.OrthotropicColList)


class ProjectInfoCol(IdNameEntityCol[ProjectInfo]):
	def __init__(self, projectInfoCol: _api.ProjectInfoCol):
		self.Entity = projectInfoCol
		self.CollectedClass = ProjectInfo
		self.ProjectInfoColList = tuple([ProjectInfo(projectInfoCol) for projectInfoCol in self.Entity])

	@overload
	def Get(self, name: str) -> ProjectInfo:
		pass

	@overload
	def Get(self, id: int) -> ProjectInfo:
		pass

	def Get(self, item1 = None) -> ProjectInfo:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.ProjectInfoColList[index]

	def __iter__(self):
		yield from self.ProjectInfoColList

	def __len__(self):
		return len(self.ProjectInfoColList)


class Application:
	def __init__(self, application: _api.Application):
		self.Entity = application

	@property
	def DatabasePath(self) -> str:
		return self.Entity.DatabasePath

	@property
	def ActiveProject(self) -> Project:
		return Project(self.Entity.ActiveProject)

	@property
	def UiRunnerMode(self) -> bool:
		return self.Entity.UiRunnerMode

	@property
	def Version(self) -> str:
		return self.Entity.Version

	@property
	def FailureModeCategories(self) -> FailureModeCategoryCol:
		return FailureModeCategoryCol(self.Entity.FailureModeCategories)

	@property
	def FailureModes(self) -> FailureModeCol:
		return FailureModeCol(self.Entity.FailureModes)

	@property
	def Foams(self) -> FoamCol:
		return FoamCol(self.Entity.Foams)

	@property
	def Honeycombs(self) -> HoneycombCol:
		return HoneycombCol(self.Entity.Honeycombs)

	@property
	def Isotropics(self) -> IsotropicCol:
		return IsotropicCol(self.Entity.Isotropics)

	@property
	def AnalysisProperties(self) -> AnalysisPropertyCol:
		return AnalysisPropertyCol(self.Entity.AnalysisProperties)

	@property
	def DesignProperties(self) -> DesignPropertyCol:
		return DesignPropertyCol(self.Entity.DesignProperties)

	@property
	def LoadProperties(self) -> LoadPropertyCol:
		return LoadPropertyCol(self.Entity.LoadProperties)

	@property
	def Orthotropics(self) -> OrthotropicCol:
		return OrthotropicCol(self.Entity.Orthotropics)

	@property
	def ProjectInfos(self) -> ProjectInfoCol:
		return ProjectInfoCol(self.Entity.ProjectInfos)

	@property
	def UserName(self) -> str:
		return self.Entity.UserName

	def CloseDatabase(self, delay: int = 0) -> None:
		return self.Entity.CloseDatabase(delay)

	def CopyProject(self, projectId: int, newName: str, copyDesignProperties: bool = True, copyAnalysisProperties: bool = True, copyLoadProperties: bool = True, copyWorkingFolder: bool = True) -> int:
		return self.Entity.CopyProject(projectId, newName, copyDesignProperties, copyAnalysisProperties, copyLoadProperties, copyWorkingFolder)

	def CreateAnalysisProperty(self, name: str, type: types.FamilyCategory) -> int:
		return self.Entity.CreateAnalysisProperty(name, _types.FamilyCategory(type.value))

	def CreateFailureMode(self, failureModeCategoryId: int) -> int:
		return self.Entity.CreateFailureMode(failureModeCategoryId)

	def CreateDatabaseFromTemplate(self, templateName: str, newPath: str) -> CreateDatabaseStatus:
		return CreateDatabaseStatus[self.Entity.CreateDatabaseFromTemplate(templateName, newPath).ToString()]

	def CreateProject(self, projectName: str) -> ProjectCreationStatus:
		return ProjectCreationStatus[self.Entity.CreateProject(projectName).ToString()]

	def DeleteAnalysisProperty(self, id: int) -> None:
		return self.Entity.DeleteAnalysisProperty(id)

	def DeleteProject(self, projectName: str) -> ProjectDeletionStatus:
		return ProjectDeletionStatus[self.Entity.DeleteProject(projectName).ToString()]

	def Dispose(self) -> None:
		return self.Entity.Dispose()

	def GetAnalyses(self) -> dict[int, AnalysisDefinition]:
		return dict[int, AnalysisDefinition](self.Entity.GetAnalyses())

	def Login(self, userName: str, password: str = "") -> None:
		return self.Entity.Login(userName, password)

	def Migrate(self, databasePath: str) -> str:
		return self.Entity.Migrate(databasePath)

	def OpenDatabase(self, databasePath: str) -> None:
		return self.Entity.OpenDatabase(databasePath)

	def SelectProject(self, projectName: str) -> Project:
		return Project(self.Entity.SelectProject(projectName))


class JointDesignProperty(DesignProperty):
	def __init__(self, jointDesignProperty: _api.JointDesignProperty):
		self.Entity = jointDesignProperty


class ToolingConstraint(IdNameEntity):
	def __init__(self, toolingConstraint: _api.ToolingConstraint):
		self.Entity = toolingConstraint

	@property
	def ConstraintMax(self) -> float:
		return self.Entity.ConstraintMax

	@property
	def ConstraintMin(self) -> float:
		return self.Entity.ConstraintMin

	@property
	def ConstraintValue(self) -> float:
		return self.Entity.ConstraintValue

	@property
	def ToolingSelectionType(self) -> types.ToolingSelectionType:
		return types.ToolingSelectionType[self.Entity.ToolingSelectionType.ToString()]

	def SetToAnyValue(self) -> None:
		return self.Entity.SetToAnyValue()

	def SetToInequality(self, value: float) -> None:
		return self.Entity.SetToInequality(value)

	def SetToRange(self, min: float, max: float) -> None:
		return self.Entity.SetToRange(min, max)

	def SetToValue(self, value: float) -> None:
		return self.Entity.SetToValue(value)


class DesignVariableMaterial:
	def __init__(self, designVariableMaterial: _api.DesignVariableMaterial):
		self.Entity = designVariableMaterial

	@property
	def MaterialId(self) -> int:
		return self.Entity.MaterialId


class DesignVariable(IdEntity):
	def __init__(self, designVariable: _api.DesignVariable):
		self.Entity = designVariable

	@property
	def AllowMaterials(self) -> bool:
		return self.Entity.AllowMaterials

	@property
	def Max(self) -> float:
		return self.Entity.Max

	@property
	def Min(self) -> float:
		return self.Entity.Min

	@property
	def Name(self) -> str:
		return self.Entity.Name

	@property
	def StepSize(self) -> float:
		return self.Entity.StepSize

	@property
	def UseAnalysis(self) -> bool:
		return self.Entity.UseAnalysis

	def AddMaterials(self, materialIds: list[int]) -> None:
		materialIdsList = List[int]()
		if materialIds is not None:
			for thing in materialIds:
				if thing is not None:
					materialIdsList.Add(thing)
		return self.Entity.AddMaterials(materialIdsList)

	def GetMaterials(self) -> list[DesignVariableMaterial]:
		return list[DesignVariableMaterial](self.Entity.GetMaterials())

	def RemoveAllMaterials(self) -> None:
		return self.Entity.RemoveAllMaterials()


class ToolingConstraintCol(IdNameEntityCol[ToolingConstraint]):
	def __init__(self, toolingConstraintCol: _api.ToolingConstraintCol):
		self.Entity = toolingConstraintCol
		self.CollectedClass = ToolingConstraint
		self.ToolingConstraintColList = tuple([ToolingConstraint(toolingConstraintCol) for toolingConstraintCol in self.Entity])

	@overload
	def Get(self, name: str) -> ToolingConstraint:
		pass

	@overload
	def Get(self, id: int) -> ToolingConstraint:
		pass

	def Get(self, item1 = None) -> ToolingConstraint:
		if isinstance(item1, str):
			return super().Get(item1)

		if isinstance(item1, int):
			return super().Get(item1)

	def __getitem__(self, index: int):
		return self.ToolingConstraintColList[index]

	def __iter__(self):
		yield from self.ToolingConstraintColList

	def __len__(self):
		return len(self.ToolingConstraintColList)


class DesignVariableCol(IdEntityCol[DesignVariable]):
	def __init__(self, designVariableCol: _api.DesignVariableCol):
		self.Entity = designVariableCol
		self.CollectedClass = DesignVariable
		self.DesignVariableColList = tuple([DesignVariable(designVariableCol) for designVariableCol in self.Entity])

	def __getitem__(self, index: int):
		return self.DesignVariableColList[index]

	def __iter__(self):
		yield from self.DesignVariableColList

	def __len__(self):
		return len(self.DesignVariableColList)


class ZoneDesignProperty(DesignProperty):
	def __init__(self, zoneDesignProperty: _api.ZoneDesignProperty):
		self.Entity = zoneDesignProperty

	@property
	def ToolingConstraints(self) -> ToolingConstraintCol:
		return ToolingConstraintCol(self.Entity.ToolingConstraints)

	@property
	def DesignVariables(self) -> DesignVariableCol:
		return DesignVariableCol(self.Entity.DesignVariables)


class Environment(ABC):
	def __init__(self, environment: _api.Environment):
		self.Entity = environment

	def SetLocation(self, location: str) -> None:
		return self.Entity.SetLocation(location)

	def Initialize(self) -> None:
		return self.Entity.Initialize()


class FailureCriterionSetting(FailureSetting):
	def __init__(self, failureCriterionSetting: _api.FailureCriterionSetting):
		self.Entity = failureCriterionSetting


class FailureModeSetting(FailureSetting):
	def __init__(self, failureModeSetting: _api.FailureModeSetting):
		self.Entity = failureModeSetting


class HelperFunctions(ABC):
	def __init__(self, helperFunctions: _api.HelperFunctions):
		self.Entity = helperFunctions

	def NullableSingle(self, input: float) -> float:
		return self.Entity.NullableSingle(input)


class TabularCorrectionFactorIndependentValue:
	def __init__(self, tabularCorrectionFactorIndependentValue: _api.TabularCorrectionFactorIndependentValue):
		self.Entity = tabularCorrectionFactorIndependentValue

	@property
	def BoolValue(self) -> bool:
		return self.Entity.BoolValue

	@property
	def DoubleValue(self) -> float:
		return self.Entity.DoubleValue

	@property
	def IntValue(self) -> int:
		return self.Entity.IntValue

	@property
	def ValueType(self) -> types.CorrectionValueType:
		return types.CorrectionValueType[self.Entity.CorrectionValueType.ToString()]


class OrthotropicEffectiveLaminate:
	def __init__(self, orthotropicEffectiveLaminate: _api.OrthotropicEffectiveLaminate):
		self.Entity = orthotropicEffectiveLaminate

	@property
	def Percent_tape_0(self) -> float:
		return self.Entity.Percent_tape_0

	@property
	def Percent_tape_90(self) -> float:
		return self.Entity.Percent_tape_90

	@property
	def Percent_tape_45(self) -> float:
		return self.Entity.Percent_tape_45

	@property
	def Percent_fabric_0(self) -> float:
		return self.Entity.Percent_fabric_0

	@property
	def Percent_fabric_90(self) -> float:
		return self.Entity.Percent_fabric_90

	@property
	def Percent_fabric_45(self) -> float:
		return self.Entity.Percent_fabric_45

	@property
	def Tape_Orthotropic(self) -> str:
		return self.Entity.Tape_Orthotropic

	@property
	def Fabric_Orthotropic(self) -> str:
		return self.Entity.Fabric_Orthotropic

	@property
	def Valid(self) -> bool:
		return self.Entity.Valid

	@property
	def Use_tape_allowables(self) -> bool:
		return self.Entity.Use_tape_allowables


class Beam(Zone):
	def __init__(self, beam: _api.Beam):
		self.Entity = beam

	@property
	def Length(self) -> float:
		return self.Entity.Length


class Panel(Zone):
	def __init__(self, panel: _api.Panel):
		self.Entity = panel

	@property
	def Area(self) -> float:
		return self.Entity.Area
