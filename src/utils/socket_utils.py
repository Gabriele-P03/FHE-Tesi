import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

def recv(__socket):
    size = 0
    data = [b'']
    bSize = INSTANCE.buffer_size.value
    pSize = INSTANCE.packet_size.value
    while b'\n' not in data[-1] and size < bSize:
        tmp = __socket.recv(pSize)
        data.append(tmp)
        size += len(tmp)
    return data, size
