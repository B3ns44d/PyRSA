import sympy
import random
import math


def mod_inverse(x, y):

    def eea(a, b):
        if b == 0:
            return (1, 0)
        (q, r) = (a//b, a % b)
        (s, t) = eea(b, r)
        return (t, s-(q*t))

    inv = eea(x, y)[0]
    if inv < 1:
        inv += y  # we only want positive values
    return inv


p = sympy.randprime(2**256, 2**512)
q = sympy.randprime(2**256, 2**512)
while p == q:
    q = sympy.randprime(2**256, 2**512)
N = p*q
phi = (p-1)*(q-1)
e = random.randint(1, phi)
while math.gcd(e, phi) != 1:
    e = random.randint(1, phi)
d = mod_inverse(e, phi)
print("N :", N, "\n\n", "e :", e, "\n\n", "d :", d)

M0 = 77940
M1 = 19031998
print("\nMessages :", M0, M1)

C0 = pow(M0, e, N)
C1 = pow(M1, e, N)
print("\nEncrypted messages:", C0, C1)

M2 = pow(C0, d, N)
M3 = pow(C1, d, N)
print("\nDecrypted messages:", M2, M3)
