'''
Copyright Matthias Sedlmaier 2022
This file is part of pygccx.

pygccx is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

pygccx is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pygccx.  
If not, see <http://www.gnu.org/licenses/>.
'''

from typing import Protocol, runtime_checkable
import numpy as np
import numpy.typing as npt
from . import enums

number = int|float|np.number

class ISurface(Protocol):
    """Protocol for surface classes"""
    name:str
    """Gets the name of this surface """
    type: enums.ESurfTypes
    """Gets the type of this surface"""

    def write_ccx(self, buffer:list[str]): 
        """Writes the ccx input string of this surface to the given buffer"""
class IElement(Protocol):
    """Protocol for Element classes"""
    id:int
    """Gets the id of this element"""
    type:enums.EEtypes
    """Gets the GMSH type of this element"""
    node_ids:tuple[int, ...]
    """Gets the node ids of this element"""

    def get_dim(self) -> int:
        """Gets the dimension of this element"""
        ...
    def get_corner_node_count(self) -> int:
        """Gets the number of corner nodes for this element"""
        ...
    def get_corner_node_ids(self) -> tuple[int, ...]:
        """Gets the corner node ids for this element"""
        ...
    def get_faces(self) -> tuple[tuple[int, ...]]:
        """Gets the faces for this element. 
        Each face is a tuple with nodes ids forming this face.
        The order of the faces as well as the node ids of each face
        corresponds to the order in the element. I.e. faces[0] is
        the face this no. 1 ..."""
        ...

@runtime_checkable
class ISet(Protocol):
    """Protocol for node- or element set classes"""
    name:str
    """Gets the name of this set"""
    type:enums.ESetTypes
    """Gets the type of this set"""
    ids:set[int]
    """Gets the ids of this set"""

@runtime_checkable
class IKeyword(Protocol):
    """Protocol for Keyword classes"""
    name:str
    """Gets the name of this keyword"""
    desc:str
    """Gets the description of this keyword. This will also be written to the ccx input file"""

@runtime_checkable
class IStep(Protocol):
    """Protocol for Step classes"""
    desc:str
    step_keywords:list[IKeyword]

    def add_step_keywords(self, *step_keywords:IKeyword): ...

class ICoordinateSystem(Protocol):
    """Protocol for coordinate systems"""
    name:str
    """Name of this coordinate system. Used if an Orientation or Transform is
        instantiated using this coordinate system."""
    type:enums.EOrientationSystems
    """Type of this coordinate system"""

    def get_origin(self) -> npt.NDArray:
        """Gets the origin of this coordinate system as 1D numpy array"""
        ...

    def get_matrix(self) -> npt.NDArray:
        """Gets the orientation matrix of this coordinate system as 2D numpy array.
        row 0: vector of x axis in global system
        row 1: vector of y axis in global system
        row 2: vector of z axis in global system
        """
        ...

