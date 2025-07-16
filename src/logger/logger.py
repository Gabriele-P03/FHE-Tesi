import datetime as dt
from enum import Enum
import traceback
from sys import gettrace as sys_gettrace

file_name = str(dt.datetime.now()).replace(' ', '_')
log_file = open('logs/'+file_name+'.txt', 'w+')

#DEBUG is true if debugger is attached
DEBUG = sys_gettrace() is not None

class LOGTYPE(Enum):
    INFO = 1
    WARN = 2
    ERR  = 3
    DBG  = 4 

class _LOGTYPE_COLORS(Enum):
    INFO = '\033[92m'
    WARN = '\033[93m'
    ERR  = '\033[91m'
    DBG  =  '\033[94m'

def _getColorByLogType(logtype: LOGTYPE):
    match logtype:
        case LOGTYPE.INFO:
            return _LOGTYPE_COLORS.INFO
        case LOGTYPE.WARN:
            return _LOGTYPE_COLORS.WARN   
        case LOGTYPE.ERR:
            return _LOGTYPE_COLORS.ERR   
        case LOGTYPE.DBG:
            return _LOGTYPE_COLORS.DBG

def _getCurrentTimestamp():
    return dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

def log(logtype: LOGTYPE, msg: str):
    color = _getColorByLogType(logtype).value
    ts = _getCurrentTimestamp()
    ts = "[ " + ts + " ]: "
    print(color + ts + msg)
    log_file.write(ts + msg + '\n')

def info(msg: str):
    log(LOGTYPE.INFO, msg)

def warn(msg: str):
    log(LOGTYPE.WARN, msg)

def err(msg: str):
    log(LOGTYPE.ERR, msg)

def dbg(msg: str):
    if not DEBUG:
        msg = "!!! DEBUGGER IS NOT ATTACHED !!!"    
    log(LOGTYPE.DBG, msg)

def throw(exc: Exception):
    err(exc.__str__())
    err(''.join(traceback.TracebackException.from_exception(exc).format()))