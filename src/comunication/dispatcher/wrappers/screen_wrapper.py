'''

A Screen represents a screenshot of the current state of a cyphertext

'''

import sys

sys.path.append('../../../fhe')
from sec.fhe import FHE

sys.path.append('../../../logger')
from logger import logger

sys.path.append('..')
from ..dispatcher import Dispatcher

sys.path.append('../../')
from comunication.operations import Operation 
from comunication.errors import ERRORS

from openfhe import BINARY
import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def screen(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED, b''
    data = json.dumps(dispatcher.data.toJson(fhe))
    logger.info(f'Screening Dataset: {len(data)}') 
    return ERRORS.OK, data