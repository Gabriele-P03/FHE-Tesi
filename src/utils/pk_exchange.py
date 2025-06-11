'''

In this file ad hoc will be performed ke- exchanging-steps between two end-points

Server sends its rsa public key (a) to client
Client sends its aes key (e) already encrypted via a
Server decrypts enc e with its rsa private key  

'''

import sys

sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../logger')
from logger import logger

sys.path.append('../exception')
from exception import key_exception

from utils.socket_utils import recv, send
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat



def exchange(__socket, key: bytes):
    logger.info("Exchanging PK...")
    if INSTANCE.port.assigned:#Server side

        logger.info(f'Sending RSA Public Key: {len(key)} bytes')
        send(__socket, key)
        logger.info("Waiting for Client's AES Key")
        client_aes_enc, server_pk_size = recv(__socket)
        return client_aes_enc
    else:
        logger.info("Waiting for Server's RSA Public Key")
        server_pk, server_pk_size = recv(__socket)
        server_pk = serialization.load_pem_public_key(server_pk)
        logger.info("Sending Encrypted AES Key")
        enc_aes = server_pk.encrypt(key, padding.OAEP(
                                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                algorithm=hashes.SHA256(),
                                                label=None)
    )
        send(__socket, enc_aes)
        return None

