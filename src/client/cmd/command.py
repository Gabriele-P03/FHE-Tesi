import sys

sys.path.append('../../exception')
from exception.command_exception import CommandException

sys.path.append('../../comunication')
from comunication import operations

import datetime


class Command:

    __datetime: datetime.datetime = None

    __raw: str

    __op: operations.OPERATIONS

    def __new__(cls, raw_cmd: str):
        if len(raw_cmd) < 1:
            raise CommandException("Empty Command typed")
        cls.__raw = raw_cmd

    def __init__(self):
        self.__datetime = datetime.datetime.now() 
        self.__op = operations.getOperationByName(self.__raw.split(" ")[0])
