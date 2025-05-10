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


def sum(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.c is None:
        return ERRORS.NO_DATASET_LOADED
    try:
        uri = op.getParameterValue('uri')
        logger.info("Summing " + uri + " dataset")
        dataset = path_utils.getDataset(uri)
        dec_list = [ ord(c) for c in dataset ]
        plain = fhe.cc.MakeCKKSPackedPlaintext(dec_list)

        c = fhe.cc.EvalAdd(dispatcher.c, plain)
        dispatcher.c = c
        return ERRORS.OK
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND