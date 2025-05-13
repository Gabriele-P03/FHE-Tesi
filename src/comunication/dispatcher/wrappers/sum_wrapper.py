import sys

sys.path.append('../../../logger')
from logger import logger

sys.path.append('../../../fhe')
from fhe.fhe import FHE

sys.path.append('..')
from ..dispatcher import Dispatcher

sys.path.append('../../')
from comunication.operations import Operation, OPERATIONS 
from comunication.errors import ERRORS

from . import loader_wrapper

sys.path.append('../../../exception')
from exception.command_exception import CommandException
from exception.dataset_exception import DatasetException


def sum(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    try:
        uri = op.getParameterValue('uri')
        dataset = loader_wrapper.createDataset(uri, fhe=fhe)   #Loaded dataset to sum

        columns = [x.name for x in dispatcher.data.columns]

        try:
            cols = op.getParameterValue('columns').strip()
            cols = cols.split(';')
            #Checking if all typed columns exists in second dataset 
            for c in cols:
                dataset.hasColumn(c)

            ext_indeces = {}
            for j in range(len(dataset.columns)):
                c = dataset.columns[j].name
                flag = False
                for i in range(len(columns)):
                    c1 = columns[i]
                    if c == c1:
                        ext_indeces.update({j:i}) 
                        flag = True
                        break
                if not flag:
                    raise DatasetException(f'Column {c} is not present in the loaded dataset, therefore summing is not available')
        except CommandException:
            cols = columns
            #Checking if all loaded dataset's columns exist in second dataset 
            for c in columns:
                dataset.hasColumn(c)
            ext_indeces = {i:i for i in range(len(columns))}
        logger.info(f'Summing {uri} dataset by columns: {cols}. Indeces Linkage: {ext_indeces}')
        

        loaded_dataset = dispatcher.data.data
        loaded_row_size = dispatcher.data.size
        for j in ext_indeces:
            #j is the col in loaded dataset
            for i1 in range(0,loaded_row_size):
                c = loaded_dataset[i1][j]
                c1 = dataset.data[i1][ext_indeces[j]]
                c = fhe.cc.EvalAdd(c, c1)
                loaded_dataset[i1][j] = c
        
        return ERRORS.OK
    except DatasetException as e:
        return ERRORS.DATASET_COLUMN_NOT_PRESENT
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND