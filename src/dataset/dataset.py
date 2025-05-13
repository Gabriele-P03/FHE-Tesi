"""

A dataset is a class which represents a dataset including its column name and type

"""

from dataset.datasets import DATASETTYPES
from dataset.column import Column
from dataset.dataset_loader_wrapper import load_csv

import json, pickle, sys

sys.path.append('../exception')
from exception.dataset_exception import DatasetException 

from openfhe import Ciphertext, Serialize, BINARY

sys.path.append('../fhe')
from fhe.fhe import FHE

class Dataset:

    __name: str
    __type: DATASETTYPES
    __columns: list[Column] = []

    __data = [[Ciphertext]]

    def __init__(self, _name:str = '', _type: DATASETTYPES = None, _columns: list[Column] = []):
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
    
    @property
    def data(self):
        return self.__data
    
    @property
    def columns(self):
        return self.__columns

    def load(self, stream, fhe: FHE):
        if self.__type == DATASETTYPES.CSV:
            self.__columns, self.__data = load_csv(stream, fhe)

    def hasColumn(self, name: str):
        for c in self.columns:
            if c.name == name:
                return
        raise RuntimeError(f'Dataset {self.name} does not contain any {name} column')

    """
        Return the whole dataset as a json array
        containing a json array for each row.
        The single value is the ciphertext.
        Each single ciphertext must be decrypted bu client
    """
    def toJson(self):
        js = []
        for row in self.__data:
            js_row = []
            for val in row:
                b = Serialize(val, BINARY)
                js_row.append(str(b))  #Appending ciphertext
            js.append(js_row)
        return js