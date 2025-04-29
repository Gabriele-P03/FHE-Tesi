import socket
import logger.logger as logger

import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../fhe')
from fhe.fhe import FHE

from util.public_key import PublicKey

sys.path.append('../utils')
from utils import pk_exchange

class SocketClient:

    __socket = None

    __pk : PublicKey = None

    __fhe: FHE = None

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.connect( (INSTANCE.server_ip.value, INSTANCE.server_port.value) )
        logger.info("Client connected to " + str(INSTANCE.server_ip.value) + ":" + str(INSTANCE.server_port.value))

        self.__fhe = FHE()
        self.__pk = pk_exchange.exchange(self.__socket, self.__fhe.pk)




