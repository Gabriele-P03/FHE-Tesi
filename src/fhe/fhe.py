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
        first_mod_size = int(self.__config['first_mod_size'])
        scale_mod_size = int(self.__config['scale_mod_size'])
        batch_size = int(self.__config['batch_size'])
        mul_depth = int(self.__config['mul_depth'])

        logger.info(f'Generating Parameters (FMS: {first_mod_size}, SMS: {scale_mod_size}, BS: {batch_size}, MD: {mul_depth})...')

        self.__parameters = CCParamsCKKSRNS()
        #self.__parameters.SetFirstModSize(first_mod_size)
        self.__parameters.SetMultiplicativeDepth(mul_depth)
        self.__parameters.SetScalingModSize(scale_mod_size)
        self.__parameters.SetBatchSize(batch_size)

    def __cryptoContext(self):
        logger.info("Generating Crypto Context...")
        self.__context = GenCryptoContext(self.__parameters)
        logger.info("Enabling PKE, KEYSWITCH, LEVELEDSHE and ADVANCEDSHE")
        self.__context.Enable(PKESchemeFeature.PKE)
        self.__context.Enable(PKESchemeFeature.KEYSWITCH)
        self.__context.Enable(PKESchemeFeature.LEVELEDSHE)
        #self.__context.Enable(PKESchemeFeature.ADVANCEDSHE)

    def __keygen(self):
        flagGenKey = self.__config['custom_keys']
        flagServer = INSTANCE.port.assigned
        sk_file_path = 'private_client.pem'
        pk_file_path = 'public_client.pem'
        if flagServer:
            sk_file_path = 'private_server.pem'
            pk_file_path = 'public_server.pem'
        if flagGenKey:
            logger.info(f'Reading Secret Key from {sk_file_path}')
            sk_str = readResourceFile(sk_file_path, mode='rb')
            self.__secret_key = DeserializePrivateKeyString(sk_str, BINARY)
            logger.info(f'Reading Public Key from {pk_file_path}')
            pk_str = readResourceFile(pk_file_path, mode='rb')
            self.__public_key = DeserializePublicKeyString(pk_str, BINARY)
            self.__context
        else:
            logger.info("Generating Keys...")
            keys = self.__context.KeyGen()
            self.__public_key = keys.publicKey
            self.__secret_key = keys.secretKey
            if self.__config['save_keys']:
                logger.info(f'Storing Public Key in {pk_file_path}')
                saveFile(pk_file_path, Serialize(self.__public_key, BINARY), mode='wb')
                logger.info(f'Storing Secret Key in {sk_file_path}')
                saveFile(sk_file_path, Serialize(self.__secret_key, BINARY), mode='wb')
        logger.info("Evaluating MultKeyGen...")
        self.cc.EvalMultKeyGen(self.__secret_key)        

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




