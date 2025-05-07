'''

Producer is the module which manage request made up by client and sent to server.

Producer will receive the whole command as string typed by client via CLI

'''

import sys

sys.path.append('..')
from comunication.packet import Packet 
from comunication import operations

sys.path.append('../../logger')
from logger import logger

class Producer:

    def __new__(cls):
        instance = super().__new__(cls)
        logger.info("Producer Initialized")
        return instance

    def execute(cmd: str):
        splitted_cmd = cmd.split(" ", 2)
        cmd_name = splitted_cmd[0]    #Command Name
        op = operations.getOperationByName(cmd_name).__copy__()
        if len(splitted_cmd) > 1:
            op.operation.storeParameters(splitted_cmd[1]) #Store parameters
