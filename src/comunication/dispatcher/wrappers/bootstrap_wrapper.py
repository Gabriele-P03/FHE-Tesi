import sys

sys.path.append('../../../logger')
from logger import logger

sys.path.append('../../../fhe')
from sec.fhe import FHE

sys.path.append('..')
from ..dispatcher import Dispatcher

sys.path.append('../../')
from comunication.operations import Operation, OPERATIONS 
from comunication.errors import ERRORS

sys.path.append('../../../utils')
from utils import dataset_utils

from . import loader_wrapper

sys.path.append('../../../exception')
from exception.command_exception import CommandException
from exception.dataset_exception import DatasetException


def bootstrap(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    logger.info("Executing bootstrap")
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    
    dataset = dispatcher.data
    cols_size = len(dataset.columns)
    cc = fhe.cc
    sk = fhe.secretKey
    for i in range(dataset.size):
        row = dataset.data[i]
        for j in range(cols_size):
            ciphertext = row[j]
            #Evaluate the single precision
            row[j] = cc.EvalBootstrap(ciphertext, 2, 17)
    return ERRORS.OK