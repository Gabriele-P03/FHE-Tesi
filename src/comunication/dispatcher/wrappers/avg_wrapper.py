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

import json


def avg(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    logger.info("Executing average")
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    try:
        dataset = dispatcher.data.data
        row_size = dispatcher.data.size

        columns = [x.name for x in dispatcher.data.columns]
        try:
            cols = op.getParameterValue('columns').strip()
            cols = cols.split(';')
        except CommandException:
            cols = list( map(lambda x: x.name, dataset.columns) )

        try:
            ext_indeces = dataset_utils.match_indices_cols(columns, cols, dataset)
        except DatasetException as e:
            return ERRORS.DATASET_COLUMN_NOT_PRESENT, str(e)

        buffer = []

        for j in ext_indeces:
            #j is the col in loaded dataset
            ciphertext_buffer = None
            for i1 in range(0,row_size):
                c = dataset[i1][j]
                if i1 == 0:
                    ciphertext_buffer = c
                else:
                    ciphertext_buffer = fhe.cc.EvalAdd(ciphertext_buffer, c)

            sum = fhe.cc.Decrypt(fhe.secretKey, ciphertext_buffer).GetCKKSPackedValue()[0].real
            avg = sum/row_size
            buffer.append(avg)
        
        return ERRORS.OK, json.dumps([buffer])
    except DatasetException as e:
        return ERRORS.DATASET_COLUMN_NOT_PRESENT
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND