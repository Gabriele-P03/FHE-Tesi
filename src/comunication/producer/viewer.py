import sys

sys.path.append('../')
from comunication.packet import Packet
from comunication.operations import OPERATIONS

sys.path.append('../../fhe')
from fhe.fhe import FHE 

sys.path.append('../../logger')
from logger import logger

from openfhe import DeserializeCiphertextString, BINARY, Ciphertext
import json, binascii

def view(req: Packet, res: Packet, fhe: FHE):
    if req.op == OPERATIONS.SCREEN.value:
        logger.info("Printing Current Cyphertext")
        data = json.loads(res.data)
        logger.dbg(f'Dec {len(res.data)} bytes of ciphertext')
        print("---------------------------------------------------------------------------\n")
        for row in data:
            l = len(row)
            for i in range(0,l):
                value = row[i]
                value: bytes = eval(value)
                c: Ciphertext = DeserializeCiphertextString(value, BINARY)
                s = str(fhe.cc.Decrypt(fhe.secretKey, c).GetCKKSPackedValue()[0].real)
                print(f'{s}')
                if i < l-1:
                    print(', ')
            print('\n')
        print("---------------------------------------------------------------------------")