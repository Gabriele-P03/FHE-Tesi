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

    def execute(self, cmd: str, socket) -> Packet:
        splitted_cmd = cmd.split(" ", 2)
        cmd_name = splitted_cmd[0]    #Command Name
        op_enum = operations.getOperationByName(cmd_name)
        op = op_enum.operation.__copy__()
        op.storeParameters(splitted_cmd) #Store parameters
        packet = Packet(_data=op.data(), _op=op_enum.value)
        bs = bytes(packet.json(), encoding='utf8')+b'\0\0\0\0\0\0\0\0'
        socket.sendall(bs)
        return packet
        

