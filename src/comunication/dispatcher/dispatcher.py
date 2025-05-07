'''

Dispatcher is the module which take care to elaborate request/operation received by client

'''
import sys

sys.path.append('../')
from comunication.packet import Packet, operations 
from ckks.ckks_encryptor import Ciphertext

sys.path.append('../../logger')
from logger import logger

class Dispatcher:

    c: Ciphertext = None 

    def __new__(cls):
        logger.info("Dispatcher Initialized")

    def dispatch(self, json: str) -> Packet:
        packet: Packet = self.__parsePacket(json=json)

    def __parsePacket(self, json: str) -> Packet:
        return Packet(json)

    def __execute(self, op: operations.OPERATIONS):
        return ''