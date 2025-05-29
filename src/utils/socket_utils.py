import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../logger')
from logger import logger

import zlib

def recv(__socket):
    size = 0
    data = b''
    bSize = INSTANCE.buffer_size.value
    pSize = INSTANCE.packet_size.value
    i = 0
    while True:
        i += 1
        if size > bSize:
            break
        if len(data) > 0:
            if b'\0\0\0\0\0\0\0\0' == data[-8:]:
                break
        tmp = __socket.recv(pSize)
        data += tmp
        size += len(tmp)
        #logger.dbg(f'Read i: {i} -> {size} bytes')
    data = data[:-8]
    data = zlib.decompress(data)
    return data, size-8



def send(__socket, data: bytes):

    data = zlib.compress(data)

    size = len(data)
    pSize = INSTANCE.packet_size.value    
    it = int((size/pSize))+1
    #logger.warn(f'Size: {size}. It: {it}')
    for i in range(0, it):
        start = i*pSize
        end = min( size-i*pSize, pSize) 
        #logger.warn(f'i: {i}. Start: {start}. End: {end}')
        __socket.sendall(data[start:start+end])
    __socket.sendall(b'\0\0\0\0\0\0\0\0')