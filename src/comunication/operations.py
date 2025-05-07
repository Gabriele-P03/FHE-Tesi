'''
In this enum file will be declared all operations type available

'''

import re 
import sys

sys.path.append('../exception')
from exception import command_exception

from enum import Enum
from typing import TypeVar, Generic
from typing import List

T = TypeVar('T', int, float, str, bool)

class Parameter(Generic[T]):
    __key: str
    __required: bool

    __value: T

    __cast_function = None

    def __new__(cls, *argv, **kwds):
        inst = object.__new__(cls)
        return inst
    
    def __init__(self, _key:str, _required: bool = False, _cast_function = str):
        self.__key = _key
        self.__required = _required
        self.__cast_function = _cast_function


    def valorize(self, value: str):
        self.__value = self.__cast_function(value)

    @property
    def value(self):
        return self.__value    
    
import copy    

class Operation:

    __name: str
    __parameters: List[Parameter] = []

    __model: bool = True    #Specify if it is a model parameter or already valorized

    def __new__(cls, *argv, **kwds):
        inst = object.__new__(cls)
        return inst
    
    def __init__(self, _name: str, _parameters: List[Parameter] = []):
        self.__name = _name
        self.__parameters = _parameters
    
    def __copy__(self):
        if not self.__model:
            raise command_exception.CommandException(self.__name + " is not a model command")

        copied = Operation(self.__name, self.__parameters)
        copied.__model = False
        return copied
    
    def __deepcopy__(self, memo):
        if not self.__model:
            raise command_exception.CommandException(self.__name + " is not a model command")
        
        copied = Operation(copy.deepcopy(self.__name, self.__parameters, memo))
        copied.__model = False
        return copied
    
    def storeParameters(self, raw_pars: str): 
        if self.__model:
            raise command_exception.CommandException(self.__name + " is actually a model command")
        
        splitted_parameters = re.sub(' +', ' ', raw_pars.strip).split(' ')  #Remove multiple spaces and split the result string
        for par in splitted_parameters:
            spli_par = par.split('=')
            #Check if parameter's key exists
            for cr in self.__parameters:
                if cr.__key == spli_par:
                    cr.valorize(spli_par[1])
                    break
            raise command_exception.CommandException("Parameter " + spli_par[0] + " is not owned by " + self.__name)

class OPERATIONS(Enum):

    __index: int
    __operation: Operation

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__)+1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj  

    def __init__(self, index: int, operation: Operation):
        self.__index = index  
        self.__operation = operation

    @property
    def operation(self) -> Operation:
        return self.__operation

    LOAD = 1, Operation(
                    'load', 
                    {
                        Parameter[str]('uri', True, str)
                    }
            )
    
    PING = 2, Operation(
                    'ping',
                    {}
            ) 

def getOperationByName(name: str) -> OPERATIONS:
    for cr in list(OPERATIONS):
        if cr.__operation.__name == name:
            return cr