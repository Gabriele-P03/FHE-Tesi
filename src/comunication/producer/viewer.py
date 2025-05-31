import sys

sys.path.append('../')
from comunication.packet import Packet
from comunication.operations import OPERATIONS

sys.path.append('../../sec')
from sec.rsa import RSA 

sys.path.append('../../logger')
from logger import logger

import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def view(req: Packet, res: Packet, rsa: RSA):
    if req.op == OPERATIONS.SCREEN.value:
        logger.info("Printing Current Cyphertext")
        data = json.loads(res.data)
        logger.dbg(f'Dec {len(res.data)} bytes of ciphertext')
        print("---------------------------------------------------------------------------")
        for row in data:
            l = len(row)
            for i in range(0,l):
                value = row[i]
                print(f'{value}', end='')
                if i < l-1:
                    print(', ', end='')
            print()
        print("---------------------------------------------------------------------------")