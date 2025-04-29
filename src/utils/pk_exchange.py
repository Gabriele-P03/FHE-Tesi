from util.public_key import PublicKey

import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../logger')
from logger import logger

from utils.socket_utils import recv

def exchange(__socket, pk: PublicKey) -> PublicKey:
    logger.info("Exchaning PK...")
    __send(__socket, pk)
    pk2 = __receive(__socket)
    logger.info("Exchangin Done!")
    return pk2

def __receive(__socket) -> PublicKey:
    p0, p0_size = recv(__socket)
    logger.info("PK0 received: " + str(p0_size) + " bytes")
    p1, p1_size = recv(__socket)
    logger.info("PK1 received: " + str(p1_size) + " bytes")
    return __composePK(p0, p1)

def __send(__socket, pk: PublicKey):
    p0 = str(pk.p0) + '\n'
    p1 = str(pk.p1) + '\n'
    __socket.sendall(bytes(p0, encoding='utf8'))
    logger.info("PK0 sent: " + str(len(p0)) + " bytes")
    __socket.sendall(bytes(p1, encoding='utf8'))
    logger.info("PK1 sent: " + str(len(p1)) + " bytes")

def __composePK(p0, p1) -> PublicKey:
    return PublicKey(p0,p1)

