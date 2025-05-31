import sys

sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../logger')
from logger import logger

sys.path.append('../exception')
from exception import key_exception

from utils.socket_utils import recv, send
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def exchange(__socket, pk):
    logger.info("Exchanging PK...")
    if INSTANCE.port.assigned:
        pk = __receive(__socket)
        return pk
    else:
        __send(__socket, pk)
        return None
    

def __receive(__socket) ->  rsa.RSAPublicKey:
    p, p_size = recv(__socket)
    logger.info(f'Received {p_size} bytes of Client\'s PK')
    pk = serialization.load_pem_public_key(p)
    if not isinstance(pk, rsa.RSAPublicKey):
        raise key_exception.KeyException("It seems like received Client's Public Key is not valid")
    return pk

def __send(__socket, pk):
    logger.info(f'Sending {len(pk)} + bytes of PK.')
    pk = bytes(pk, encoding='utf8')
    send(__socket, pk)

