def counting_sort(seq):
    lst = [0]
    for x in seq:
        lst.extend([0] * (x - len(lst) + 1))
        lst[x] += 1
    return [x for x, count in enumerate(lst) for _ in range(count)]