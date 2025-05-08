from util.public_key import PublicKey

import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../logger')
from logger import logger

from utils.socket_utils import recv

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
    p = pickle.dumps(pk)
    logger.info("Sending " + str(len(p)) + " bytes of PK. Last item: " + str(p[-1]))
    p += b'\n'
    __socket.sendall(p)

def __composePK(p) -> PublicKey:
    return pickle.loads(p)

