import sys

sys.path.append('../../../logger')
from logger import logger

sys.path.append('../../../fhe')
from fhe.fhe import FHE

sys.path.append('..')
from ..dispatcher import Dispatcher

sys.path.append('../../')
from comunication.operations import Operation, OPERATIONS 
from comunication.errors import ERRORS

sys.path.append('../../../utils')
from utils import path_utils

def load(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.c is not None:
        return ERRORS.DATASET_ALREADY_LOADED
    try:
        #dataset = path_utils.getDataset(op.getParameterValue('uri'))
        #plain = fhe.encoder.encode(list(bytes(dataset, encoding='utf8')), 1 << 30)
        plain = fhe.encoder.encode([0.5, 0.3 + 0.2j, 0.78, 0.88j], 1 << 30)
        c = fhe.encryptor.encrypt(plain)
        dispatcher.c = c
        return ERRORS.OK
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND