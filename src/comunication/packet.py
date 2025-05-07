'''
A packet is a set of istruction which two end-point sent each other.

A packet sent by server to client always contain only either data field or a message in case
of error. 
'''

from comunication import errors, operations
import json
from types import SimpleNamespace

class Packet:

    __status: int
    __msg : str
    __op : int
    __data = None

    __valid = True

    def __new__(self, data = '', op = operations.OPERATIONS.PING):
        self.__status = errors.ERRORS.OK
        self.__msg = errors.getMessageErrorByIndex(self.__status)
        self.__data = data
        self.__op = operations.getOperationByIndex(op)

    def __init__(self, _json):
        self = json.load(_json, object_hook=lambda d: SimpleNamespace(**d))

    def __ensure(self):
        if self.__op == -1:
            self.__status = errors.ERRORS.INVALID_OPERATION
        
        if self.__status is not errors.ERRORS.OK:
            self.__valid = False
            self.__msg = errors.getMessageErrorByIndex(self.__status)

    def json(self):
        return json.dump(self, indent=1, sort_keys=True)
    
    def send(self, socket):
        socket.send(self.json())
        


