'''

In this python file there will be defined loader functions for each dataset type

'''

from column import Column

def load_csv(stream, separator = ';'):
    headers_str: str = stream.readline()
    headers_str_splitted = headers_str.split(separator)
    columns = [ Column[str](c) for c in headers_str_splitted ]
    data = [[]]
    size_c = len(columns)
    for line in stream:
        #Parsing single line
        values = line.split(separator)
        data.append(values)
    return columns, data

