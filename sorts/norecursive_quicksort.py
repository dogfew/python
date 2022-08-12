from random import randint, shuffle


def partition(lst, stack, left, right):
    pivot_index = randint(left, right - 1)
    pivot_value = lst[pivot_index]
    lt, eq, gt = [], [], []
    for element in lst[left:right]:
        if element < pivot_value:
            lt.append(element)
        elif element > pivot_value:
            gt.append(element)
        else:
            eq.append(element)
    lst[left:right] = lt + eq + gt
    if lt:
        stack.append((left, left + len(lt)))
    if gt:
        stack.append((left + len(lt) + len(eq), right))


def quicksort(lst):
    left, right = 0, len(lst)
    stack = [(left, right)]
    while stack:
        left, right = stack.pop(-1)
        partition(lst, stack, left, right)
    return lst


if __name__ == '__main__':
    for _ in range(100):
        a = randint(-255, 255)
        b = a + randint(1, 255)
        lst_ = list(range(a, b)) * randint(1, 5)
        shuffle(lst_)
        assert quicksort(lst_) == sorted(lst_)
