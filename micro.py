from sympy import Eq, solveset, diff, substitution
from sympy.abc import p


def first_degree(D):
    pi = p * (D)
    foc = diff(pi, p)
    coeffs = list(solveset(foc, p))
    return f"p = {coeffs[0]}"
    

def non_discrimination(Ds, explain=True):
    dictionary = {}
    for D in Ds:
        interval = list(solveset(D, p))[0]
        dictionary[D] = interval
    interval = 0
    function = 0
    sum_demands = {0:[0, 0]}
    prev_function = 0 
    for key, value in sorted(dictionary.items(), key=lambda x: x[1])[::-1]:
        function += key
        sum_demands[function] = [value, 0]
        sum_demands[prev_function][1] = value
        prev_function = function
    sum_demands.pop(0)
    profits = {}
    for D, interval in sum_demands.items():
        profit = D * p
        foc = solveset(diff(profit, p))
        coeff = list(foc)[0]
        if interval[1] <= coeff <= interval[0]:
            items = [(profit.subs(p, v), v) for v in [interval[0], interval[1], coeff]]
            profits[D] = sorted(items, key=lambda x: x[0])[-1]
        elif coeff > interval[0]:
            profits[D] = [profit.subs(p, interval[0]), interval[0]]
        else:
            profits[D] = [profit.subs(p, interval[1]), interval[1]]
    function, pp = sorted(profits.items(), key=lambda x: x[1][0])[-1]
    
    if explain: ###Пояснение!
        print('Intervals and summed demands:')
        for key, value in sum_demands.items():
            print(f'{key} -> {min(value), max(value)}')
        print()
        print('Maximum profits for each interval')
        for key, value in profits.items(): 
            print(f'{key}: max profit is {value[0]} with price {value[1]}')
        print()
    return f'Function: {function}\nPrice: {pp[1]}\nProfit: {pp[0]}'

D_1 = 2 -  p
D_2 = 3 - 2 * p
D_3 = 4 - 4 * p
D = [D_1, D_2, D_3]
print(non_discrimination(D))




    