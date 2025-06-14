import socketserver
import socket
from parameters.parameters import INSTANCE
import logger.logger as logger

import sys, json
sys.path.append('../fhe')
from sec.fhe import FHE

sys.path.append('../utils')
from utils import pk_exchange
from utils import socket_utils

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

sys.path.append('../comunication')
from comunication.dispatcher.dispatcher import Dispatcher
from comunication.operations import OPERATIONS

import zlib

port = INSTANCE.port.value
host = 'localhost'


class SocketServer(socketserver.BaseRequestHandler):

    fhe: FHE = None

    __aes = None

    __connected = False

    __dispatcher: Dispatcher = None

    def handle(self):
        logger.info("Connection enstabilished with " + self.client_address[0])
        self.fhe = FHE()
        rsa_pub_str = self.fhe.rsaPublicKeyStr
        client_enc_aes_key = pk_exchange.exchange(self.request, rsa_pub_str)
        aes_key_client = self.fhe.rsaPrivateKey.decrypt(client_enc_aes_key, padding.OAEP(
                                                                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                            algorithm=hashes.SHA256(),
                                                                            label=None)
        )
        self.__aes = AES.new(aes_key_client, AES.MODE_ECB)
        
        self.__dispatcher = Dispatcher()

        self.loop()

    def loop(self):
        flag = True
        while flag:
            logger.info("Waiting for a new command...")
            data, size = socket_utils.recv(self.request)
            json_string = str(data, encoding='utf8')
            packet = self.__dispatcher.dispatch(json_string, self.fhe)
            buffer = bytes(json.dumps(packet.json()), encoding='utf8')
            buffer = self.__aes.encrypt(pad(buffer, 32))

            buffer = zlib.compress(buffer)+b'\0\0\0\0\0\0\0\0'
            self.request.sendall(buffer)


        
def getIstance() -> socketserver.TCPServer:
    __instance = socketserver.TCPServer( (host, port), SocketServer)
    __instance.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    logger.info("Server Socket listening...")
    return __instance
