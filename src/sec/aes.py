from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization



import sys

sys.path.append('../logger')
from logger import logger

sys.path.append('../utils')
from utils import path_utils

sys.path.append('../exception')
from exception.key_exception import KeyException

from cryptography.hazmat.primitives import serialization

from Crypto.Cipher.AES import new, MODE_ECB

class AES:
    __aesKeyStr: str = ''
    __aes = None

    def __init__(self):
        self.__loadKeys()

    def __loadKeys(self):
        logger.info("Reading Client AES Key...")
        self.__aesKeyStr = path_utils.readResourceFile('aes_client.pem')
        self.__aes = new(bytes(self.__aesKeyStr, encoding='utf8'), MODE_ECB)

    @property
    def cipher(self):
        return self.__aes
    @property
    def aesKeyStr(self):
        return self.__aesKeyStr
        