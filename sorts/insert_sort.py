from bisect import bisect_left


def insert_sort(lst):
    sorted_seq = []
    for item_1 in lst:
        coord = bisect_left(sorted_seq, item_1)
        sorted_seq.insert(coord, item_1)
    return sorted_seq
