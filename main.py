import random
from IntM import *


# phi(p) = p - 1
# g: g ^ (p - 1) = 1 mod p
def is_prime(n: int):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def ferma_prime_test(n, k=12):
    """
    Тест Ферма для проверки простоты числа.
    n - число для проверки
    k - количество итераций теста (чем больше, тем точнее проверка)
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True


def mod_pow(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2  # Делим степень на 2
    return result


def find_g(p: int):
    phi = p - 1
    i = 2
    prime_divisors = set()
    while i * i <= phi:
        if i ** 2 == phi // 10:
            print("1/10!")
        if phi % i == 0:
            prime_divisors.add(i)
            prime_divisors.add(phi // i)
        i += 1
    g = 2
    print('all prime divisors!')
    while g * g <= phi:
        if all(mod_pow(g, phi // d, p) != 1 for d in prime_divisors):
            return g
        g += 1
    return None


def find_large_prime(number_of_bits: int):
    while True:
        candidate = random.getrandbits(number_of_bits) | 1  # Делаем число нечетным
        if ferma_prime_test(candidate) and candidate > 2 ** 32:
            return candidate


def key_gen() -> dict[str: tuple[int, int, int], str: int]:
    p = find_large_prime(54)
    print(f'p: {p}')
    g = find_g(p)
    x = random.randint(2, p - 2)
    y = mod_pow(g, x, p)
    return {'public': (y, g, p), 'private': x}


def encrypt(m: int, pub_key: tuple[int, int, int]) -> tuple[int, int]:
    y, g, p = pub_key
    k = random.randint(2, p - 2)
    a = mod_pow(g, k, p)
    b = (m * mod_pow(y, k, p)) % p
    return a, b


def decrypt(priv_key: int, pub_key: tuple[int, int, int], ciphertext: tuple[int, int]) -> int:
    y, g, p = pub_key
    x = priv_key
    a, b = ciphertext
    return b * IntM(mod_pow(a, x, p), p).inv().value % p


keys = key_gen()
# keys = {'public': (3, 2, 11), 'private': 8}
print(decrypt(keys["private"], keys["public"], encrypt(214, keys["public"])))
