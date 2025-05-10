'''

A Column take care to store metadata about a dataset's column

In case you do not know column's type, you should always obtain for a str

'''

import sys

sys.path.append('../exception')
from exception.dataset_exception import DatasetException

from typing import Generic, TypeVar

T = TypeVar('T')

class Column(Generic[T]):

    __name: str
    __cls = type    
    __required: bool
    __algebraic: bool

    def __init__(self, _name: str, _required: bool = False):
        super().__init__()
        if len(_name) < 1:
            raise DatasetException("Column's Name is empty")
        self.__name = _name
        self.__required = _required
        self.__cls = type(T)
        self.__algebraic = T in [int, float]

    @property
    def name(self) -> str:
        return self.__name
    @property
    def required(self) -> bool:
        return self.__required
    @property
    def algebraic(self) -> bool:
        return self.__algebraic
    @property
    def cls(self) -> type:
        return self.__cls

