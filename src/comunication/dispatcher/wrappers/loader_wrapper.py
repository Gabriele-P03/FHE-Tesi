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

from exception import command_exception

sys.path.append('../../../utils')
from utils import path_utils, dataset_utils

sys.path.append('../../../dataset')
from dataset.dataset import Dataset
from dataset import datasets


def getNameAndFormatByPath(path: str):
    splitted_uri = path.split('.')
    return splitted_uri[0], datasets.fromFormat(splitted_uri[1])

def load(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is not None:
        return ERRORS.DATASET_ALREADY_LOADED
    try:
        dispatcher.data = createDataset(op, fhe)
        return ERRORS.OK, ''
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND, ''
    except command_exception.CommandException as e:
        return ERRORS.PARAMETER_ERROR, str(e)
    
def createDataset(op: Operation, fhe: FHE, reciprocal=False):
    uri = op.getParameterValue('uri')
    logger.info("Loading " + uri + " dataset")

    rows = dataset_utils.parseRowIndices(op)

    stream = path_utils.getDataset(uri)
    name, format = getNameAndFormatByPath(uri)
    dataset = Dataset(name, format, []) 
    dataset.load(stream, fhe, reciprocal, rows=rows) 
    l = dataset.size
    if l == 0:
        logger.warn("It seems like " + uri + " is an empty dataset")
    else:
        logger.info(str(l) + " row(s) read")
    if len(rows) <= 0:
        rows = range(0, l)
    return dataset, rows
    
def unload(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    logger.info("Unloading dataset")
    dispatcher.data = None
    return ERRORS.OK


def close(op: Operation, dispatcher: Dispatcher, fhe: FHE):
    unload(op, dispatcher, fhe)
    exit(1)