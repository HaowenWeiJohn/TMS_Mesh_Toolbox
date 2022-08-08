import xml.etree.ElementTree as ET
import pickle

import numpy as np

file_name = 'aapo_tms'
tree = ET.parse("../data/coil_positions/aapo_tms.xml")
root = tree.getroot()

trans_matrices = dict()
for index, matrix_info in enumerate(root.iter('Matrix4D')):
    matrix_dict = matrix_info.attrib
    # dict = {"a": 1, "b": 2, "c": 3, "d": 4}

    trans_matrix = list(matrix_dict.values())
    # an_array = np.array(data)
    trans_matrix = list(map(float, trans_matrix))
    trans_matrix = np.array(trans_matrix)
    trans_matrix = np.reshape(trans_matrix, (4, 4))
    trans_matrices[index] = trans_matrix
    # print(an_array)


with open(file_name+'.pickle', 'wb') as handle:
    pickle.dump(trans_matrices, handle, protocol=pickle.HIGHEST_PROTOCOL)



