from dataclasses import dataclass
from typing import Iterable, Optional
from protocols import IStepFeature, ISet
from enums import EResultOutputs, EElementResults

@dataclass(frozen=True, slots=True)
class ElFile:

    entities:Iterable[EElementResults]
    frequency:int = 1
    global_:bool = True
    output: EResultOutputs = EResultOutputs.DEFAULT
    output_all:bool = False
    section_forces:bool = False
    time_points:Optional[IStepFeature] = None
    nset:Optional[ISet] = None
    last_Iterations:bool = False
    contact_elements:bool = False
    name:str = ''
    desc:str = ''


    def __str__(self):
        s = '*EL FILE'
        if self.frequency != 1: s += f',FREQUENCY={self.frequency}'
        if not self.global_: s += ',GLOBAL=NO'
        if self.output != EResultOutputs.DEFAULT: s += f',OUTPUT={self.output.value}'
        if self.output_all: s += f',OUTPUT ALL'
        if self.section_forces: s += f',SECTION FORCES'
        if self.time_points: s += f',TIME POINTS={self.time_points.name}'
        if self.nset: s += f',NSET={self.nset.name}'
        if self.last_Iterations: s += f',LAST ITERATIONS'
        if self.contact_elements: s += f',CONTACT ELEMENTS'
        s += '\n'

        s += ','.join(e.value for e in self.entities) + '\n'

        return s