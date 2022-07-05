from random import choice


def quicksort(lst):
    if len(lst) <= 1:
        return lst
    k = choice(lst)
    le = []
    gt = []
    eq = []
    for i in lst:
        if i < k:
            le.append(i)
        elif i == k:
            eq.append(i)
        else:
            gt.append(i)
    return quicksort(le) + eq + quicksort(gt)