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
        self.__pk = pk_exchange.exchange(self.request, self.fhe.pk)
        self.__connected = True
        self.__dispatcher = Dispatcher()

        self.loop()

    def loop(self):
        logger.info("Receiving...")
        data, size = socket_utils.recv(self.request)
        json_string = str(data, encoding='utf8')
        self.__dispatcher.dispatch(json_string, self.fhe)

        
def getIstance() -> socketserver.TCPServer:
    
    with socketserver.TCPServer( (host, port), SocketServer) as server:
        server.serve_forever()
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    logger.info("Server Socket listening...")
    return server
