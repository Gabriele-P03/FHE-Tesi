
class Parameter[T]:

    __key = ''
    __extendedKey = ''

    value = ''

    valuable = True

    __convertMethod = None

    __assigned = False

    __defaultValue = ''

    def __init__(self, key: str, extendedKey: str, value: T, defaultValue: T, valuable: bool, convertMethod):
        self.__key = key
        self.__extendedKey = extendedKey
        self.value = convertMethod(value)
        self.valuable = valuable

        self.__defaultValue = defaultValue
        self.__convertMethod = convertMethod
        

    @property
    def key(self) -> str:
        return self.__key
    
    @property
    def extendedkey(self) -> str:
        return self.__extendedKey
    
    @property
    def assigned(self) -> bool:
        return self.__assigned
    
    @property
    def defaultValue(self) -> T:
        return self.__defaultValue
    
    def invokeConvertMethod(self, value: T):        
        if self.__assigned:
            raise RuntimeError("Parameter " + self.__extendedKey + " has been already assigned")
        self.value = self.__convertMethod(value)
        self.__assigned = True
    

    