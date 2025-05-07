import os
import sys

sys.path.append('../exception')

from exception import command_exception

def getDataset(file: str) -> str:
    if '..' in file or '/' in file or not file.endswith('.csv'):
        raise command_exception.CommandException("Path " + file + " is not valid")
    
    execPath = os.path.dirname(__file__)
    execPath += '/../../resources/'+file
    
    with open(execPath, 'r') as file:
        return file.read()

def getResourceFile(server: bool):
    execPath = os.path.dirname(__file__)
    execPath += '/../../resources/'
    if server:
        execPath += 'server_config.json'
    else:
        execPath += 'client_config.json'
    return open(execPath)