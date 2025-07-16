import sys

sys.path.append('../../../logger')
from logger import logger

sys.path.append('../../../fhe')
from sec.fhe import FHE

sys.path.append('..')
from ..dispatcher import Dispatcher

sys.path.append('../../')
from comunication.operations import Operation 
from comunication.errors import ERRORS

sys.path.append('../../../utils')
from utils import path_utils

import json


def dir(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    logger.info("Executing Dataset Listing")
    listfiles = path_utils.listDataset()
    #Convert listfiles to json array
    return ERRORS.OK, json.dumps(listfiles)