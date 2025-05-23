import sys
from . import loader_wrapper, sum_wrapper, screen_wrapper

sys.path.append('../../')
from comunication.packet import Packet 
from comunication.operations import OPERATIONS 
from comunication.errors import ERRORS

from logger import logger

sys.path.append('../../../fhe')
from fhe.fhe import FHE

from typing import Union

def route(packet: Packet, dispatcher, fhe: FHE) -> Union[ERRORS, bytes]:
    err = -1
    index = packet.op
    data = b''
    match index:
        case OPERATIONS.LOAD.value:
            err = loader_wrapper.load(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.UNLOAD.value:
            err = loader_wrapper.unload(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.SUM.value:
            err = sum_wrapper.sum(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.SCREEN.value:
            err, data = screen_wrapper.screen(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.CLOSE.value:
            loader_wrapper.unload(packet.toOperation(), dispatcher, fhe)
            err = ERRORS.OK
            logger.info('Exiting...')
            exit(1)
    return err.value, data