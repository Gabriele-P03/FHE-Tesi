from enum import Enum

class ERRORS(Enum):

    OK = 0,
    INVALID_OPERATION = 1
    DATASET_NOTFOUND = 2
    DATASET_ALREADY_LOADED = 3
    NO_DATASET_LOADED = 4

def getMessageErrorByIndex(er: ERRORS):
    match er:
        case ERRORS.OK:
            return 'No error'
        case ERRORS.INVALID_OPERATION:
            return 'Operation Not Valid'
        case ERRORS.DATASET_NOTFOUND:
            return 'Dataset Not Found or Not Available'
        case ERRORS.DATASET_ALREADY_LOADED:
            return 'There\'s already a dataset loaded. Close it before'
        case ERRORS.NO_DATASET_LOADED:
            return 'There\'s no dataset to unload'