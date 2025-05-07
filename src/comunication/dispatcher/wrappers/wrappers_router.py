import sys
from . import loader_wrapper

sys.path.append('../../')
from comunication.packet import Packet 
from comunication.operations import OPERATIONS 

sys.path.append('../../../fhe')
from fhe.fhe import FHE


def route(packet: Packet, dispatcher, fhe: FHE):

    if packet.op == OPERATIONS.LOAD.value:
        loader_wrapper.load(packet.toOperation(), dispatcher, fhe)