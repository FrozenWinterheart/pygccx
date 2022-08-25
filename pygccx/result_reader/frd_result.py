from dataclasses import dataclass, field
from typing import Iterable
from enum import Enum

import numpy as np
import numpy.typing as npt

from enums import EResultLocations, EFrdEntities

IMAGINARIES:set[EFrdEntities] = {
    EFrdEntities.FORCI, 
    EFrdEntities.DISPI, 
    EFrdEntities.TOSTRAII, 
    EFrdEntities.ERRORI, 
    EFrdEntities.HERRORI, 
    EFrdEntities.MESTRAII,
    EFrdEntities.STRESSI,
    EFrdEntities.ZZSTRI,
    EFrdEntities.CONTACTI
}

@dataclass(frozen=True, slots=True)
class FrdResultSet:
    entity:EFrdEntities
    """Enum of the result set entity i.e. DISP, STRESS"""
    no_components:int
    """number of components per value. I.e. for a DISP result set no_components == 3"""
    step_time:float
    """Step time of this result set"""
    component_names:tuple[str,...]
    """Names of the value components. I.e. for a DISP result set ('D1', 'D2', 'D3')"""
    values:dict[int, npt.NDArray[np.float64]] = field(repr=False)
    """
    Dictionary with values.\n
    key = node id, value = vector with entity components\n   
    """
    entity_location:EResultLocations = field(init=False, default= EResultLocations.NODAL)
    """Location of the result entity. i.e. NODAL, ELEMENT, ..."""
    set_name:str = field(init=False, default='')
    """Name of the node- or element set."""

    def get_values_by_ids(self, ids:Iterable[int]) -> npt.NDArray[np.float64]:
        return np.array([self.values.get(id, np.zeros(self.no_components)) for id in ids])


@dataclass(frozen=True, slots=True)
class FrdResult:
    step_times:tuple[float]
    """Sorted tuple with all step times"""
    result_sets:tuple[FrdResultSet, ...]
    """Tuple with all result sets"""

    def get_result_sets_by_entity(self, entity:EFrdEntities) -> tuple[FrdResultSet, ...]:
        """
        Returns all result sets with the given entity
        If no such result set exists an empty tuple is returned.

        Args:
            entity (EFrdEntities): Entity of result sets to be returned

        Returns:
            tuple[IResultSet, ...]: Tuple of all result sets with the given entity
        """

        return tuple(rs for rs in self.result_sets if rs.entity==entity)   

    def get_result_set_by_entity_and_time(self, entity:EFrdEntities, step_time:float) -> FrdResultSet|None:
        """
        Returns the result set with the given entity and closest step time to the given step_time.
        If no such result set exists, None is returned.

        Args:
            entity (EFrdEntities): Entity of result set to be returned
            step_time (float): Step time of result set to be returned

        Returns:
            IResultSet|None: Matched result set or None
        """
        # filter by name
        result_sets = self.get_result_sets_by_entity(entity)

        # filter by step times    
        nearest_time = min(self.step_times, key=lambda x:abs(x - step_time)) 
        for rs in result_sets:
            if rs.step_time == nearest_time: return rs

    def get_result_set_by_entity_and_index(self, entity:EFrdEntities, step_index:int) -> FrdResultSet|None:
        """
        Returns the result set with the given entity and step index (index of step time in step_times).
        If no such result set exists, None is returned.

        Args:
            entity (EFrdEntities): Entity of result set to be returned
            step_index (int): Step index of result set to be returned

        Returns:
            IResultSet|None: Matched result set or None
        """
        # filter by name
        result_sets = self.get_result_sets_by_entity(entity)

        # filter by step indices
        step_time = self.step_times[step_index] 
        for rs in result_sets:
            if rs.step_time == step_time: return rs

    @classmethod
    def from_file(cls, filename:str) -> 'FrdResult':
        """
        Creates a FrdResult from the given filename and returns it.

        IMPORTANT:
        Only ASCII files created with *NODE FILE, *EL FILE and *CONTACT FILE 
        can be read!!!

        Args:
            filename (str): Path to ascii *.frd file

        Returns:
            FrdResult
        """

        # For the format definition of *.frd look at the CGX Manual
              
        # Parse the file
        #-----------------------------------------------------
        result_set_open = False     # Flag indicates that a result set is starting
        entity_name = ''
        no_comp = 0
        step_time = 0.
        step_times = set()
        values:dict[int, npt.NDArray[np.float64]] = {}
        result_stes:list[FrdResultSet] = []
        component_names:list[str] = []

        with open(filename) as f:
            for line in f:        
                line_split = line.split()    #split line at white spaces

                if line_split[0] == '-3':
                    result_set_open = False
                    if values:
                        result = FrdResultSet(EFrdEntities(entity_name) , no_comp, step_time, tuple(component_names[:no_comp]), values)
                        result_stes.append(result)
                        values = {}
                        component_names = []
                    continue
                elif line_split[0] == '-4':
                    result_set_open = True
                    entity_name = line_split[1]
                    continue
                elif line_split[0] == '100CL':
                    step_time = float(line_split[2])
                    step_times.add(step_time)
                    continue

                if not result_set_open: continue

                if line_split[0] == '-5':
                    component_names.append(line_split[1])
                    if line_split[3] == '1': no_comp = 1
                    elif line_split[3] == '2': no_comp = 3
                    else: no_comp = 6 # line_split[3] must be 4. to verify
                                  
                elif line_split[0] == '-1':                  
                    nid=int(line[3:13])                   
                    components = np.array([line[13+j*12 : 13+j*12+12] for j in range(no_comp)], dtype=float)
                    values[nid] = components 

        step_times = tuple(sorted(step_times))
        return cls(step_times, tuple(result_stes))