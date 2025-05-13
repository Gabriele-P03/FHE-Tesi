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
    data = json.dumps(dispatcher.data.toJson())
    logger.info(f'Screening Dataset: {len(data)} bytes')
    json.loads(data) 
    logger.dbg('Load worked')
    return ERRORS.OK, data