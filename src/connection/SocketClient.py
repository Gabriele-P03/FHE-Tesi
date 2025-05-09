import socket
import logger.logger as logger

import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../fhe')
from fhe.fhe import FHE

from util.public_key import PublicKey

sys.path.append('../utils')
from utils import pk_exchange, socket_utils

sys.path.append('../comunication')
from comunication.producer.producer import Producer, Packet 

class SocketClient:

    __socket = None

    __pk : PublicKey = None

    __fhe: FHE = None

    __producer: Producer = None

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.connect( (INSTANCE.server_ip.value, INSTANCE.server_port.value) )
        logger.info("Client connected to " + str(INSTANCE.server_ip.value) + ":" + str(INSTANCE.server_port.value))

        self.__fhe = FHE()
        self.__pk = pk_exchange.exchange(self.__socket, self.__fhe.publicKey)

        self.__producer = Producer()
    
    def loop(self):
        flag = True
        while flag:
            cmd = input('Enter a new command: ')
            p: Packet = self.__producer.execute(cmd, self.__socket)
            data, size = socket_utils.recv(self.__socket)
            packet: Packet = Packet(_json=str(data, encoding='utf8'))
            logger.info('Request: ' + str(p.op) + ' -> ' + str(packet.status) + ': ' + packet.msg)
                




