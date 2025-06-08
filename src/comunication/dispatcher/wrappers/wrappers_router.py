import sys
from . import loader_wrapper, sum_wrapper, screen_wrapper, mul_wrapper, sub_wrapper, bootstrap_wrapper, avg_wrapper, div_wrapper, std_wrapper

sys.path.append('../../')
from comunication.packet import Packet 
from comunication.operations import OPERATIONS 
from comunication.errors import ERRORS

from logger import logger

sys.path.append('../../../fhe')
from sec.fhe import FHE

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
        case OPERATIONS.MUL.value:
            err = mul_wrapper.mul(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.SUB.value:
            err = sub_wrapper.sub(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.DIV.value:
            err = div_wrapper.div(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.AVG.value:
            err, data = avg_wrapper.avg(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.STD.value:
            err, data = std_wrapper.std(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.BST.value:
            err = bootstrap_wrapper.bootstrap(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.SCREEN.value:
            err, data = screen_wrapper.screen(packet.toOperation(), dispatcher, fhe)
        case OPERATIONS.CLOSE.value:
            loader_wrapper.unload(packet.toOperation(), dispatcher, fhe)
            err = ERRORS.OK
            logger.info('Exiting...')
            exit(1)
    return err.value, data