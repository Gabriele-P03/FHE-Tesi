from json import JSONEncoder

def beautify_key(str):

    try:
        index = str.index('__')
        if index <= 0:
            return str

        return str[index + 2:]
    except ValueError:
        return str

class JsonEncoder(JSONEncoder):

    def default(self, o):
        return {beautify_key(k) : v for k, v in vars(o).items()}