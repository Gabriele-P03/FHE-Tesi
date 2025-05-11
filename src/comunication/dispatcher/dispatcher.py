'''

Dispatcher is the module which take care to elaborate request/operation received by client

'''
import sys

sys.path.append('../')
from comunication.packet import Packet, operations 

sys.path.append('../../logger')
from logger import logger

sys.path.append('../../../fhe')
from fhe.fhe import FHE

sys.path.append('../../dataset')
from dataset.dataset import Dataset



class Dispatcher:

    data: Dataset = None 

    def __init__(self):
        logger.info("Dispatcher Initialized")

    def dispatch(self, json: str, fhe: FHE) -> Packet:
        packet: Packet = self.__parsePacket(json=json)
        return self.__execute(packet, fhe)

    def __parsePacket(self, json: str) -> Packet:
        return Packet(json)

    def __execute(self, packet: Packet, fhe: FHE) -> Packet:
        from .wrappers import wrappers_router
        err, data = wrappers_router.route(packet, self, fhe)
        respPacket = Packet(_data=str(data), _status=err)
        return respPacket