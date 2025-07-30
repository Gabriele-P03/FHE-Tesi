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


import psutil
from openpyxl import Workbook
import datetime
wb = Workbook()
ws = wb.active


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

        ps = pre = psutil.Process()
        dt = datetime.datetime.now()
        ws.append([str(dt)])
        row_index = 0

        for j in ext_indeces:
            pre = ps.memory_info().rss
            row_index += 1
            print(f'Sub {row_index}')
            #j is the col in loaded dataset
            for i1 in range(0,loaded_row_size):
                c = loaded_dataset[i1][j]
                c1 = dataset.data[i1][ext_indeces[j]]
                c = fhe.cc.EvalSub(c, c1)
                loaded_dataset[i1][j] = c
            
            ws.append([row_index, pre, ps.memory_info().rss])
        file_name = 'test_'+str(datetime.datetime.now())+'_'
        wb.save('/home/gabrielepace_std/FHE-Tesi/test/sub_'+file_name+'.xlsx')
        
        return ERRORS.OK
    except DatasetException as e:
        return ERRORS.DATASET_COLUMN_NOT_PRESENT
    except FileNotFoundError as e:
        return ERRORS.DATASET_NOTFOUND