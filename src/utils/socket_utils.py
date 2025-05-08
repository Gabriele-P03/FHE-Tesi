import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

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
