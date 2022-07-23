from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Material:
    """
    Class to indicate the start of a material definition

    Args:
        name: Name of this material up to 80 characters
        desc: Optional. A short description of this Material. This is written to the ccx input file.
    """
    name:str
    desc:str = ''

    def __post_init__(self):

        if len(self.name) > 80:
            raise ValueError(f'name can only contain up to 80 characters, got {len(self.name)}')

    def __str__(self):
        return f'*MATERIAL,NAME={self.name}\n'