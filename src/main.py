'''

This is meant to be the main python file of this FHE implementation project.

A secured connection is enstabilished between two end-point

'''

import logger.logger as logger
from parameters.parameters import INSTANCE
from connection import SocketServer, SocketClient

from sec import fhe

import sys
import atexit

def excepthook(type, value, tb):
    logger.throw(value)

def init():
    logger.info("Initializing Excepthook")
    sys.excepthook = excepthook

__socket = None

def run():
    global __socket
    logger.info("Running FHE Implementation Project")
    if INSTANCE.port.assigned:
        __socket = SocketServer.getIstance()
        atexit.register(onExitServer)
        __socket.serve_forever()
    else:
        __socket = SocketClient.SocketClient()
        atexit.register(onExitClient)
        __socket.loop()

def onExitServer():
    global __socket
    logger.info("Closing Server...")
    __socket.server_close()
def onExitClient():
        global __socket
        logger.info("Closing Client...")
        __socket.close()


if __name__ == '__main__':
    init()
    run()
