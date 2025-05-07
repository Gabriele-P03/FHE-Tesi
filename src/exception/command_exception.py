class CommandException(BaseException):

    def __new__(cls, msg: str):
        inst = super().__new__(msg)
        return inst
