from gmpy2 import invert, gcd, is_strong_prp, ceil, log2
from os import urandom
from random import SystemRandom
from typing import Tuple
from .keyinfo import KeyInfo

# M is the product of all odd primes which fits in 32 bits.
# It's used as a quick check for finding primes.
M = 3*5*7*11*13*17*19*23*29
# Use SystemRandom for finding bases for Miller-Rabin.
# random.SystemRandom uses os.urandom.
_sys_rand = SystemRandom()


def random_odd(bits: int) -> int:
    """Returns a random odd number with the specified amount of bits."""
    assert (bits % 8) == 0
    mask = 1 << (bits - 1) | 1
    return int.from_bytes(urandom(bits // 8), 'big') | mask


def miller_rabin(n: int, iterations: int) -> bool:
    """Does Miller-Rabin checks on n with random bases."""
    for i in range(iterations):
        base = _sys_rand.randrange(n)
        # gmpy2.is_strong_prp is the Miller-Rabin test
        if not is_strong_prp(n, base):
            return False
    return True


def find_prime(bits: int) -> int:
    """Returns a prime number with the specified amount of bits."""
    p = random_odd(bits)
    while True:
        # if p is not coprime with M then it isn't prime.
        if gcd(p, M) != 1:
            p += 2
            continue
        if miller_rabin(p, 10):
            return p
        else:
            p += 2


def check_pair(p: int, q: int) -> Tuple[int, int]:
    """Returns the encryption modulus and totient for the given primes."""
    n = p*q
    k = ceil(log2(n))
    if abs(p - q) > 2**(k/2 - 100):
        return n, n - (p + q - 1)
    return 0, 0


def generate_key(bits: int, public_exponent: int = 3) -> KeyInfo:
    """Finds parameters appropriate for RSA encryption."""
    primes = []
    while True:
        q = find_prime(bits//2)
        for p in primes:
            modulus, totient = check_pair(p, q)
            if modulus == 0:
                continue
            if gcd(public_exponent, totient) != 1:
                continue
            private_exponent = invert(public_exponent, totient)
            return KeyInfo(modulus,
                           public_exponent,
                           private_exponent,
                           p, q)
        primes.append(q)
