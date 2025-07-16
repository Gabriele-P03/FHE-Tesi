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

import numpy as np


def delete(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    logger.info("Executing Deleting Rows/Columns")
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    try:

        flagColumn = False
        try:
            cols = op.getParameterValue('columns').strip()
            cols = cols.split(';')
            flagColumn = True
            logger.info("Columns Deleting selected")
        except CommandException:
            logger.info("Columns Deleting not selected")

        flagRow = False
        try:
            rows = op.getParameterValue('rows').strip()
            rows = rows.split(';')
            logger.info("Rows Deleting selected")
            flagRow = True
        except CommandException:
            logger.info("Rows Deleting not selected")

        if not flagColumn and not flagRow:
            return ERRORS.PARAMETER_ERROR, "At least one among columns or rows parameter must be passed when invoking del function"
        
        cols_size = len(dispatcher.data.columns)
        rows_size = dispatcher.data.size

        if flagRow:
            rows = []
            for i_str in rows:
                try:
                    i = int(i_str)
                    if i < 0:
                        return ERRORS.PARAMETER_VALUE_ERROR, "A row index must a positive integer"
                    if i >= rows_size:
                        return ERRORS.PARAMETER_VALUE_ERROR, f'A row index must less than row size ({rows_size})'

                    rows.append(i)
                except ValueError:
                    return ERRORS.PARAMETER_VALUE_ERROR, f'Row inedx {i_str} is not valid'
            dispatcher.data.data = np.delete(dispatcher.data.data, rows, 0)

        if flagColumn:
            columns = []
            columns_objs_buffer = []
            for i_str in cols:
                try:
                    i = dispatcher.data.getIndexColumn(i_str)
                    if i < 0:
                        return ERRORS.PARAMETER_VALUE_ERROR, "A column index must a positive integer"
                    if i >= rows_size:
                        return ERRORS.PARAMETER_VALUE_ERROR, f'A column index must less than column size ({cols_size})'

                    columns.append(i)
                    columns_objs_buffer.append(dispatcher.data.columns[i])
                except DatasetException:
                    return ERRORS.PARAMETER_VALUE_ERROR, f'Column {i_str} is not valid'
            dispatcher.data.set_data(np.delete(dispatcher.data.data, columns, 1))  
            for x in columns_objs_buffer:   #Delete columns object
                dispatcher.data.columns.remove(x)
        return ERRORS.OK, ''
    except DatasetException as e:
        return ERRORS.DATASET_COLUMN_NOT_PRESENT, ''
    except FileExistsError as e:
        return ERRORS.DATASET_NOTFOUND, ''