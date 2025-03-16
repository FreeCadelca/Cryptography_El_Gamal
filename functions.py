import random
from IntM import *


def is_prime(n: int):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def ferma_prime_test(n, k=12):
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
        if phi % i == 0:
            prime_divisors.add(i)
            prime_divisors.add(phi // i)
        i += 1
    g = 2
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
    # print(f'p: {p}')
    g = find_g(p)
    x = random.randint(2, p - 2)
    h = mod_pow(g, x, p)
    return {'public': (h, g, p), 'private': x}


def encrypt(m: int, pub_key: tuple[int, int, int], k=-1) -> tuple[int, int]:
    y, g, p = pub_key
    if k == -1:
        k = random.randint(2, p - 2)
    a = mod_pow(g, k, p)
    b = (m * mod_pow(y, k, p)) % p
    return a, b


def decrypt(priv_key: int, pub_key: tuple[int, int, int], ciphertext: tuple[int, int]) -> int:
    y, g, p = pub_key
    x = priv_key
    a, b = ciphertext
    return b * IntM(mod_pow(a, x, p), p).inv().value % p


def tuple_cipher_to_str(c: tuple[int, int]) -> str:
    return str(c[0]).zfill(17) + str(c[1]).zfill(17)


def str_to_tuple_cipher(s: str) -> tuple[int, int]:
    return int(s[:17]), int(s[17:])


def encrypt_line(s: str, pub_key: tuple[int, int, int], k=-1) -> str:
    message = [ord(i) for i in s]
    return "".join([tuple_cipher_to_str(encrypt(i, pub_key)).zfill(17) for i in message])


def decrypt_line(priv_key: int, pub_key: tuple[int, int, int], text: str) -> str:
    ciphertext = [str_to_tuple_cipher(text[i:i + 34]) for i in range(0, len(text), 34)]
    return "".join([chr(decrypt(priv_key, pub_key, ciphertext[i])) for i in range(len(ciphertext))])


if __name__ == "__main__":
    text = input("Введите текст:\n")
    mode = int(input("Введите режим работы - зашифрование/расшифрование/зашифрование числа/расшифрование числа [0/1/2/3]:\n"))
    if mode == 0:
        keys = key_gen()
        print(f"Ключи: (private: {keys["private"]}, public: {keys["public"]})")
        message = [ord(i) for i in text]
        ciphertext = "".join([tuple_cipher_to_str(encrypt(i, keys["public"])).zfill(17) for i in message])
        print("ciphertext:", ciphertext)
    elif mode == 1:
        key_private = int(input("Введите приватный ключ:\n"))
        key_public = tuple(map(int, input("Введите публичный ключ (h, g, p через пробел):\n").split()))
        ciphertext = [str_to_tuple_cipher(text[i:i + 34]) for i in range(0, len(text), 34)]
        plaintext = "".join([chr(decrypt(key_private, key_public, ciphertext[i])) for i in range(len(ciphertext))])
        print(plaintext)
    elif mode == 2:
        # keys = key_gen()
        keys = {'public': (2, 2, 7), 'private': 4}
        print(f"Ключи: (private: {keys["private"]}, public: {keys["public"]})")
        message = int(text)
        ciphertext = tuple_cipher_to_str(encrypt(message, keys["public"], k=3)).zfill(17)
        print("ciphertext:", ciphertext)
    elif mode == 3:
        key_private = int(input("Введите приватный ключ:\n"))
        key_public = tuple(map(int, input("Введите публичный ключ (h, g, p через пробел):\n").split()))
        ciphertext = str_to_tuple_cipher(text)
        plaintext = decrypt(key_private, key_public, ciphertext)
        print(plaintext)
