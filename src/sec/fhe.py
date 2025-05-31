from openfhe import *
import json
from logger import logger

import sys
sys.path.append('../utils')
from utils.path_utils import getResourceFile, readResourceFile, saveFile
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../exception')
from exception import call_exception

from cryptography.hazmat.primitives.asymmetric import rsa

from Crypto.Cipher import AES

class FHE:

    __config = None

    __parameters: CCParamsCKKSRNS
    __context: CryptoContext

    __secret_key: PrivateKey
    __public_key: PublicKey

    __pk: rsa.RSAPublicKey

    level_budget=[4,4]
    bsgs_dim=[0,0]

    def __init__(self):
        with getResourceFile(INSTANCE.port.assigned) as config_file:
            self.__config = json.load(config_file)
        if not INSTANCE.port.assigned:
            raise call_exception.CallException("FHE can be instanced only by server")
        logger.info("FHE Initializing...")    
        self.__loadParameters()  
        self.__cryptoContext()
        self.__keygen()  

        logger.info("FHE Initialized")


    def __loadParameters(self):
        self.__parameters = CCParamsCKKSRNS()

        secret_key_dist = SecretKeyDist.UNIFORM_TERNARY
        self.__parameters.SetSecretKeyDist(secret_key_dist)

        self.__parameters.SetRingDim(1<<12)
        self.__parameters.SetSecurityLevel(SecurityLevel.HEStd_NotSet)

        if get_native_int()==128:
            rescale_tech = ScalingTechnique.FIXEDAUTO
            dcrt_bits = 78
            first_mod = 89
        else:
            rescale_tech = ScalingTechnique.FLEXIBLEAUTO
            dcrt_bits = 59
            first_mod = 60

        self.__parameters.SetScalingTechnique(rescale_tech)
        self.__parameters.SetFirstModSize(first_mod)
        self.__parameters.SetScalingModSize(dcrt_bits)

        level_avaiability_after_bootstrap = 10
        depth = level_avaiability_after_bootstrap + FHECKKSRNS.GetBootstrapDepth(self.level_budget, secret_key_dist)
        self.__parameters.SetMultiplicativeDepth(depth)

    def __cryptoContext(self):
        logger.info("Generating Crypto Context...")
        self.__context = GenCryptoContext(self.__parameters)
        logger.info("Enabling PKE, KEYSWITCH, LEVELEDSHE and ADVANCEDSHE")
        self.__context.Enable(PKESchemeFeature.PKE)
        self.__context.Enable(PKESchemeFeature.KEYSWITCH)
        self.__context.Enable(PKESchemeFeature.LEVELEDSHE)
        self.__context.Enable(PKESchemeFeature.FHE)
        self.__context.Enable(PKESchemeFeature.ADVANCEDSHE)


    def __keygen(self):
        flagGenKey = self.__config['custom_keys']
        sk_file_path = 'private_server.pem'
        pk_file_path = 'public_server.pem'
        self.cc.EvalBootstrapSetup(self.level_budget)
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
        
        ring_dim = self.cc.GetRingDimension()
        num_slots = int(ring_dim/2)

        self.cc.EvalMultKeyGen(self.__secret_key)     
        self.cc.EvalBootstrapKeyGen(self.__secret_key, num_slots)   

    @property
    def publicKey(self) -> PublicKey:
        return self.__public_key
    
    def setPK(self, _pk: rsa.RSAPublicKey):
        self.__pk = _pk

    @property
    def pk(self) -> rsa.RSAPublicKey:
        return self.__pk
    
    @property
    def secretKey(self) -> PrivateKey:
        return self.__secret_key
    
    @property
    def cc(self) -> CryptoContext:
        return self.__context




