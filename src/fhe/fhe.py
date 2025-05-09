from openfhe import *
import json
from logger import logger

import sys
sys.path.append('../utils')
from utils.path_utils import getResourceFile, readResourceFile, saveFile
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

class FHE:

    __config = None

    __parameters: CCParamsCKKSRNS
    __context: CryptoContext

    __secret_key: PrivateKey
    __public_key: PublicKey

    __pk: PublicKey

    def __init__(self):
        with getResourceFile(INSTANCE.port.assigned) as config_file:
            self.__config = json.load(config_file)
        logger.info("FHE Initializing...")    
        self.__loadParameters()  
        self.__cryptoContext()
        self.__keygen()  

        logger.info("FHE Initialized")


    def __loadParameters(self):
        logger.info("Generating Parameters...")
        degree = int(self.__config['degree'])
        plain_modulus = int(self.__config['plain_modulus'])
        ciph_modulus = int(self.__config['ciph_modulus'])
        self.__parameters = CCParamsCKKSRNS()

    def __cryptoContext(self):
        logger.info("Generating Crypto Context...")
        self.__context = GenCryptoContext(self.__parameters)

    def __keygen(self):
        logger.info("Generating Keys...")
        flagGenKey = self.__config['custom_keys']
        if flagGenKey:
            logger.info("Rading Secret Key from private.pem")
            sk_str = readResourceFile('private.pem', mode='rb')
            self.__secret_key = DeserializePrivateKeyString(sk_str, BINARY)
            logger.info("Rading Public Key from public.pem")
            pk_str = readResourceFile('public.pem', mode='rb')
            self.__public_key = DeserializePublicKeyString(pk_str, BINARY)
            self.__context
        else:
            logger.info("Enabling PKE")
            self.__context.Enable(PKESchemeFeature.PKE)
            keys = self.__context.KeyGen()
            self.__public_key = keys.publicKey
            self.__secret_key = keys.secretKey
            if self.__config['save_keys']:
                logger.info("Storing Public Key in public.pem")
                saveFile('public.pem', Serialize(self.__public_key, BINARY), mode='wb')
                logger.info("Storing Secret Key in private.pem")
                saveFile('private.pem', Serialize(self.__secret_key, BINARY), mode='wb')
                

    @property
    def publicKey(self) -> PublicKey:
        return self.__public_key
    
    def setPK(self, _pk: PublicKey):
        self.__pk = _pk

    @property
    def pk(self) -> PublicKey:
        return self.__pk
    
    @property
    def secretKey(self) -> PrivateKey:
        return self.__secret_key
    
    @property
    def cc(self) -> CryptoContext:
        return self.__context




