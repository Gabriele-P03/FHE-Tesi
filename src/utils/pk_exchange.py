from openfhe import PublicKey, Serialize, BINARY, DeserializePublicKeyString

import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../logger')
from logger import logger

from utils.socket_utils import recv, send

import pickle

def exchange(__socket, pk: PublicKey) -> PublicKey:
    logger.info("Exchaning PK...")
    __send(__socket, pk)
    pk2 = __receive(__socket)
    logger.info("Exchangin Done!")
    return pk2

def __receive(__socket) -> PublicKey:
    p, p_size = recv(__socket)
    return __composePK(p)

def __send(__socket, pk: PublicKey):

    p = Serialize(pk, BINARY)
    logger.info("Sending " + str(len(p)) + " bytes of PK. Last item: " + str(p[-1]))
    send(__socket, p)

def __composePK(p: str) -> PublicKey:
    logger.info("Recomposing PK with " + str(len(p)) + " bytes")
    return DeserializePublicKeyString(p, BINARY)

