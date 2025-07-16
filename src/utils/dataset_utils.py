import sys

sys.path.append('../')
from exception import dataset_exception

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