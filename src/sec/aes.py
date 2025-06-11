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
from cryptography.hazmat.primitives.ciphers.algorithms import AES

class AES:
    __aesKeyStr: str = ''

    def __init__(self):
        self.__loadKeys()

    def __loadKeys(self):
        logger.info("Reading Client AES Key...")
        self.__aesKeyStr = path_utils.readResourceFile('aes_client.pem')

    @property
    def aesKeyStr(self):
        return self.__aesKeyStr
        