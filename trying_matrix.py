class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
    def s(self):
        return sum(sum(i) for i in self.matrix)
    def copy(A, i=0):
        if i < len(A) - 1:
            return [A[i]] + [c(A, i+1)]
        else:
            return A[i]
    def multiply(A, l = 1):
        A = A.matrix
        B = []
        for i in range(len(A)):
            B.append([])
            for j in range(len(A[0])):
                B[i].append(l * A[i][j])
        return B
    def transpose_rec(A, i=0):
        A = A.matrix
        j = list(map(lambda x: x[i], A))
        try:
            return [j] + transpose_rec(A, i+1)
        except:
            return [j]
    def multiplication(A, B, i=0):
        j = list(map(lambda x, y: x * y, A[i], B[i]))
        try:
            return [j] + multiplication(A, B, i+1)
        except:
            return [j]
