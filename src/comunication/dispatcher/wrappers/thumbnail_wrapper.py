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

import json

sys.path.append('../../../utils')
from utils import dataset_utils, path_utils

sys.path.append('../../../exception')
from exception.command_exception import CommandException
from exception.dataset_exception import DatasetException



def thumbnail(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:

    try:
        uri = op.getParameterValue('uri')
        stream = path_utils.getDataset(uri)
        columns = stream.readline().split(';')
        row_size = sum(1 for _ in stream)
    except CommandException:
        logger.info("Uri not given, thumbnail will be performed on the loaded dataset")
        if dispatcher.data is None:
            return ERRORS.NO_DATASET_LOADED, b''
        columns = [x.name for x in dispatcher.data.columns]
        row_size = dispatcher.data.size
    
    data = {}
    data["Columns"] = columns
    data["Columns Size"] = len(columns)
    data["Row Size"] = row_size
    data = json.dumps(data)
    logger.info(f'Screening Dataset: {len(data)}') 
    return ERRORS.OK, data