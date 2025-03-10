import random


# phi(p) = p - 1
# g: g ^ (p - 1) = 1 mod p
def is_prime(n: int):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def ferma_prime_test(n, k=100):
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


def mod_exp(base, exponent, mod):
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
        if phi % i == 0:
            prime_divisors.add(i)
            prime_divisors.add(phi // i)
        i += 1
    g = 2
    while g * g <= phi:
        if all(mod_exp(g, phi // d, p) != 1 for d in prime_divisors):
            return g
    return None


def find_large_prime(number_of_bits: int):
    while True:
        candidate = random.getrandbits(number_of_bits) | 1  # Делаем число нечетным
        if is_prime(candidate):
            return candidate
