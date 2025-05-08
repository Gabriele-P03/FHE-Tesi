from bfv.batch_encoder import BatchEncoder
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_evaluator import BFVEvaluator
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters

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

    __parameters: BFVParameters

    __keyGenerator = None

    __encoder: BatchEncoder
    __encryptor: BFVEncryptor
    __decryptor: BFVDecryptor
    __evaluator: BFVEvaluator 

    def __init__(self):
        with getResourceFile(INSTANCE.port.assigned) as config_file:
            self.__config = json.load(config_file)
        self.__loadParameters()    
        self.__keygen()  
        self.__initEncoder()
        #self.__initEncryptor()
        self.__initDecryptor()
        self.__initEvaluator()

        logger.info("FHE Initialized")


    def __loadParameters(self) -> BFVParameters:
        degree = int(self.__config['degree'])
        plain_modulus = int(self.__config['plain_modulus'])
        ciph_modulus = int(self.__config['ciph_modulus'])

        self.__parameters = BFVParameters(
            poly_degree=degree,
            plain_modulus=plain_modulus,
            ciph_modulus=ciph_modulus
        )


    def __keygen(self):
        self.__keyGenerator = BFVKeyGenerator(params=self.__parameters)

    def __initEncoder(self):
        self.__encoder = BatchEncoder(self.__parameters)   

    def setPK(self, pk: PublicKey):
        logger.info("Setting Encryptor with PK of other end-point")
        self.__encryptor = BFVEncryptor(self.__parameters, pk)

    def __initDecryptor(self):
        self.__decryptor = BFVDecryptor(self.__parameters, self.__keyGenerator.secret_key)

    def __initEvaluator(self):
        self.__evaluator = BFVEvaluator(self.__parameters) 

    @property
    def pk(self):
        
        return self.__keyGenerator.public_key 
    
    @property
    def encryptor(self):
        return self.__encryptor
    
    @property
    def encoder(self):
        return self.__encoder



