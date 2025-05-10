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
        uri = op.getParameterValue('uri')
        logger.info("Loading " + uri + " dataset")
        dataset = path_utils.getDataset(uri)
        dec_list = [ ord(c) for c in dataset ]
        plain = fhe.cc.MakeCKKSPackedPlaintext(dec_list)

        c = fhe.cc.Encrypt(fhe.publicKey, plain)
        dispatcher.c = c
        return ERRORS.OK
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND
    
def unload(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.c is None:
        return ERRORS.NO_DATASET_LOADED
    logger.info("Unloading dataset")
    dispatcher.c = None
    return ERRORS.OK


def close(op: Operation, dispatcher: Dispatcher, fhe: FHE):
    unload(op, dispatcher, fhe)
    exit(1)