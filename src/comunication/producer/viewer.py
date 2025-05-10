import sys

sys.path.append('../')
from comunication.packet import Packet
from comunication.operations import OPERATIONS

sys.path.append('../../logger')
from logger import logger

from openfhe import DeserializeCiphertextString, BINARY

def view(req: Packet, res: Packet):
    if req.op == OPERATIONS.SCREEN.value:
        logger.info("Printing Current Cyphertext")
        print("---------------------------------------------------------------------------")
        print(res.data)
        print("---------------------------------------------------------------------------")