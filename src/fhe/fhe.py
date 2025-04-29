from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_evaluator import CKKSEvaluator
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters

from util.public_key import PublicKey

import json
from logger import logger

import sys
sys.path.append('../utils')
from utils.path_utils import getResourceFile
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

class FHE:

    __config = None

    __parameters: CKKSParameters

    __keyGenerator = None

    __encoder: CKKSEncoder
    __encryptor: CKKSEncryptor
    __decryptor: CKKSDecryptor
    __evaluator: CKKSEvaluator 

    def __init__(self):
        with getResourceFile(INSTANCE.port.assigned) as config_file:
            self.__config = json.load(config_file)
        self.__loadParameters()    
        self.__keygen()  
        self.__initEncoder()
        self.__initEncryptor()
        self.__initDecryptor()
        self.__initEvaluator()

        logger.info("FHE Initialized")


    def __loadParameters(self) -> CKKSParameters:
        poly_degree = int(self.__config['poly_degree'])
        ciph_modulus = 1 << 600
        big_modulus = 1 << 1200
        scaling_factor = 1 << 30

        self.__parameters = CKKSParameters(
            poly_degree=poly_degree,
            ciph_modulus=ciph_modulus,
            big_modulus=big_modulus,
            scaling_factor=scaling_factor
        )


    def __keygen(self):
        self.__keyGenerator = CKKSKeyGenerator(params=self.__parameters)

    def __initEncoder(self):
        self.__encoder = CKKSEncoder(self.__parameters)   

    def __initEncryptor(self):
        self.__encryptor = CKKSEncryptor(self.__parameters, self.__keyGenerator.public_key, self.__keyGenerator.secret_key)

    def __initDecryptor(self):
        self.__decryptor = CKKSDecryptor(self.__parameters, self.__keyGenerator.secret_key)

    def __initEvaluator(self):
        self.__evaluator = CKKSEvaluator(self.__parameters) 

    @property
    def pk(self):
        
        return self.__keyGenerator.public_key 
    



