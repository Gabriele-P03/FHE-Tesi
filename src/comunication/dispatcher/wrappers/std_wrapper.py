'''

There's no trivial way to carry out square root in FHE, therefore this application will decrypt deviation and then
carry out square root on it

'''

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

import math

sys.path.append('../../../exception')
from exception.command_exception import CommandException
from exception.dataset_exception import DatasetException

import json


def std(op: Operation, dispatcher: Dispatcher, fhe: FHE) -> ERRORS:
    logger.info("Executing Standard Deviation")
    if dispatcher.data is None:
        return ERRORS.NO_DATASET_LOADED
    try:
        dataset = dispatcher.data
        row_size = dispatcher.data.size
        row_size_cpt = fhe.cc.Encrypt(fhe.publicKey, fhe.cc.MakeCKKSPackedPlaintext([1/row_size])) #Row size as ciphertext

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

        js = {}
        buffer = [] #This array will contain deviation standard
        dataset = dataset.data

        for j in ext_indeces:
            #j is the col in loaded dataset, therefore it is going to calculate std for each column
            ciphertext_buffer = None
            for i1 in range(0,row_size):
                c = dataset[i1][j]
                if i1 == 0:
                    ciphertext_buffer = c
                else:
                    ciphertext_buffer = fhe.cc.EvalAdd(ciphertext_buffer, c)

            avg = fhe.cc.EvalMultNoRelin(ciphertext_buffer, row_size_cpt)
            #Now that we have avg, we can calculate std

            ciphertext_buffer = None
            for i1 in range(0,row_size):
                c = dataset[i1][j]
                ciphertext_tmp = fhe.cc.EvalSub(c, avg) #Sub avergae
                ciphertext_tmp = fhe.cc.EvalMultNoRelin(ciphertext_tmp,ciphertext_tmp) #Power 2
                if i1 == 0:
                    ciphertext_buffer = ciphertext_tmp #At step 0, buffer is None
                else:
                    ciphertext_buffer = fhe.cc.EvalAdd(ciphertext_buffer, ciphertext_tmp)
                    std = fhe.cc.Decrypt(fhe.secretKey, ciphertext_buffer).GetCKKSPackedValue()[0].real
            ciphertext_buffer = fhe.cc.EvalMultNoRelin(ciphertext_buffer, row_size_cpt)#Division by size
            dev = fhe.cc.Decrypt(fhe.secretKey, ciphertext_buffer).GetCKKSPackedValue()[0].real
            std = math.sqrt(dev)
            buffer.append(std)
        
        js["columns"] = cols
        js["data"] = [buffer]
        
        return ERRORS.OK, json.dumps(js)
    except DatasetException as e:
        return ERRORS.DATASET_COLUMN_NOT_PRESENT
    except FileNotFoundError as e:
        return ERRORS.DATASET_NOTFOUND