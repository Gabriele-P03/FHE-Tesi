'''

A Column take care to store metadata about a dataset's column


'''

import sys

sys.path.append('../exception')
from exception.dataset_exception import DatasetException

class Column:

    __name: str  
    __required: bool

    def __init__(self, _name: str, _required: bool = False):
        super().__init__()
        if len(_name) < 1:
            raise DatasetException("Column's Name is empty")
        self.__name = _name
        self.__required = _required

    @property
    def name(self) -> str:
        return self.__name
    @property
    def required(self) -> bool:
        return self.__required

