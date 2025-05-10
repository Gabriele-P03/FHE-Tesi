'''

In this enum file will be declared all dataset type which this application
is able to parse

'''

from enum import Enum

class DATASETTYPES(Enum):

    __index: int
    __format: str

    def __init__(self, _index: int, _format: str):
        super().__init__()
        self.__index  = _index
        self.__format = _format

    @property
    def index(self):
        return self.__index
    @property
    def format(self):
        return self.__format

    CSV = 0, 'csv'

