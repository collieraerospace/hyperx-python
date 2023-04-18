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
from System.Collections.Generic import List

from abc import abstractmethod


class IdEntity:
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


class ZoneBase(ZoneJointEntity):
    @property
    def Centroid(self):
        return self.Entity.Centroid
    
    @property
    def Id(self):
        return self.Entity.Id
    
    @property
    def Weight(self):
        return self.Entity.Weight
    
    def RenumberZone(self, newId: int):
        return self.Entity.RenumberZone(newId)
    
    def GetAllResults(self):
        return self.Entity.GetAllResults()
    
    def GetControllingResult(self):
        return self.Entity.GetControllingResult()
    
    def GetMinimumMargin(self):
        return self.Entity.GetMinimumMargin()


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
    def MarginOfSafety(self):
        return self.Entity.MarginOfSafety
    
    @property
    def Centroid(self):
        return Centroid(self.Entity.Centroid)


class ElementCol:
    def __init__(self, elementCol: _api.ElementCol):
        self.ElementCol = elementCol
        self.ElementList = [Element(element) for element in self.ElementCol]

    def __iter__(self):
        yield from self.ElementList
    
    def __getitem__(self, index: int):
        return self.ElementList[index]
    
    def __len__(self):
        return len(self.ElementList)


class Zone(ZoneBase):
    @property
    def Elements(self):
        return ElementCol(self.Entity.Elements)
    
    def __init__(self, Zone: _api.Zone):
        self.Entity = Zone

    def AddElements(self, elementIds: list[int]):
        elementIdList = List[int]()
        for elementId in elementIds:
            elementIdList.Add(elementId)
        
        self.Zone.AddElements(elementIdList)


class ZoneCol:
    def __init__(self, zoneCol: _api.ZoneCol):
        self.ZoneCol = zoneCol
        self.ZoneList = [Zone(zone) for zone in self.ZoneCol]

    def __iter__(self):
        yield from self.ZoneList
    
    def __getitem__(self, index: int):
        return self.ZoneList[index]
    
    def __len__(self):
        return len(self.ZoneList)
    
    @property
    def Ids(self):
        return [id for id in self.ZoneCol.Ids]
    
    @property
    def Names(self):
        return [name for name in self.ZoneCol.Names]
    
    def Contains(self, id: int):
        return self.ZoneCol.Contains(id)
    
    def Get(self, id: int) -> Zone:
        return Zone(self.ZoneCol.Get(id))
    
    def Get(self, name: str) -> Zone:
        return Zone(self.ZoneCol.Get(name))


class Structure(IdNameEntityRenameable):
    @property
    def Zones(self): # TODO: fix this
        return ZoneCol(self.Entity.ZoneCol)
    
    def __init__(self, structure: _api.Structure):
        self.Entity = structure

    def AddElements(self, elementIds: list[int]):
        elementIdList = List[int]()
        for elementId in elementIds:
            elementIdList.Add(elementId)
        
        self.Structure.AddElements(elementIdList)
    
    def AddZone(self, zone: Zone):
        return self.Structure.AddZone(zone.Zone)

    def CreateZone(self, elementIds: list[int], name: str = None):
        elementIdList = List[int]()
        for elementId in elementIds:
            elementIdList.Add(elementId)
        
        if name is not None:
            self.Structure.CreateZone(elementIdList)
        else:
            self.Structure.CreateZone(elementIdList, name)


class StructureCol:
    def __init__(self, structureCol: _api.StructureCol):
        self.StructureCol = structureCol
        self.StructureList = [Structure(structure) for structure in self.StructureCol]
    
    def Get(self, id: int) -> Structure:
        return Structure(self.StructureCol.Get(id))
    
    def Get(self, name: str) -> Structure:
        return Structure(self.StructureCol.Get(name))
    
    @property
    def Ids(self):
        return [id for id in self.StructureCol.Ids]
    
    @property
    def Names(self):
        return [name for name in self.StructureCol.Names]
    
    def DeleteStructure(self, id: int):
        return self.StructureCol.DeleteStructure(id)
    
    def DeleteStructure(self, name: str):
        return self.StructureCol.DeleteStructure(name)
    
    def Contains(self, id: int):
        return self.StructureCol.Contains(id)
    
    def __iter__(self):
        yield from self.StructureList
    
    def __getitem__(self, index: int):
        return self.StructureList[index]
    
    def __len__(self):
        return len(self.StructureList)


class LoadProperty(AssignableProperty):
    def __init__(self, loadProperty: _api.LoadProperty):
        self.LoadProperty = loadProperty

    @property
    def Name(self):
        return self.LoadProperty.Name
    
    @property
    def Id(self):
        return self.LoadProperty.Id


class LoadPropertyCol:
    def __init__(self, loadPropertyCol: _api.LoadPropertyCol):
        self.Entity = loadPropertyCol
        self.LoadPropertyList = [LoadProperty(loadProperty) for loadProperty in self.Entity]

    def __iter__(self):
        yield from self.LoadPropertyList
    
    def __getitem__(self, index: int):
        return self.LoadPropertyList[index]
    
    def __len__(self):
        return len(self.LoadPropertyList)
    
    def Get(self, id: int) -> LoadProperty:
        return LoadProperty(self.Entity.Get(id))
    
    def Get(self, name: str) -> LoadProperty:
        return LoadProperty(self.Entity.Get(name))
    
    @property
    def Ids(self):
        return [id for id in self.Entity.Ids]
    
    @property
    def Names(self):
        return [name for name in self.Entity.Names]


class AnalysisProperty(AssignableProperty):
    def __init__(self, analysisProperty: _api.AnalysisProperty):
        self.AnalysisProperty = analysisProperty

    @property
    def Name(self):
        return self.AnalysisProperty.Name
    
    @property
    def Id(self):
        return self.AnalysisProperty.Id


class DesignProperty(AssignableProperty):
    def __init__(self, designProperty: _api.DesignProperty):
        self.DesignProperty = designProperty

    @property
    def Name(self):
        return self.DesignProperty.Name
    
    @property
    def Id(self):
        return self.DesignProperty.Id


class Project:
    @property
    def Zones(self):
        return ZoneCol(self.Project.Zones)
    
    @property
    def Structures(self):
        return StructureCol(self.Project.Structures)
    
    @property
    def Id(self):
        return self.Project.Id
    
    @property
    def Name(self):
        return self.Project.Name
    
    @property
    def LoadProperties(self):
        return LoadPropertyCol(self.Project.LoadProperties)
    
    def __init__(self, project: _api.Project):
        self.Project = project