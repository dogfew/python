import numpy as np 


def fib(n):
    matrix = np.array([[1, 1], 
                       [1, 0]], dtype=object)
    result = np.array([[1, 1], 
                       [1, 0]], dtype=object)
    for x in bin(n)[2:][::-1]:
        if x == '1':
            result = result @ matrix
        matrix = matrix @ matrix
    return result[1][1] if n & 1 or n > 0 else - result[1][1]
