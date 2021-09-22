import itertools

a, b, c, d, t = 'a', 'b', 'c', 'd', 't'

def create_bin():
    print('Напишите через пробел ребра для вашего графа:\n')
    pairs = []
    while True:
        try:
            a, b = input().split()
            pairs.append((a, b))
        except Exception:            
                return pairs
            
            
def prod(A, B):
    pairs = set()
    for x, y_0 in A:
        for y_1, z in B:
            if y_0 == y_1:
                pairs.add((x, z))
    return pairs


def intersect(A, B):
    C = set()
    for pair in A:
        if pair in B:
            C.add(pair)
    return C

def complement(P):
    A = set()
    for x, y in P:
        A.add(x)
        A.add(y)
    return set(itertools.product(A, repeat=2)) - set(P)


def dual(A):
    return set([(y, x) for x, y in A])


def prop(P):
    A = set()
    for x, y in P:
        A.add(x)
        A.add(y)
    cartesian = itertools.product(A, repeat=2)
    P_c = complement(P)
    reflex = all((x, x) in P for x in A)
    anti_reflex = all((x, x) not in P for x in A)
    sim = all((x, y) in P for y, x in P)
    asim = all((x, y) not in P for y, x in P)
    anti_sim = all((y, x) not in P or (x == y) for x, y in P)
    full = all((y, x) in P or (x, y) in P for x, y in cartesian)
    coh = all(x == y or (y, x) in P or (x, y) in P for x, y in cartesian)
    trans = True
    flag = False
    for x, y_0 in P:
        for y_1, z in P:
            if y_0 != y_1: continue
            if (x, z) not in P:
                trans, flag = False, True
                break
        if flag: break
        
    neg_trans = True
    flag = False
    for x, y_0 in P_c:
        for y_1, z in P_c:
            if y_0 != y_1: continue
            if (x, z) not in P_c:
                neg_trans, flag = False, True
                break
        if flag: break
    cyc, acyc = cycle(P)
    properties = {'Рефлексивность': reflex,
                  'Антирефлексивность': anti_reflex,
                  'Симметричность': sim,
                  'Ассиметричность': asim,
                  'Антисимметричность': anti_sim,
                  'Полнота': full,
                  'Связность': coh,
                  'Транзитивность': trans,
                  'Отрицательная транзитивность': neg_trans,
                  'Цикличность': cyc,
                  'Ацикличность': acyc}

    return properties




def cycle(P):
    paths = {}
    P1 = P
    P1 = P1 + P1
    for x, y in P:
        x_one = x
        for y1, z in P1:
            if y1 != y:
                continue
            if x_one == z:
                paths[(x_one)] = True
                break
            x, y = y, z
        else:
            paths[(x_one)] = False
    cyc, acyc = all(paths), not any(paths)
    return cyc, acyc


def I(P): #отношение несравнимости
    A = set()
    for x, y in P:
        A.add(x)
        A.add(y)
    return set(itertools.product(A, repeat = 2)) - (set(P) | dual(P))

def I_1(A):
    return complement(set(A) | dual(A))

def I_2(A):
    return complement(set(A)) & complement(dual(A))

