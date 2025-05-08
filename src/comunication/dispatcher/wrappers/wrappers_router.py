import sys
from . import loader_wrapper

sys.path.append('../../')
from comunication.packet import Packet 
from comunication.operations import OPERATIONS 
from comunication.errors import ERRORS

sys.path.append('../../../fhe')
from fhe.fhe import FHE


def route(packet: Packet, dispatcher, fhe: FHE) -> ERRORS:
    err = -1
    if packet.op == OPERATIONS.LOAD.value:
        err = loader_wrapper.load(packet.toOperation(), dispatcher, fhe)

    return err.value