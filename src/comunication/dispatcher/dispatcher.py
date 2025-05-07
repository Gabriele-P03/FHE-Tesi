'''

Dispatcher is the module which take care to elaborate request/operation received by client

'''
import sys

sys.path.append('../')
from comunication.packet import Packet, operations 
from ckks.ckks_encryptor import Ciphertext

sys.path.append('../../logger')
from logger import logger

sys.path.append('../../../fhe')
from fhe.fhe import FHE



class Dispatcher:

    c: Ciphertext = None 

    def __init__(self):
        logger.info("Dispatcher Initialized")

    def dispatch(self, json: str, fhe: FHE) -> Packet:
        packet: Packet = self.__parsePacket(json=json)
        self.__execute(packet, fhe)

    def __parsePacket(self, json: str) -> Packet:
        return Packet(json)

    def __execute(self, packet: Packet, fhe: FHE) -> Packet:
        from .wrappers import wrappers_router
        wrappers_router.route(packet, self, fhe)
        return Packet('', '')