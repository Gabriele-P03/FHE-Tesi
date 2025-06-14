'''

In this python file there will be defined loader functions for each dataset type

'''

import openpyxl.workbook
from dataset.column import Column
from openfhe import Ciphertext

import sys
sys.path.append('../fhe')
from sec.fhe import FHE

sys.path.append('../comunication')
from comunication.errors import ERRORS

sys.path.append('../logger')
from logger import logger

import psutil
from openpyxl import Workbook, load_workbook

#wb = load_workbook('test.xlsx')
wb = Workbook()
ws = wb.active

def load_csv(stream, fhe: FHE, separator = ';', reciprocal=False):
    headers_str: str = stream.readline()
    headers_str_splitted = headers_str.split(separator)
    columns = [ Column(c) for c in headers_str_splitted ]
    data = []
    cc = fhe.cc
    pk = fhe.publicKey
    row_index = 0
    ps = pre = psutil.Process()
    for line in stream:
        pre = ps.memory_info().rss
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
                logger.err('Row ' + str(row_index) + " Col " + columns[i].name + " has an invalid value: " + str(values[i]) )

            pltxt = cc.MakeCKKSPackedPlaintext(f)
            enc = cc.Encrypt(pk, pltxt)
            ciphertexts.append(enc)    
        data.append(ciphertexts)
        
        ws.append([row_index, pre, ps.memory_info().rss])
    wb.save('test.xlsx')    
    return columns, data

import math
coef = 1000 #3 cifre decimali
def truncate(x):
    return math.floor(x*coef)/coef


