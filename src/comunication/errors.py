from enum import Enum
import json

class ERRORS(Enum):

    index: int

    OK = 0
    INVALID_OPERATION = 1
    DATASET_NOTFOUND = 2
    DATASET_ALREADY_LOADED = 3
    NO_DATASET_LOADED = 4
    DATASET_CORRUPTED = 5
    DATASET_COLUMN_NOT_PRESENT = 6
    PARAMETER_ERROR = 7
    PARAMETER_VALUE_ERROR = 8



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
        case ERRORS.DATASET_CORRUPTED.value:
            return 'There\'s an invalid value in the selected dataset'
        case ERRORS.DATASET_COLUMN_NOT_PRESENT.value:
            return 'There are some columns which are not present in the laoded dataset'
        case ERRORS.PARAMETER_ERROR.value:
            return 'Parameter flow is not valid'
        case ERRORS.PARAMETER_VALUE_ERROR.value:
            return 'Parameter\'s value is not valid'