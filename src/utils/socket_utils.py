import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../logger')
from logger import logger

def recv(__socket):
    size = 0
    data = b''
    bSize = INSTANCE.buffer_size.value
    pSize = INSTANCE.packet_size.value
    while True:
        if size > bSize:
            break
        if len(data) > 0:
            if b'\n' == data[-1:]:
                break
        tmp = __socket.recv(pSize)
        data += tmp
        size += len(tmp)
    return data, size



def send(__socket, data: bytes):
    size = len(data)
    pSize = INSTANCE.packet_size.value    
    it = int((size/pSize))+1
    for i in range(0, it):
        start = i*pSize
        end = min( size-i*pSize, pSize) 
        __socket.sendall(data[start:start+end])
    __socket.sendall(b'\n')