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

from . import loader_wrapper


def sum(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.c is None:
        return ERRORS.NO_DATASET_LOADED
    try:
        uri = op.getParameterValue('uri')
        logger.info("Summing " + uri + " dataset")
        dataset = loader_wrapper.createDataset(uri, fhe=fhe)
        return ERRORS.OK
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND