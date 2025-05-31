from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization



import sys

sys.path.append('../logger')
from logger import logger

sys.path.append('../utils')
from utils import path_utils

sys.path.append('../exception')
from exception.key_exception import KeyException

class RSA:

    __privateKey: rsa.RSAPrivateKey = None
    __publicKey: rsa.RSAPublicKey = None

    __publicKeyRaw: str = ""

    def __init__(self):
        self.__loadKeys()

    def __loadKeys(self):
        logger.info("Reading Private Client PEM...")
        pk_str = path_utils.readResourceFile('private_client.pem')
        self.__privateKey = serialization.load_pem_private_key(pk_str.encode(), password=None)
        if not isinstance(self.__privateKey, rsa.RSAPrivateKey):
            raise KeyException("It seems like RSA Private Key is not valid")
        
        logger.info("Reading Public Client PEM...")
        self.__publicKeyRaw = path_utils.readResourceFile('public_client.pem')
        self.__publicKey = serialization.load_pem_public_key(self.__publicKeyRaw.encode())
        if not isinstance(self.__publicKey, rsa.RSAPublicKey):
            raise KeyException("It seems like RSA Public Key is not valid")
        

    
    @property
    def publicKey(self) -> rsa.RSAPublicKey:
        return self.__publicKey
    
    @property
    def privateKey(self) -> rsa.RSAPrivateKey:
        return self.__privateKey
    
    @property
    def publicKeyRaw(self) -> str:
        return self.__publicKeyRaw