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
from .library import _api

from .api import Db, types
from .utils import Open, OpenWithDefault, WriteCsv
from typing import TypeVar, Generic, overload
from enum import Enum
from System.Collections.Generic import List, IEnumerable

from abc import ABC, abstractmethod

T = TypeVar('T')

class PropertyAssignmentStatus(Enum):
    Success = 1,
    Failure = 2,
    FailureCollectionAssignment = 3,
    PropertyIsNull = 4,
    PropertyNotFoundInDb = 5,
    EmptyCollection = 6,


class CollectionModificationStatus(Enum):
    Success = 1
    DuplicateIdFailure = 2
    EntityMissingAddFailure = 3
    EntityMissingRemovalFailure = 4
    FemConnectionFailure = 5


class RundeckUpdateStatus(Enum):
    Success = 1
    InvalidId = 2
    IdDoesNotExist = 3
    RundeckAlreadyPrimary = 4
    InputPathInUse = 5
    ResultPathInUse = 6


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


class ZoneIdUpdateStatus(Enum):
    Success = 1
    DuplicateIdFailure = 2

class IdEntity(ABC):
    @property
    def Id(self):
        return self.Entity.Id
 

class IdNameEntity(IdEntity):
    @property
    def Name(self):
        return self.Entity.Name
 

class IdNameEntityRenameable(IdNameEntity): 
    def Rename(self, name: str) -> None:
        self.Entity.Rename(name)


class IdEntityCol(ABC, Generic[T]):
    @property
    def Ids(self):
        return tuple([id for id in self.Entity.Ids])
    
    def Contains(self, id: int) -> bool:
        return self.Entity.Contains(id)
    
    def Count(self) -> int:
        return self.Entity.Count()
    
    def Get(self, id: int) -> T:
        return self.CollectedClass(self.Entity.Get(id))
    
    def GetEnumerator(self) -> tuple[T]:
        enumerator = self.Entity.GetEnumerator()
        tup = ()
        for item in enumerator:
            tup += (item)

        return tup


class IdNameEntityCol(IdEntityCol, Generic[T]):
    @property
    def Names(self) -> tuple[str]:
        nameList = [name for name in self.Entity.Names]
        return tuple(nameList)
    
    def Get(self, name: str) -> T: # TODO: can this type hint to suggest type T? 
        return self.CollectedClass(self.Entity.Get(name))
    

class ZoneJointContainerCol(IdNameEntityCol, Generic[T]):
    @abstractmethod
    def Create(self, name: str) -> bool:
        return self.Entity.Create(name)


class AssignableProperty(IdNameEntity):
    pass


class EntityWithAssignableProperties(IdNameEntityRenameable):
    @property
    def AssignedAnalysisProperty(self):
        return None if self.Entity.AssignedAnalysisProperty is None else AnalysisProperty(self.Entity.AssignedAnalysisProperty)
    
    @property
    def AssignedLoadProperty(self):
        return None if self.Entity.AssignedLoadProperty is None else LoadProperty(self.Entity.AssignedLoadProperty)
    
    @property
    def AssignedDesignProperty(self):
        return None if self.Entity.AssignedDesignProperty is None else DesignProperty(self.Entity.AssignedDesignProperty)
    
    def AssignAnalysisProperty(self, id: int):
        return self.Entity.AssignAnalysisProperty(id)
    
    def AssignLoadProperty(self, id: int):
        return self.Entity.AssignLoadProperty(id)
    
    def AssignDesignProperty(self, id: int):
        return self.Entity.AssignDesignProperty(id)
    
    def AssignProperty(self, property: AssignableProperty):
        self.Entity.AssignProperty(property)


class EntityWithAssignablePropertiesCol(IdNameEntityCol, Generic[T]): # TODO: how to enforce that T inherits from EntityWithAssignableProperties?
    def AssignPropertyToAll(self, assignableProperty: AssignableProperty):
        return PropertyAssignmentStatus[self.Entity.AssignPropertyToAll(assignableProperty).ToString()]

  
class ZoneJointEntity(EntityWithAssignableProperties):
    @abstractmethod
    def GetMinimumMargin():
        pass

    @abstractmethod
    def GetControllingResult():
        pass

    @abstractmethod
    def GetAllResults():
        pass

class Margin:
    def __init__(self, margin: _api.Margin):
        self.Entity = margin

    @property
    def AdjustedMargin(self):
        return self.Entity.AdjustedMargin
    
    @property
    def IsFailureCode(self):
        return self.Entity.IsFailureCode
    
    @property
    def IsInformationalCode(self):
        return self.Entity.IsInformationalCode
    
    @property
    def MarginCode(self):
        return types.MarginCode[self.Entity.MarginCode.ToString()]

class AnalysisDefinition(IdNameEntity):
    def __init__(self, analysisDefinition: _api.AnalysisDefinition):
        self.Entity = analysisDefinition

    @property
    def Description(self):
        return self.Entity.Description


class AnalysisResult(ABC):
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
    
class AnalysisResultCol(Generic[T]):
    def __init__(self, analysisResultCol: _api.AnalysisResultCol):
        self.Entity = analysisResultCol
        self.AnalysisResultList = tuple([AnalysisResult(analysisResult) for analysisResult in self.Entity])

    def __iter__(self):
        yield from self.AnalysisResultList
    
    def __getitem__(self, index: int):
        return self.AnalysisResultList[index]
    
    def __len__(self):
        return len(self.AnalysisResultList)
    
    def Count(self) -> int:
        return self.Entity.Count()
    
    def GetEnumerator(self) -> tuple[T]:
        enumerator = self.Entity.GetEnumerator()
        tup = ()
        for item in enumerator:
            tup += (item)

        return tup

class ZoneBase(ZoneJointEntity):
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
    
    def GetAllResults(self) -> AnalysisResultCol[AnalysisResult]:
        return AnalysisResultCol(self.Entity.GetAllResults())
    
    def GetControllingResult(self) -> AnalysisResult:
        return AnalysisResult(self.Entity.GetControllingResult())
    
    def GetMinimumMargin(self) -> Margin:
        return Margin(self.Entity.GetMinimumMargin())


class Centroid:
    def __init__(self, centroid: _api.Centroid):
        self.Centroid = centroid

    @property
    def X(self):
        return self.Centroid.X
    
    @property
    def Y(self):
        return self.Centroid.Y
    
    @property
    def Z(self):
        return self.Centroid.Z


class Element(IdEntity):
    def __init__(self, element: _api.Element):
        self.Entity = element
    
    @property
    def MarginOfSafety(self) -> float:
        return self.Entity.MarginOfSafety
    
    @property
    def Centroid(self) -> Centroid:
        return Centroid(self.Entity.Centroid)


class ElementCol(IdEntityCol[Element]):
    def __init__(self, elementCol: _api.ElementCol):
        self.Entity = elementCol
        self.CollectedClass = Element
        self.ElementList = tuple([Element(element) for element in self.Entity])

    def __iter__(self):
        yield from self.ElementList
    
    def __getitem__(self, index: int):
        return self.ElementList[index]
    
    def __len__(self):
        return len(self.ElementList)


class Zone(ZoneBase):
    def __init__(self, Zone: _api.Zone):
        self.Entity = Zone

    @property
    def Elements(self) -> ElementCol:
        return ElementCol(self.Entity.Elements)
    
    def AddElements(self, elementIds: list[int]) -> None:
        elementIdList = List[int]()
        for elementId in elementIds:
            elementIdList.Add(elementId)
        
        self.Zone.AddElements(elementIdList)

class Panel(Zone):
    @property
    def Area(self) -> float:
        return self.Entity.Area

class ZoneCol(EntityWithAssignablePropertiesCol[Zone]):
    def __init__(self, zoneCol: _api.ZoneCol):
        self.Entity = zoneCol
        self.CollectedClass = Zone
        self.ZoneList = tuple([Zone(zone) for zone in self.Entity])

    def __iter__(self):
        yield from self.ZoneList
    
    def __getitem__(self, index: int):
        return self.ZoneList[index]
    
    def __len__(self):
        return len(self.ZoneList)


class Joint(ZoneJointEntity):
    def __init__(self, joint: _api.Joint):
        self.Entity = joint

    def GetAllResults(self) -> AnalysisResultCol[AnalysisResult]:
        return AnalysisResultCol(self.Entity.GetAllResults())
    
    def GetControllingResult(self):
        return AnalysisResult(self.Entity.GetControllingResult())
    
    def GetMinimumMargin(self):
        pass


class JointCol(EntityWithAssignablePropertiesCol[Joint]):
    def __init__(self, jointCol: _api.JointCol):
        self.Entity = jointCol
        self.CollectedClass = Joint
        self.JointList = tuple([Joint(joint) for joint in self.Entity])

    def __iter__(self):
        yield from self.JointList
    
    def __getitem__(self, index: int):
        return self.JointList[index]
    
    def __len__(self):
        return len(self.JointList)


class PanelSegment(ZoneBase):
    def __init__(self, panelSegment: _api.PanelSegment):
        self.Entity = panelSegment

    @property
    def DiscreteTechnique(self) -> types.DiscreteTechnique:
        return types.DiscreteTechnique(self.Entity.DiscreteTechnique)
    
    @property
    def ElementsByObjectOrSkin(self) -> dict[types.DiscreteDefinitionType, ElementCol]: # TODO: TEST!!!!!!
        elementsByObjectOrSkinDict = {}
        for kvp in self.Entity.ElementsByObjectOrSkin:
            elementsByObjectOrSkinDict[types.DiscreteDefinitionType[kvp.Key.ToString()]] = ElementCol(kvp.Value)

        return elementsByObjectOrSkinDict
    
    @property
    def LeftSkinZoneId(self) -> int:
        return self.Entity.LeftSkinZoneId
    
    @property
    def Objects(self) -> tuple(types.DiscreteDefinitionType): # TODO: TEST!!!!!!!!!!!
        objectList = [types.DiscreteDefinitionType(object) for object in self.Entity.Objects]
        return tuple(objectList)
    
    @property
    def RightSkinZoneId(self) -> int:
        return self.Entity.RightSkinZoneId
    
    @property
    def Skins(self) -> tuple(types.DiscreteDefinitionType):
        skinList = [types.DiscreteDefinitionType(skin) for skin in self.Entity.Skins]
        return tuple(skinList)
    
    def SetObjectElements(self, discreteDefinitionType: types.DiscreteDefinitionType, elementIds: list[int]) -> None: # TODO: TEST!!!!!!!!!
        return self.Entity.SetObjectElements(discreteDefinitionType.value, elementIds)

    def GetElements(self, discreteDefinitionType: types.DiscreteDefinitionType) -> ElementCol: # TODO: TEST!!!!!!!!!
        return ElementCol(self.Entity.GetElements(discreteDefinitionType.value))


class PanelSegmentCol(EntityWithAssignablePropertiesCol[PanelSegment]):
    def __init__(self, panelSegmentCol: _api.PanelSegmentCol):
        self.Entity = panelSegmentCol
        self.CollectedClass = PanelSegment
        self.PanelSegmentList = tuple([PanelSegment(panelSegment) for panelSegment in self.Entity])

    def __iter__(self):
        yield from self.PanelSegmentList
    
    def __getitem__(self, index: int):
        return self.PanelSegmentList[index]
    
    def __len__(self):
        return len(self.PanelSegmentList)


class ZoneJointContainer(IdNameEntityRenameable):
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

    def AddJoint(self, id: int) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.AddJoint(id))
    
    def AddJoint(self, joint: Joint) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.AddJoint(joint.Entity))
    
    def AddPanelSegment(self, id: int) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.AddPanelSegment(id))
    
    def AddPanelSegment(self, panelSegment: PanelSegment) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.AddPanelSegment(panelSegment.Entity))
    
    @overload
    def AddZone(self, id: int) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.AddZone(id))
    
    @overload
    def AddZone(self, zone: Zone) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.AddZone(zone.Entity))
    
    def AddZone(self, zone) -> CollectionModificationStatus:
        if isinstance(zone, int):
            return CollectionModificationStatus[self.Entity.AddZone(zone).ToString()]
        if Zone.__instancecheck__(zone):
            return CollectionModificationStatus[self.Entity.AddZone(zone.Entity).ToString()]

    def RemoveJoint(self, id: int) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.RemoveJoint(id))
    
    def RemoveJoint(self, joint: Joint) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.RemoveJoint(joint.Entity))
    
    def RemoveJoints(self, ids: list[int]) -> CollectionModificationStatus: #TODO: TEST!!!!!!!!!!!!!!!!!!!
        return CollectionModificationStatus(self.Entity.RemoveJoints(ids))
    
    def RemoveJoints(self, joints: JointCol) -> CollectionModificationStatus: #TODO: TEST!!!!!!!!!!!!!!!!!!!
        return CollectionModificationStatus(self.Entity.RemoveJoints(joints))
    
    def RemovePanelSegment(self, id: int) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.RemovePanelSegment(id))
    
    def RemovePanelSegment(self, panelSegment: PanelSegment) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.RemovePanelSegment(panelSegment.Entity))
    
    @overload
    def RemovePanelSegments(self, ids: list[int]) -> CollectionModificationStatus: #TODO: TEST!!!!!!!!!!!!!!!!!!!
        return CollectionModificationStatus(self.Entity.RemovePanelSegments(ids))
    
    @overload
    def RemovePanelSegments(self, panelSegments: PanelSegmentCol) -> CollectionModificationStatus: #TODO: TEST!!!!!!!!!!!!!!!!!!!
        return CollectionModificationStatus(self.Entity.RemovePanelSegments(panelSegments))
    
    def RemovePanelSegments(self, panelSegments) -> CollectionModificationStatus:
        if isinstance(panelSegments, list[int]):
            return CollectionModificationStatus(self.Entity.RemovePanelSegments(panelSegments))
        
        if isinstance(panelSegments, PanelSegmentCol):
            return CollectionModificationStatus(self.Entity.RemovePanelSegments(panelSegments))


    def RemoveZone(self, id: int) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.RemoveZone(id))
    
    def RemoveZone(self, zone: Zone) -> CollectionModificationStatus:
        return CollectionModificationStatus(self.Entity.RemoveZone(zone.Entity))
    
    @overload
    def RemoveZones(self, ids: list[int]) -> CollectionModificationStatus: #TODO: TEST!!!!!!!!!!!!!!!!!!!
        return CollectionModificationStatus(self.Entity.RemoveZones(ids))
    
    @overload
    def RemoveZones(self, zones: ZoneCol) -> CollectionModificationStatus: #TODO: TEST!!!!!!!!!!!!!!!!!!!
        return CollectionModificationStatus(self.Entity.RemoveZones(zones))
    
    def RemoveZones(self, zones) -> CollectionModificationStatus:
        if list[int].__instancecheck__(zones): 
            idList = List[int]()
            for id in zones:
                idList.Add(id)

            enumerable = IEnumerable(idList)
            result = self.Entity.RemoveZones(enumerable)
            return CollectionModificationStatus[result.ToString()]
        
        if ZoneCol.__instancecheck__(zones):
            return CollectionModificationStatus[self.Entity.RemoveZones(zones.Entity).ToString()]


class Set(ZoneJointContainer):
    def __init__(self, set: _api.Set):
        self.Entity = set


class SetCol(ZoneJointContainerCol[Set]):
    def __init__(self, setCol: _api.SetCol):
        self.Entity = setCol
        self.CollectedClass = Set
        self.SetList = tuple([Set(set) for set in self.Entity])

    def __iter__(self):
        yield from self.SetList
    
    def __getitem__(self, index: int):
        return self.SetList[index]
    
    def __len__(self):
        return len(self.SetList)
    
    def Create(self, name: str) -> bool:
        return self.Entity.Create(name)


class Structure(ZoneJointContainer):
    def __init__(self, structure: _api.Structure):
        self.Entity = structure
    
    @property
    def Zones(self) -> ZoneCol:
        return ZoneCol(self.Entity.Zones)

    def AddElements(self, elementIds: list[int]):
        elementIdList = List[int]()
        for elementId in elementIds:
            elementIdList.Add(elementId)
        
        self.Structure.AddElements(elementIdList)
    
    @overload
    def AddZone(self, id: int) -> CollectionModificationStatus:
        return self.Structure.AddZone(id)

    @overload
    def AddZone(self, zone: Zone) -> CollectionModificationStatus:
        return self.Structure.AddZone(zone.Entity)

    def AddZone(self, zone) -> CollectionModificationStatus:
        if isinstance(zone, int):
            return CollectionModificationStatus[self.Entity.AddZone(zone).ToString()]
        
        if Zone.__instancecheck__(zone):
            return CollectionModificationStatus[self.Entity.AddZone(zone.Entity).ToString()]

    def CreateZone(self, elementIds: list[int], name: str = None) -> None:
        elementIdList = List[int]()
        for elementId in elementIds:
            elementIdList.Add(elementId)
        
        if name is not None:
            self.Structure.CreateZone(elementIdList)
        else:
            self.Structure.CreateZone(elementIdList, name)


class StructureCol(ZoneJointContainerCol[Structure]):
    def __init__(self, structureCol: _api.StructureCol):
        self.Entity = structureCol
        self.CollectedClass = Structure
        self.StructureList = [Structure(structure) for structure in self.Entity]
    
    @overload
    def DeleteStructure(self, id: int) -> bool:
        return self.Entity.DeleteStructure(id)
    
    @overload
    def DeleteStructure(self, name: str) -> bool:
        return self.Entity.DeleteStructure(name)
    
    def DeleteStructure(self, structure) -> bool:
        if isinstance(structure, int):
            return self.Entity.DeleteStructure(structure)
        
        if Structure.__instancecheck__(structure):
            return self.Entity.DeleteStructure(structure.Entity)
    
    def Create(self, name: str) -> bool:
        return self.Entity.Create(name)
    
    def __iter__(self):
        yield from self.StructureList
    
    def __getitem__(self, index: int):
        return self.StructureList[index]
    
    def __len__(self):
        return len(self.StructureList)


class LoadProperty(AssignableProperty):
    def __init__(self, loadProperty: _api.LoadProperty):
        self.Entity = loadProperty


class LoadPropertyCol(IdNameEntityCol[LoadProperty]):
    def __init__(self, loadPropertyCol: _api.LoadPropertyCol):
        self.Entity = loadPropertyCol
        self.CollectedClass = LoadProperty
        self.LoadPropertyList = tuple([LoadProperty(loadProperty) for loadProperty in self.Entity])

    def __iter__(self):
        yield from self.LoadPropertyList
    
    def __getitem__(self, index: int):
        return self.LoadPropertyList[index]
    
    def __len__(self):
        return len(self.LoadPropertyList)


class AnalysisProperty(AssignableProperty):
    def __init__(self, analysisProperty: _api.AnalysisProperty):
        self.Entity = analysisProperty


class AnalysisPropertyCol(IdNameEntityCol[AnalysisProperty]):
    def __init__(self, analysisPropertyCol: _api.AnalysisPropertyCol):
        self.Entity = analysisPropertyCol
        self.CollectedClass = AnalysisProperty
        self.AnalysisPropertyList = tuple([AnalysisProperty(analysisProperty) for analysisProperty in self.Entity])

    def __iter__(self):
        yield from self.AnalysisPropertyList
    
    def __getitem__(self, index: int):
        return self.AnalysisPropertyList[index]
    
    def __len__(self):
        return len(self.AnalysisPropertyList)


class DesignProperty(AssignableProperty):
    def __init__(self, designProperty: _api.DesignProperty):
        self.Entity = designProperty


class DesignPropertyCol(IdNameEntityCol[DesignProperty]):
    def __init__(self, designPropertyCol: _api.DesignPropertyCol):
        self.Entity = designPropertyCol
        self.CollectedClass = DesignProperty
        self.DesignPropertyList = tuple([DesignProperty(designProperty) for designProperty in self.Entity])

    def __iter__(self):
        yield from self.DesignPropertyList
    
    def __getitem__(self, index: int):
        return self.DesignPropertyList[index]
    
    def __len__(self):
        return len(self.DesignPropertyList)


class FemProperty(IdNameEntity):
    def __init__(self, femProperty: _api.FemProperty):
        self.Entity = femProperty

    @property
    def Elements(self) -> ElementCol:
        return ElementCol(self.Entity.Elements)


class FemPropertyCol(IdEntityCol[FemProperty]):
    def __init__(self, femPropertyCol: _api.FemPropertyCol):
        self.Entity = femPropertyCol
        self.CollectedClass = FemProperty
        self.FemPropertyList = tuple([FemProperty(femProperty) for femProperty in self.Entity])

    def __iter__(self):
        yield from self.FemPropertyList
    
    def __getitem__(self, index: int):
        return self.FemPropertyList[index]
    
    def __len__(self):
        return len(self.FemPropertyList)


class ElementSet(IdNameEntity):
    def __init__(self, elementSet: _api.ElementSet):
        self.Entity = elementSet

    @property
    def Elements(self) -> ElementCol:
        return ElementCol(self.Entity.Elements)


class ElementSetCol(IdEntityCol[ElementSet]):
    def __init__(self, elementSetCol: _api.ElementSetCol):
        self.Entity = elementSetCol
        self.CollectedClass = ElementSet
        self.ElementSetList = tuple([ElementSet(elementSet) for elementSet in self.Entity])

    def __iter__(self):
        yield from self.ElementSetList
    
    def __getitem__(self, index: int):
        return self.ElementSetList[index]
    
    def __len__(self):
        return len(self.ElementSetList)

class FemDataSet:
    def __init__(self, femDataSet: _api.FemDataSet):
        self.Entity = femDataSet

    @property
    def FemProperties(self) -> FemPropertyCol:
        return FemPropertyCol(self.Entity.FemProperties)
    
    @property
    def ElementSets(self) -> ElementSetCol:
        return ElementSetCol(self.Entity.ElementSets)


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
    
    def SetInputFilePath(self, filePath: str) -> RundeckUpdateStatus:
        return RundeckUpdateStatus[self.Entity.SetInputFilePath(filePath).ToString()]
    
    def SetResultFilePath(self, filePath: str) -> RundeckUpdateStatus:
        return RundeckUpdateStatus[self.Entity.SetResultFilePath(filePath).ToString()]


class RundeckCol(IdEntityCol[Rundeck]):
    def __init__(self, rundeckCol: _api.RundeckCol):
        self.Entity = rundeckCol
        self.CollectedClass = Rundeck
        self.RundeckList = tuple([Rundeck(rundeck) for rundeck in self.Entity])

    def __iter__(self):
        yield from self.RundeckList
    
    def __getitem__(self, index: int):
        return self.RundeckList[index]
    
    def __len__(self):
        return len(self.RundeckList)
    
    def AddRundeck(self, inputPath: str, resultPath: str = None) -> RundeckCreationStatus:
        return RundeckCreationStatus[self.Entity.AddRundeck(inputPath, resultPath).ToString()] if resultPath is not None else RundeckCreationStatus[self.Entity.AddRundeck(inputPath).ToString()]
    
    def ReassignPrimary(self, id: int) -> RundeckUpdateStatus:
        return RundeckUpdateStatus[self.Entity.ReassignPrimary(id).ToString()]
    
    def RemoveRundeck(self, id: int) -> RundeckRemoveStatus:
        return RundeckRemoveStatus[self.Entity.RemoveRundeck(id).ToString()]


class Project:
    @property
    def WorkingFolder(self) -> str:
        return self.Project.WorkingFolder
    
    @property
    def FemDataSet(self) -> FemDataSet:
        return FemDataSet(self.Project.FemDataSet)
    
    @property
    def Beams(self) -> ZoneCol:
        return ZoneCol(self.Project.Beams)
    
    @property
    def Panels(self) -> ZoneCol:
        return ZoneCol(self.Project.Panels)

    @property
    def Id(self) -> int:
        return self.Project.Id
    
    @property
    def Name(self) -> str:
        return self.Project.Name

    @property
    def Zones(self) -> ZoneCol:
        return ZoneCol(self.Project.Zones)
    
    @property
    def Sets(self) -> SetCol:
        return SetCol(self.Project.Sets)

    @property
    def Structures(self) -> StructureCol:
        return StructureCol(self.Project.Structures)
    
    @property
    def Rundecks(self) -> RundeckCol:
        return RundeckCol(self.Project.Rundecks)
    
    @property
    def LoadProperties(self) -> LoadPropertyCol:
        return LoadPropertyCol(self.Project.LoadProperties)
    
    @property
    def AnalysisProperties(self) -> AnalysisPropertyCol:
        return AnalysisPropertyCol(self.Project.AnalysisProperties)
    
    @property
    def DesignProperties(self) -> DesignPropertyCol:
        return DesignPropertyCol(self.Project.DesignProperties)
    
    def __init__(self, project: _api.Project):
        self.Project = project