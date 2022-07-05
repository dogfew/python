def merge_sort(seq):
    if len(seq) <= 1:
        return seq
    n = len(seq) // 2
    a = merge_sort(seq[:n])
    b = merge_sort(seq[n:])
    out = []
    i, j = 0, 0
    while True:
        x, y = a[i], b[j]
        if x < y:
            out.append(x)
            i += 1
            if i == len(a):
                break
        else:
            out.append(y)
            j += 1
            if j == len(b):
                break
    out.extend(a[i:])
    out.extend(b[j:])
    return out
