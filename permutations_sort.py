from itertools import permutations


def permutations_sort(lst):
    for seq in permutations(lst):
        for i in range(len(seq) - 1):
            if seq[i] > seq[i + 1]:
                break
        else:
            return list(seq)
