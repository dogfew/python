def transpose(A, i=0): 
    j = list(map(lambda x: x[i], A))
    try:
        return [j] + transpose(A, i+1)
    except:
        return [j]
def scalar(A, B, i=0):
    j = list(map(lambda x, y: x * y, A[i], B[i]))
    try: 
        return [j] + scalar(A, B, i+1)
    except:
        return [j]
def zeros(size, i=0):
    return [[*[0]*size] for i in range(size)]
def eye(size):
    line = [1] + [*[0]*(size-1)]
    return [line[-i:] + line[:-i] for i in range(size)]
def multiplication(A, B, i=0):
    C = []
    for i in A:
        C_i = []
        for j in B:
            C_ij = sum(map(lambda x, y: x * y, i, j))
            C_i.append(C_ij)
        C.append(C_i)
    return C
def det(A):
    if len(A) > 2: 
        B, C = [line[:0] + line[1:] for line in A], [line[0] for line in A]
        return sum(x * det(B[:i] + B[i+1:]) * (-1) ** (i) for i, x in enumerate(C))
    else:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
