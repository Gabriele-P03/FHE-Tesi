from enum import Enum
import json

class ERRORS(Enum):

    index: int

    OK = 0
    INVALID_OPERATION = 1
    DATASET_NOTFOUND = 2
    DATASET_ALREADY_LOADED = 3
    NO_DATASET_LOADED = 4


def getMessageErrorByIndex(er: int):
    match er:
        case ERRORS.OK.value:
            return 'No error'
        case ERRORS.INVALID_OPERATION.value:
            return 'Operation Not Valid'
        case ERRORS.DATASET_NOTFOUND.value:
            return 'Dataset Not Found or Not Available'
        case ERRORS.DATASET_ALREADY_LOADED.value:
            return 'There\'s already a dataset loaded. Close it before'
        case ERRORS.NO_DATASET_LOADED.value:
            return 'There\'s no dataset to unload'