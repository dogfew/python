import re
from math import factorial


def expand(expr):
    x = re.findall(r'[a-z]', expr)[0]
    *a, b, n = map(int, re.findall(r'[^a-z()^]+', expr.replace(f"-{x}", f"-1{x}")))
    a = 1 if a == [] else a[0]
    result = ""
    for k in range(n + 1):
        f = int(factorial(n) / (factorial(k) * (factorial(n - k))))
        coeff = f * (b ** k) * (a ** (n - k))
        result += f"{coeff if coeff != 1 or n - k == 0 else ''}{x}^{n-k}+"
    return result[:-1].replace(f"{x}^0", "").replace(f"-1{x}", f"-{x}").replace("+-", "-").replace(f"{x}^1", x)
