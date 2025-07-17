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


def sub(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    try:
        uri = op.getParameterValue('uri')
        dataset = loader_wrapper.createDataset(uri, fhe=fhe)   #Loaded dataset to sum

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
        logger.info(f'Subtracting {uri} dataset by columns: {cols}. Indeces Linkage: {ext_indeces}')

        loaded_dataset = dispatcher.data.data
        loaded_row_size = dispatcher.data.size
        for j in ext_indeces:
            #j is the col in loaded dataset
            for i1 in range(0,loaded_row_size):
                c = loaded_dataset[i1][j]
                c1 = dataset.data[i1][ext_indeces[j]]
                c = fhe.cc.EvalSub(c, c1)
                loaded_dataset[i1][j] = c
        
        return ERRORS.OK
    except DatasetException as e:
        return ERRORS.DATASET_COLUMN_NOT_PRESENT
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND