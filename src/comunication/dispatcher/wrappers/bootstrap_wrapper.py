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


import psutil
from openpyxl import Workbook
import datetime
wb = Workbook()
ws = wb.active

def bootstrap(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    logger.info("Executing bootstrap")
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    
    dataset = dispatcher.data
    cols_size = len(dataset.columns)
    cc = fhe.cc
    sk = fhe.secretKey
    row_index = 0
    for i in range(dataset.size):
        row = dataset.data[i]
        row_index += 1
        print(f'Bootstrapping {row_index}')
        for j in range(cols_size):
            ciphertext = row[j]
            #Evaluate the single precision
            row[j] = cc.EvalBootstrap(ciphertext)

    return ERRORS.OK