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
from utils import path_utils

sys.path.append('../../../dataset')
from dataset.dataset import Dataset
from dataset import datasets

from exception import command_exception

def getNameAndFormatByPath(path: str):
    splitted_uri = path.split('.')
    return splitted_uri[0], datasets.fromFormat(splitted_uri[1])

def load(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is not None:
        return ERRORS.DATASET_ALREADY_LOADED, ''
    try:
        dispatcher.data = createDataset(op.getParameterValue('uri'), fhe)
        return ERRORS.OK, ''
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND, ''
    except ValueError as e:
        return ERRORS.DATASET_CORRUPTED, str(e)
    except command_exception.CommandException as e:
        return ERRORS.PARAMETER_VALUE_ERROR, str(e)
    
def createDataset(uri: str, fhe: FHE, reciprocal=False):
    logger.info("Loading " + uri + " dataset")
    stream = path_utils.getDataset(uri)
    name, format = getNameAndFormatByPath(uri)
    dataset = Dataset(name, format, []) 
    dataset.load(stream, fhe, reciprocal) 
    l = dataset.size
    if l == 0:
        logger.warn("It seems like " + uri + " is an empty dataset")
    else:
        logger.info(str(l) + " row(s) read")
    return dataset
    
def unload(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    logger.info("Unloading dataset")
    dispatcher.data = None
    return ERRORS.OK


def close(op: Operation, dispatcher: Dispatcher, fhe: FHE):
    unload(op, dispatcher, fhe)
    exit(1)