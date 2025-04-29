'''

In this class will be stored, after have checked successfully, parameters passed via CLI

'''

import logger.logger as logger;

#Library used in order to retrieve parameters
import sys as s;
from .parameter import Parameter



class Parameters:

    size = 0

    verbosity = Parameter('v', 'verbose', False, False, False, bool)
    port = Parameter('p', 'port', 0, 8080, True,int)
    server_ip = Parameter('s', 'server', '', 'localhost', True, str)
    server_port = Parameter('e', 'serverport', 0, 8080, True, int)
    buffer_size = Parameter('b', 'buffer', 0, 10000, True, int)
    packet_size = Parameter('p', 'packet', 0, 256, True, int)

    __mapper = {
        'vverbosity': verbosity,
        'pport': port,
        'sserver': server_ip,
        'eserverport': server_port,
        'bbuffer': buffer_size,
        'ppacket': packet_size
    }

    def __init__(self):
        size = len(s.argv)

        for i in range(0, size):
            var = s.argv[i]

            if var.startswith('--'):
                self.__checkDoubleDashParameter(var[2:])
            elif var.startswith('-'):
                flag = self.__checkSingleDashParameter(var[1:], i)
                if flag:
                    i = i+1
        
        self.integrate()
        self.recap()

    #Check if there are some parameters which conflict with other ones
    def integrate(self):
        logger.info("Checking Parameters...")
        server = self.port.assigned   #True if it has been runned as Server (port assigned)
        client = self.server_ip.assigned or self.server_port.assigned #True if it has been runned as CLient (either server port or address assigned)
        if server and client:
            raise RuntimeError("Application does not support Client and Server running mode both")
        
        if not server and not client:
            self.port.invokeConvertMethod(self.port.defaultValue)
            self.buffer_size.invokeConvertMethod(self.buffer_size.defaultValue)
            self.packet_size.invokeConvertMethod(self.packet_size.defaultValue)
            logger.info("Neither Server nor Client mode detected. I am going running as Server listening on port " + str(self.port.defaultValue) + " with a buffer of " + str(self.buffer_size.defaultValue) + " bytes and a packet of " + str(self.packet_size.defaultValue) + " bytes")
        else:
            if not server:
                logger.info("Client mode detected...")
                if not self.server_ip.assigned:
                    self.server_ip.invokeConvertMethod(self.server_ip.defaultValue)
                    logger.info("Server addres has not been declared. This client is going to connect to " + str(self.server_ip.defaultValue))
                if not self.server_port.assigned:
                    self.server_port.invokeConvertMethod(self.server_port.defaultValue)
                    logger.info("Server Port has not been declared. This client is going to connect to " + str(self.server_port.defaultValue))
            
            if not client:
                logger.info("Server mode detected...")
                if not self.port.assigned:
                    self.port.invokeConvertMethod(self.port.defaultValue)
                    logger.info("Port server has to listen on was not declared. It is going to use " + str(self.port.defaultValue))
            if not self.buffer_size.assigned:
                self.buffer_size.invokeConvertMethod(self.buffer_size.defaultValue)
                logger.info("Buffer's Max Size has not beed declared. It is going to be set as " + str(self.buffer_size.defaultValue))
            if not self.packet_size.assigned:
                self.packet_size.invokeConvertMethod(self.packet_size.defaultValue)
                logger.info("Packet's Max Size has not been declared. It is going to be set as " + str(self.packet_size.defaultValue))


    def recap(self):
        if self.verbosity.value:
            logger.info(" ------------------------ PRINTING PARAMETERS ------------------------ ")
            if self.port.assigned:
                logger.info('Server Mode')
            else:
                logger.info('Client Mode')
            for par in self.__mapper:
                parameter = self.__mapper[par]
                value = ''
                if parameter.assigned:
                    value = str(parameter.value)
                logger.info(parameter.extendedkey + " -> " + value)
            logger.info(" --------------------------------------------------------------------- ")
    
    def __checkDoubleDashParameter(self, param: str) -> bool:
        if len(param) == 0:
            raise RuntimeError("There is a parameter")
        
        equalIndex = param.find('=')
        if equalIndex < 0:
            equalIndex = len(param)

        key = param[:equalIndex]
        value = ''

        for par in self.__mapper:
            if par[1:] == key:
                parameter = self.__mapper[par]

                valuable = parameter.valuable
                if valuable:
                    equalIndex = param.find('=')
                    if equalIndex < 2:  #A double dash parameter has always to begin at least with two letters
                        raise RuntimeError("Parameter " + param + " is not valid")
                    value = param[equalIndex+1:]
                self.__checkParameter(parameter, value)
                
                return valuable
        
        return False
        
    def __checkSingleDashParameter(self, param: str, i: int) -> bool:

        for par in self.__mapper:
            if par[0:1] == param:
                parameter = self.__mapper[par]

                valuable = parameter.valuable
                value = True
                if valuable:
                    value = s.argv[i+1]

                self.__checkParameter(parameter, value)

                return valuable
        
        return False

    def __checkParameter(self, parameter: Parameter, value: str):
        parameter.invokeConvertMethod(value) 


INSTANCE = Parameters()