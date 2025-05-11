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

from openfhe import BINARY
import json

def screen(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED, b''
    logger.info("Screening Dataset")

    c = dispatcher.data.data
    js = json.loads('[]')
    for row in c:
        row_json = json.loads('[]')
        for cipher in row:
            plaintext = fhe.cc.Decrypt(ciphertext=cipher, privateKey=fhe.secretKey)
            plaintext_str = plaintext.GetCKKSPackedValue()
            value = float(plaintext_str[0].real)
            row_json.append(value)
        js.append(row_json)
    return ERRORS.OK, json.dumps(js)