from dataclasses import dataclass
from enums import EEtypes
from protocols import IElementFace

FACE_INDEX_TABLE = {
    EEtypes.C3D4:  ((0,1,2),   (0,3,1),   (1,3,2),   (2,3,0)),
    EEtypes.C3D8I: ((0,1,2,3), (4,7,6,5), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)),
    EEtypes.C3D6:  ((0,1,2),   (3,4,5),   (0,1,4,3), (1,2,5,4), (2,0,3,5)),
    EEtypes.C3D10: ((0,1,2),   (0,3,1),   (1,3,2),   (2,3,0)),
    EEtypes.C3D20R:((0,1,2,3), (4,7,6,5), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)), 
    EEtypes.C3D15: ((0,1,2),   (3,4,5),   (0,1,4,3), (1,2,5,4), (2,0,3,5)),
}

NODE_COUNT_TABLE = {
    EEtypes.SPRING1: 1,
    EEtypes.DCOUP3D: 1,
    EEtypes.MASS:    1,

    EEtypes.GAPUNI:  2,
    EEtypes.DASHPOTA: 2,
    EEtypes.SPRING2: 2,
    EEtypes.SPRINGA: 2,

    EEtypes.C3D4:   4,
    EEtypes.C3D8:   8,
    EEtypes.C3D8R:  8,
    EEtypes.C3D8I:  8,
    EEtypes.C3D6:   6,
    EEtypes.C3D10:  10,
    EEtypes.C3D20:  20,
    EEtypes.C3D20R: 20,
    EEtypes.C3D15:  15,
}

CORNER_NODE_COUNT_TABLE = {
    EEtypes.SPRING1: 1,
    EEtypes.DCOUP3D: 1,
    EEtypes.MASS:    1,

    EEtypes.GAPUNI: 2,
    EEtypes.DASHPOTA: 2,
    EEtypes.SPRING2: 2,
    EEtypes.SPRINGA: 2,

    EEtypes.C3D4:   4,
    EEtypes.C3D8:   8,
    EEtypes.C3D8R:  8,
    EEtypes.C3D8I:  8,
    EEtypes.C3D6:   6,
    EEtypes.C3D10:  4,
    EEtypes.C3D20:  8,
    EEtypes.C3D20R: 8,
    EEtypes.C3D15:  6,
}

def get_element_dimension(type:EEtypes) -> int:
    """
    Gets the dimension vor the given element type.

    0 for point elements (i.e. SPRING1, MASS), 
    1 for line elements (i.e. SPRING2, B32)
    2 for face elements (I.e. S4, CAX8), 
    3 for solid elements (i.e. C3D4, C3D20)

    Args:
        type (enums.EEtypes): Element type for which the dimension should be returned

    Returns:
        int: dimension
    """

    if type in (EEtypes.SPRING1, EEtypes.DCOUP3D, EEtypes.MASS):
        return 0
    elif type in (EEtypes.GAPUNI,EEtypes.DASHPOTA,EEtypes.SPRING2, EEtypes.SPRINGA):
        return 1
    elif type in (EEtypes.C3D4, EEtypes.C3D8, EEtypes.C3D8R, EEtypes.C3D8I, EEtypes.C3D6, 
                   EEtypes.C3D10, EEtypes.C3D20, EEtypes.C3D20R, EEtypes.C3D15):
        return 3
    raise ValueError(f'unkown etype, got{type}')

@dataclass(frozen=True, slots=True)
class Element:
    id:int
    type:EEtypes
    node_ids:tuple[int, ...]

    def __post_init__(self):

        if self.id < 0:
            raise ValueError(f"id has to be greater than 0, got{self.id}")
        no_nodes = NODE_COUNT_TABLE[self.type]
        name = self.type.name
        if len(self.node_ids) != no_nodes:      
            raise ValueError(f"Element of type {name} must have {no_nodes} node ids, got {len(self.node_ids)}")

    def get_dim(self) -> int:
        """Gets the dimension of this Element"""
        return get_element_dimension(self.type)

    def get_corner_node_count(self) -> int:
        """Gets the number of corner nodes of this element"""
        if self.type in CORNER_NODE_COUNT_TABLE:
            return CORNER_NODE_COUNT_TABLE[self.type]
        return len(self.node_ids)

    def get_corner_node_ids(self) -> tuple[int, ...]:
        """Gets the ids of the corner nodes"""
        return self.node_ids[:self.get_corner_node_count()]

    def get_faces(self) -> tuple[IElementFace, ...]:
        face_node_ind = FACE_INDEX_TABLE.get(self.type, [])
        faces = []
        for num, inds in enumerate(face_node_ind, 1):
            nids = tuple(self.node_ids[i] for i in inds)
            faces.append(ElementFace(num, self.id, nids))

        return tuple(faces)
    
@dataclass(frozen=True, slots=True)
class ElementFace:
    number:int
    element_id:int
    node_ids:tuple[int, ...]

    @property
    def name(self) -> str:
        return f'{self.element_id},S{self.number}'


