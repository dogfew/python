import math
N = int(input())
prime_numbers = [2, 3]
i = 0
n = 0
while i < N - 2:
    prime_1 = True
    prime_2 = True
    k, m = n + 7, n + 5
    n = n + 6
    sqrt = int(math.sqrt(m))
    for j in prime_numbers:
        if k % j == 0:
            prime_1 = False
            break
        elif j > sqrt:
            break
    for j in prime_numbers:
        if m % j == 0:
            prime_2 = False
            break
        elif j > sqrt:
            break
    if prime_2:
        prime_numbers.append(m)
        i = i + 1
    if prime_1:
        prime_numbers.append(k)
        i = i + 1
print(prime_numbers)



