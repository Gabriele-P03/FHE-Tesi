import socketserver
import socket
from parameters.parameters import INSTANCE
import logger.logger as logger

import sys
sys.path.append('../fhe')
from fhe.fhe import FHE

sys.path.append('../utils')
from utils import pk_exchange
from utils import socket_utils
from util.public_key import PublicKey

sys.path.append('../comunication')
from comunication.dispatcher.dispatcher import Dispatcher
from comunication.operations import OPERATIONS

port = INSTANCE.port.value
host = 'localhost'

class SocketServer(socketserver.BaseRequestHandler):

    fhe: FHE = None

    __pk: PublicKey = None

    __connected = False

    __dispatcher: Dispatcher = None

    def handle(self):
        logger.info("Connection enstabilished with " + self.client_address[0])
        self.fhe = FHE()
        self.__pk = pk_exchange.exchange(self.request, self.fhe.publicKey)
        self.fhe.setPK(self.__pk)
        self.__connected = True
        self.__dispatcher = Dispatcher()

        self.loop()

    def loop(self):
        flag = True
        while flag:
            logger.info("Waiting for a new command...")
            data, size = socket_utils.recv(self.request)
            json_string = str(data, encoding='utf8')
            packet = self.__dispatcher.dispatch(json_string, self.fhe)
            if packet.op == OPERATIONS.CLOSE.value:
                flag = False
            self.request.sendall(bytes(packet.json(), encoding='utf8')+b'\0\0\0\0\0\0\0\0')


        
def getIstance() -> socketserver.TCPServer:
    __instance = socketserver.TCPServer( (host, port), SocketServer)
    __instance.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    logger.info("Server Socket listening...")
    return __instance
