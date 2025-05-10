"""

A dataset is a class which represents a dataset including its column name and type

"""

from datasets import DATASETTYPES
from column import Column
from dataset_loader_wrapper import load_csv

import sys

sys.path.append('../exception')
from exception.dataset_exception import DatasetException 

class Dataset:

    __name: str
    __type: DATASETTYPES
    __columns: list[Column] = []

    __data = [[]]

    def __init__(self, _name:str = '', _type: DATASETTYPES = None, _columns: list[Column] = []):
        object.__init__()
        if len(_name) < 1:
            raise DatasetException("Dataset's Name is empty")
        if _type is None:
            raise DatasetException("Dataset's Type is None")
        self.__name = _name
        self.__type = _type
        self.__columns = _columns

    @property
    def size(self):
        return len(self.__data)
    @property
    def name(self):
        return self.__name

    def load(self, stream):
        if self.__type == DATASETTYPES.CSV.value:
            self.__columns, self.__data = load_csv(stream)