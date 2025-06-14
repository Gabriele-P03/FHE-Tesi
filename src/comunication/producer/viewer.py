import sys

sys.path.append('../')
from comunication.packet import Packet
from comunication.operations import OPERATIONS

sys.path.append('../../sec')
from sec.aes import AES 

sys.path.append('../../logger')
from logger import logger

import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def view(req: Packet, res: Packet, aes: AES):
    if req.op in [OPERATIONS.SCREEN.value, OPERATIONS.AVG.value, OPERATIONS.STD.value]:
        logger.info("Printing Current Cyphertext")
        data = json.loads(res.data)
        logger.dbg(f'Dec {len(res.data)} bytes of ciphertext')
        columns = data['columns']
        for i in range(len(columns)):
            c = columns[i]
            print(f'{c}', end='')
            if i < len(columns)-1:
                print(',\t', end='')
        data = data['data']
        print("\n---------------------------------------------------------------------------")
        
        for row in data:
            l = len(row)
            for i in range(0,l):
                value = row[i]
                print(f'{value}', end='')
                if i < l-1:
                    print(', ', end='')
            print()
        print("---------------------------------------------------------------------------")