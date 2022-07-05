def radix_sort(lst):
    base_2_seq = []
    max_index = 0
    for elem in lst:
        base_2_elem = bin(elem)[2:]
        if len(base_2_elem) > max_index:
            max_index = len(base_2_elem)
        base_2_seq.append(base_2_elem)
    seq = [x.zfill(max_index) for x in base_2_seq]
    return helper(seq, 0, max_index)


def helper(seq, index, max_index):
    if index == max_index:
        return [int(x, base=2) for x in seq]
    ones = []
    zeros = []
    for x in seq:
        if x[index] == '0':
            zeros.append(x)
        else:
            ones.append(x)
    return helper(zeros, index+1, max_index) + helper(ones, index+1, max_index)


