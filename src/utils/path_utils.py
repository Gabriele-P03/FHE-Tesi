import os
import sys

import re

sys.path.append('../exception')

from exception import command_exception

def listDataset():
    execPath = os.path.dirname(__file__)
    execPath += '/../../dataset/'
    files = os.listdir(execPath)
    return files

def getDataset(file: str):
    if not re.fullmatch(r'^[a-zA-Z0-9_]+\.csv$', file):
        raise command_exception.CommandException("Path " + file + " is not valid")
    
    execPath = os.path.dirname(__file__)
    execPath += '/../../dataset/'+file
    return open(execPath, 'r')
    
def readResourceFile(path: str, size: int = -1, mode: str = 'r') -> str:
    execPath = os.path.dirname(__file__)
    execPath += '/../../resources/'+path
    
    with open(execPath, mode) as file:
        return file.read(size)
    
def saveFile(file: str, data, mode: str = 'w'):
    execPath = os.path.dirname(__file__)
    execPath += '/../../resources/'+file
    
    with open(execPath, mode) as file:
        return file.write(data)

def getResourceFile(server: bool):
    execPath = os.path.dirname(__file__)
    execPath += '/../../resources/'
    if server:
        execPath += 'server_config.json'
    else:
        execPath += 'client_config.json'
    return open(execPath)