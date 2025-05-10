'''
A packet is a set of istruction which two end-point sent each other.

A packet sent by server to client always contain only either data field or a message in case
of error. 
'''

from comunication import errors, operations
import json
from types import SimpleNamespace

from comunication.packet_json_encoder import JsonEncoder

class Packet:

    __status: int
    __msg : str = ''
    __op : int
    __data = ''
    __valid = True

    def __new__(cls, *argv, **kwds):
        inst = object.__new__(cls)
        return inst

    def __init__(self, _json: str = '', _data: str = '', _op: int = operations.OPERATIONS.PING.value, _status: int = -1):
        if len(_json) > 0:
            dict = json.loads(_json)
            if 'op' in dict:
                self.__op = int(dict['op'])
            if 'msg' in dict:
                self.__msg = str(dict['msg'])
            if 'status' in dict:
                self.__status = int(dict['status'])
            if 'data' in dict:
                self.__data = str(dict['data'])
        else: 
            if _status == -1:
                self.__status = errors.ERRORS.OK._value_
                self.__msg = errors.getMessageErrorByIndex(self.__status)
                self.__data = _data
                self.__op = _op
            else:
                self.__status = _status
                self.__op = operations.OPERATIONS.RESPONSE.value
                self.__data=_data

        self.ens()    

    def ens(self):
        if self.__op == -1:
            self.__status = errors.ERRORS.INVALID_OPERATION._value_
        
        if self.__status is not errors.ERRORS.OK._value_:
            self.__valid = False
            self.__msg = errors.getMessageErrorByIndex(self.__status)
    
    @property
    def status(self):
        return self.__status
    
    @property
    def valid(self):
        return self.__valid
    
    @property
    def data(self):
        return self.__data
    
    @property
    def op(self):
        return self.__op
    
    @property
    def msg(self):
        return self.__msg

    def json(self):
        js = json.dumps(self, indent=1, cls=JsonEncoder)
        return js
    
    def toOperation(self) -> operations.Operation:
        o: operations.OPERATIONS = operations.getOperationByIndex(self.op)
        operation = o.operation.__copy__()
        parametersJsonArray = json.loads(self.data, object_hook=lambda d: SimpleNamespace(**d))
        for par in parametersJsonArray:
            d = par.__dict__
            for c in d:
                operation.setParameterValue(c, d[c])
        return operation

