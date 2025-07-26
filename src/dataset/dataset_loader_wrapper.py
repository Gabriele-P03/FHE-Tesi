'''

In this python file there will be defined loader functions for each dataset type

'''

from parameters.parameters import INSTANCE
from dataset.column import Column

import sys
sys.path.append('../fhe')
from sec.fhe import FHE

sys.path.append('../logger')
from logger import logger

import psutil
from openpyxl import Workbook
import datetime

wb = Workbook()
ws = wb.active

def load_csv(stream, fhe: FHE, separator = ';', reciprocal=False):
    headers_str: str = stream.readline()
    headers_str_splitted = headers_str.split(separator)
    columns = [ Column(c) for c in headers_str_splitted ]
    logger.info(f'Loading {len(columns)} columns')
    data = []
    cc = fhe.cc
    pk = fhe.publicKey
    row_index = 0
    #ps = pre = psutil.Process()
    #dt = datetime.datetime.now()
    #ws.append([str(dt)])
    for line in stream:
        #pre = ps.memory_info().rss
        row_index += 1
        #Parsing single line
        values = line.split(separator)#Splitting values
        ciphertexts = []
        print(str(row_index))
        for i in range(len(values)):
            f = []
            try:
                x = float(values[i])
                if reciprocal:
                    x = 1/x
                x = truncate(x)
                f.append(x)
            except ValueError as e:
                raise ValueError(f'Row {str(row_index)} Col {columns[i].name} has an invalid value: {str(values[i])}')

            pltxt = cc.MakeCKKSPackedPlaintext(f)
            enc = cc.Encrypt(pk, pltxt)
            ciphertexts.append(enc)    
        data.append(ciphertexts)
        
    #    ws.append([row_index, pre, ps.memory_info().rss])

    #file_name = 'test_'+str(datetime.datetime.now())+'_'
    #if INSTANCE.port.assigned:
    #    file_name += 's'
    #else:
    #    file_name = 'c'
    #ws.append([str(datetime.datetime.now())])
    #wb.save('/home/gabrielepace_std/FHE-Tesi/test/'+file_name+'.xlsx')    
    return columns, data

import math
coef = 1000 #3 cifre decimali
def truncate(x):
    return math.floor(x*coef)/coef


