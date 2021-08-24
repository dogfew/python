import numpy as np
def spiralize(size):
    spiral = np.zeros((size, size), dtype=np.int8)
    i_0, j_0 = 0, 0 
    i, j = 0, size - 1
    spiral[i, j_0:j] = 1 
    for number, x in enumerate(range(size - 1, -1, -2)):
        const = x * (-1) ** number
        i_0, i = i, i + const
        spiral[i_0:i, j] = 1 
        spiral[i:i_0, j] = 1 
        j_0, j = j, j - const 
        spiral[i, j_0:j] = 1 
        spiral[i, j:j_0 + 1] = 1 
    if size % 2 == 0: 
        spiral[i, j] = 0     
    return spiral.tolist()
