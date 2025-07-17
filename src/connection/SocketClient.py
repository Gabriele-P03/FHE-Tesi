import socket
import logger.logger as logger

import sys
sys.path.append('../parameters')
from parameters.parameters import INSTANCE

sys.path.append('../fhe')
from sec.aes import AES

sys.path.append('../utils')
from utils import pk_exchange, socket_utils

sys.path.append('../comunication')
from comunication.producer.producer import Producer, Packet
from comunication.operations import OPERATIONS
from comunication.producer.viewer import view 

from Crypto.Util.Padding import unpad

class SocketClient:

    __socket = None
    __aes: AES = None
    __producer: Producer = None

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.connect( (INSTANCE.server_ip.value, INSTANCE.server_port.value) )
        logger.info("Client connected to " + str(INSTANCE.server_ip.value) + ":" + str(INSTANCE.server_port.value))

        self.__aes = AES()
        pk_exchange.exchange(self.__socket, bytes(self.__aes.aesKeyStr, encoding='utf8'))

        self.__producer = Producer()
    
    def loop(self):
        flag = True
        while flag:
            cmd = input('Enter a new command: ')
            p: Packet = self.__producer.execute(cmd, self.__socket)
            if p is not None:
                if p.op == OPERATIONS.CLOSE.value:
                    logger.info('Exiting...')
                    exit(1)
                data, size = socket_utils.recv(self.__socket)
                data = self.__aes.cipher.decrypt(data)
                data = unpad(data, 32)
                packet: Packet = Packet(_json=str(data, encoding='utf8'))
                logger.info('Request: ' + str(p.op) + ' -> ' + str(packet.status) + ': ' + packet.msg)
                if packet.status == 0:
                    view(p, packet, self.__aes)

                
    def close(self):
        if self.__socket is not None:
            self.__producer.execute('close', self.__socket)
        self.__socket.close()



