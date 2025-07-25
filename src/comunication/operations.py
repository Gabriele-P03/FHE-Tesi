'''
In this enum file will be declared all operations type available

'''

import re 
import sys
import json

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
    __valorized: bool

    __cast_function = None


    def __new__(cls, *argv, **kwds):
        inst = object.__new__(cls)
        return inst
    
    def __init__(self, _key:str, _required: bool = False, _cast_function = str):
        self.__key = _key
        self.__required = _required
        self.__cast_function = _cast_function
        self.__valorized = False

    def valorize(self, value: str):
        self.__value = self.__cast_function(value)
        self.__valorized = True

    def resetToModel(self):
        self.__value = None
        self.__valorized = False

    @property
    def value(self):
        return self.__value    
    
    @property
    def valorized(self) -> bool:
        return self.__valorized
    
    @property
    def required(self) -> bool:
        return self.__required
    
    @property
    def key(self) -> str:
        return self.__key
    
    def data(self) -> str:
        buffer = '\"' + self.key + "\": "
        if isinstance(self.__value, str):
            buffer += '\"'+self.value+'\"'
        else:
            buffer += self.value
        return buffer
    
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

    def resetToModel(self):
        self.__model=True
        for par in self.__parameters:
            par.resetToModel()

    def setParameterValue(self, key:str, value):
        for par in self.__parameters:
            if par.key == key:
                par.valorize(value=value)
                return
        raise command_exception.CommandException("Parameter " + key + " is not available")

    def getParameterValue(self, key: str):
        for par in self.__parameters:
            if par.key == key:
                if par.valorized:
                    return par.value
                raise command_exception.CommandException("Parameter " + key + " was not passed")
        raise command_exception.CommandException("Parameter " + key + " is not available")

    @property
    def name(self):
        return self.__name    
    
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
    
    def storeParameters(self, raw_pars: list[str]): 
        if self.__model:
            raise command_exception.CommandException(self.__name + " is actually a model command")
        
        if len(raw_pars) > 1:

            if len(raw_pars) != 2:
                raise command_exception(raw_pars + " is not a valid command")

            splitted_parameters = re.sub(' +', ' ', raw_pars[1].strip()).split(' ')  #Remove multiple spaces and split the result string
            for par in splitted_parameters:
                spli_par = par.split('=')
                #Check if parameter's key exists
                flagFound = False
                for cr in self.__parameters:
                    if cr.key == spli_par[0]:
                        cr.valorize(spli_par[1])
                        flagFound = True
                        break
                if not flagFound:
                    raise command_exception.CommandException("Parameter " + spli_par[0] + " is not owned by " + self.__name)
        self.__checkRequiredUnvalorizedParams()

    def __checkRequiredUnvalorizedParams(self):
        for par in self.__parameters:
            if par.required and not par.valorized:
                raise command_exception.CommandException("Parameter " + par.key + " is required")

    def data(self) -> str:
        buffer = "["
        flag = False
        for i in range(0, len(self.__parameters)):
            par = self.__parameters[i]
            if par.valorized:
                if flag:
                    flag = False
                    buffer += ','
                buffer += '{' + par.data() + '}'
                flag = True
        buffer += "]"
        return buffer

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

    LOAD = 1, Operation('load', [
        Parameter[str]('uri', True, str),
        Parameter[str]('rows', False, str)
    ])
    
    UNLOAD = 2, Operation('unload', [])

    SUM = 3, Operation('sum', [
        Parameter[str]('uri', True, str),
        Parameter[str]('columns', False, str),
        Parameter[str]('rows', False, str)
    ])

    MUL = 4, Operation('mul', [
        Parameter[str]('uri', True, str),
        Parameter[str]('columns', False, str)
    ])

    SUB = 5, Operation('sub', [
        Parameter[str]('uri', True, str),
        Parameter[str]('columns', False, str)
    ])

    DIV = 6, Operation('div', [
        Parameter[str]('uri', True, str),
        Parameter[str]('columns', False, str)
    ])

    AVG = 7, Operation('avg', [
        Parameter[str]('columns', False, str)
    ])

    STD = 8, Operation('std', [
        Parameter[str]('columns', False, str)
    ])

    BST = 9, Operation('bootstrap', [
    ])

    DEL = 10, Operation('del', [
        Parameter[str]('rows', False, str),
        Parameter[str]('columns', False, str)
    ])

    DIR = 11, Operation('dir', [
    ])

    THN = 12, Operation('thn', [
        Parameter[str]('uri', False, str)
    ]) 
    

    SCREEN = 995, Operation(
                'screen', 
                []
            )
    RESPONSE = 996, Operation(
                    'response',
                    []
            )
    PING = 997, Operation(
                    'ping',
                    []
            )
    CLOSE = 999, Operation(
                    'close',
                    []
            )

def getOperationByIndex(i: int) -> OPERATIONS:
    for cr in list(OPERATIONS):
        if cr.value == i:
            return cr
    raise command_exception.CommandException("Command with index " + str(i) + " does not exists")

def getOperationByName(name: str) -> OPERATIONS:
    for cr in list(OPERATIONS):
        if cr.operation.name == name:
            return cr
    raise command_exception.CommandException("Command " + name + " does not exists")