'''

A Screen represents a screenshot of the current state of a cyphertext

'''

import sys

sys.path.append('../../../fhe')
from fhe.fhe import FHE

sys.path.append('../../../logger')
from logger import logger

sys.path.append('..')
from ..dispatcher import Dispatcher

sys.path.append('../../')
from comunication.operations import Operation 
from comunication.errors import ERRORS

from openfhe import Serialize, BINARY

def screen(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.c is None:
        return ERRORS.NO_DATASET_LOADED, b''
    logger.info("Screening Dataset")

    c = dispatcher.c
    plaintext = fhe.cc.Decrypt(ciphertext=c, privateKey=fhe.secretKey)
    plaintext_str = plaintext.GetCKKSPackedValue()
    plaintext_str = "".join([chr(round(c.real)) for c in plaintext_str])
    return ERRORS.OK, plaintext_str