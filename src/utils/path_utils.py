import os


def getResourceFile(server: bool):
    execPath = os.path.dirname(__file__)
    execPath += '/../../resources/'
    if server:
        execPath += 'server_config.json'
    else:
        execPath += 'client_config.json'
    return open(execPath)