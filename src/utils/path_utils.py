import os
import sys

sys.path.append('../exception')

from exception import command_exception

def getDataset(file: str) -> str:
    if '..' in file or '/' in file or not file.endswith('.csv'):
        raise command_exception.CommandException("Path " + file + " is not valid")
    
    return readResourceFile(file)
    
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