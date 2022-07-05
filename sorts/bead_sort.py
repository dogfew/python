import numpy as np


def bead_sort(lst):
    array = np.zeros((max(lst) + 1, max(lst) + 1))
    for i, x in enumerate(lst):
        array[i, :x] = 1
    transposed_array = np.sum(array, axis=0)
    res = [np.count_nonzero(transposed_array > i) for i in range(len(lst))]
    return res
