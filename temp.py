import re
from collections import defaultdict
from math import isqrt, gcd, sqrt, log, exp, prod
import random
from xml.sax.handler import feature_validation


def issquare(n):
    return isqrt(n) ** 2 == n


# def factor(n):
#     res = defaultdict(lambda: 0)
#     while True:
#         p = get_prime_divisor(n)

#         res[p] += 1
#         if p == n:
#             return res
#         n //= p
    
# def get_prime_divisor(N):
#     if N%2==0:
#             return 2
#     x = random.randint(1, N-1)
#     y = x
#     c = random.randint(1, N-1)
#     g = 1
#     while g==1:             
#             x = ((x*x)%N+c)%N
#             y = ((y*y)%N+c)%N
#             y = ((y*y)%N+c)%N
#             g = gcd(abs(x-y),N)
#     return g

def factor(n):
    Ans = defaultdict(lambda: 0)
    d = 2
    while d * d <= n:
        if n % d == 0:
            Ans[d] += 1
            n //= d
        else:
            d += 1
    if n > 1:
        Ans[n] += 1
    
    return Ans


def issquarefree(n):
    for e in factor(n).values():
        if e >= 2:
            return False

    return True


def next_multiplier(n, k):
    k += 2

    while (not issquarefree(k) or gcd(k, n) != 1):
        k += 1

    return k


def gaussian_elimination(A, n):
    m = len(A)
    I = [1 << k for k in range(m + 1)]
    nrow = 0

    for col in range(1, min(m, n) + 1):
        npivot = 0

        for row in range(nrow + 1, m + 1):
            if ((A[row - 1] >> (col-1)) & 1) == 1:
                npivot = row
                nrow += 1
                break

        if npivot == 0:
            continue

        if npivot != nrow:
            A[npivot - 1], A[nrow - 1] = A[nrow - 1], A[npivot - 1]
            I[npivot - 1], A[nrow - 1] = I[nrow - 1], I[npivot - 1]

        for row in range(nrow+1, m + 1):
            if ((A[row - 1] >> (col-1)) & 1) == 1:
                A[row - 1] = A[row - 1] ^ A[nrow - 1]
                I[row - 1] = I[row - 1] ^ I[nrow - 1]

    return I


def is_prime(n, k=10):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    s = 0
    d = n-1
    while d % 2 == 0:
        s += 1
        d //= 2

    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        if x != 1:
            for r in range(s):
                if x == n - 1:
                    break
                x = (x ** 2) % n
            if x != n - 1:
                return False

    return True


def check_factor(n, g, factors):

    while n % g == 0:

        n //= g
        factors.append(g)

        if is_prime(n):
            factors.append(n)
            return 1

    return n


def is_smooth_over_prod(n, k):

    g = gcd(n, k)

    while g > 1:
        n //= g
        while n % g == 0:
            n //= g

        if n == 1:
            return True
        g = gcd(n, g)

    return n == 1


def jacobi(a, n):
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a >>= 1
            if ((n % 8) in [3, 5]):
                result *= -1

        a, n = n, a
        if (a % 4 == n % 4 == 3):
            result *= -1
        a %= n

    return result if n == 1 else 0


def cffm(n, multiplier=1):
    if n <= 1:
        return []
    if is_prime(n):
        return [n]

    if n % 2 == 0:
        v = 0
        while n % 2 == 0:
            v += 1
            n >>= 1

        arr1 = [2] * v
        arr2 = cffm(n)

        return arr1 + arr2

    if issquare(n):
        f = cffm(isqrt(n))
        return sorted(f + f)

    N = n*multiplier

    x = isqrt(N)
    y = x
    z = 1
    w = x+x
    r = w

    B = round(exp(sqrt(log(n) * log(log(n))) / 2))
    factor_base = []

    for p in range(B):
        if is_prime(p) and jacobi(N, p) >= 0:
            factor_base.append(p)

    factor_prod = prod(factor_base)
    factor_index = {}  # Dict{Int64, Int64}()

    for k in range(1, len(factor_base) + 1):
        factor_index[factor_base[k - 1]] = k - 1

    def exponent_signature(factors):
        sig = 0

        for p, e in factors.items():
            if e % 2 == 1:
                sig |= (1 << factor_index[p])

        return sig

    L = len(factor_base) + 1

    Q = []
    A = []

    (f1, f2) = (1, x)

    while len(A) < L:

        y = (r*z - y)
        z = (N - y*y) // z
        r = (x + y) // z

        (f1, f2) = (f2, (r*f2 + f1) % n)

        if issquare(z):
            g = gcd(f1 - isqrt(z), n)

            if g > 1 and g < n:
                arr1 = cffm(g)
                arr2 = cffm(n // g)
                return sorted(arr1 + arr2)

        if z > 1 and is_smooth_over_prod(z, factor_prod):
            A.append(exponent_signature(factor(z)))
            Q.append([f1, z])

        if z == 1:
            return cffm(n, next_multiplier(n, multiplier))

    while len(A) < L:
        A.append(0)

    I = gaussian_elimination(A, len(A))

    LR = 0
    # !
    for k in range(len(A) - 1, 0, -1):
        if A[k] != 0:
            LR = k + 1
            break

    remainder = n
    factors = []

    def cfrac_find_factors(solution, remainder):

        X = 1
        Y = 1

        for i in range(len(Q)):
            if ((solution >> i) & 1) == 1:
                X *= Q[i][0]
                Y *= Q[i][1]

                g = gcd(X - isqrt(Y), remainder)

                if (g > 1 and g < remainder):
                    remainder = check_factor(remainder, g, factors)

                    if remainder == 1:
                        return True, remainder

        return False, remainder

    for k in range(LR - 1, len(I)):
        flag, remainder = cfrac_find_factors(I[k], remainder)
        if flag:
            break

    final_factors = []

    for f in factors:
        if is_prime(f):
            final_factors.append(f)
        else:
            final_factors += cffm(f)

    if remainder != 1:
        if remainder != n:
            final_factors += cffm(remainder)
        else:
            final_factors.append(remainder)

    # Failed to factorize n (try again with a multiplier)
    if remainder == n:
        return cffm(n, next_multiplier(n, multiplier))

    # Return all prime factors of n
    return sorted(final_factors)


file = open("./nums.txt").read()
nums = [int(i) for i in re.findall(r'\b\d+\b', file)]


print(cffm(2 ** 128 + 1))
# print(cffm(2 ** (2 ** 7) + 1))

for i in range(000):
    p = random.choice(nums)
    q = random.choice(nums)

    n = p * q
    res = cffm(n)
    if p in res:
        pass
    else:
        print("Ебаный рот блять")
