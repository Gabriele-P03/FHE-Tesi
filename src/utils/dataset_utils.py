import sys

sys.path.append('../')
from exception import dataset_exception, command_exception

sys.path.append('../')
from comunication.operations import Operation, OPERATIONS 

import re

def parseRowIndices(op: Operation) -> [int]:
    try:
        raw_rows = op.getParameterValue("rows")
    except command_exception.CommandException as e:
        return []
    if re.match(r"^[0-9]+:[0-9]+$", raw_rows):    #Range indices start:end
        splitted = raw_rows.split(":")
        try:
            start = int(splitted[0])
            end = int(splitted[1])
            return range(start, end+1)  #end+1 since end is exclusive
        except ValueError:
            raise command_exception.CommandException(f'{raw_rows} is not a valid row indices range')
    else:   #Range as csv
        splitted = raw_rows.split(";")
        rows = []
        for c in splitted:
            try:
                i = int(c)
            except ValueError:
                raise command_exception.CommandException(f'{c} is not a valid row index')
            rows.append(i)
        return rows

def match_indices_cols(cols1, cols2, dataset):
    if len(cols2) <= 0:
        cols2 = cols1

    indices = {}  
    columns_name_buffer = list( map(lambda x: x.name, dataset.columns) )  
    for i2 in range(len(cols2)):
        c2 = cols2[i2]
        dataset.hasColumn(c2)
        i = columns_name_buffer.index(c2)

        flag = False
        for i1 in range(len(cols1)):
            c1 = cols1[i1]
            if c1 == c2:
                flag = True
                indices.update({i1:i})
                break

        if not flag:
            raise dataset_exception.DatasetException(f'It seems like loaded dataset does not contain {c2} column')
    return indices