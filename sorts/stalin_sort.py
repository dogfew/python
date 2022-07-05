def stalin_sort(seq):
    max_elem = seq[0]
    sorted_seq = []
    for elem in seq:
        if elem >= max_elem:
            max_elem = elem
            sorted_seq.append(elem)
    return sorted_seq
