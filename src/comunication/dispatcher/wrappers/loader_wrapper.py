import sys

sys.path.append('../../../logger')
from logger import logger

sys.path.append('../../../fhe')
from fhe.fhe import FHE

sys.path.append('..')
from ..dispatcher import Dispatcher

sys.path.append('../../')
from comunication.operations import Operation 
from comunication.errors import ERRORS

sys.path.append('../../../utils')
from utils import path_utils

def load(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.c is not None:
        return ERRORS.DATASET_ALREADY_LOADED
    try:
        dataset = path_utils.getDataset(packet.data.split('=')[1])
        c = fhe.__encryptor.encrypt(dataset)
        dispatcher.c = c
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND