def primesTo(n):    
    x = [i for i in range(2, n)]
    a = []
    sqrt = max(x) ** 0.5
    current_prime = 0
    while len(x) >= 1 and current_prime < sqrt:
        current_prime = x[0]
        a.append(x[0])
        x = list(filter(lambda v: v % current_prime != 0, x))
    primes = a + x
    return primes
print(primesTo(int(input())))
