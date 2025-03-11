# Extended algorythm of Euclid
def ext_euclid(a: int, b: int) -> tuple:
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b > 0:
        q, r = a // b, a % b
        x, y = x2 - q * x1, y2 - q * y1

        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    return a, x2, y2


class IntM:
    def __init__(self, v: int, m: int):
        self.modulus = m
        self.value = v % m

    def __int__(self):
        return self.value

    def __add__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value + other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value + other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __sub__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value - other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value - other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __mul__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return IntM((self.value * other.value) % self.modulus, self.modulus)
        elif isinstance(other, int):
            return IntM((self.value * other) % self.modulus, self.modulus)
        else:
            raise ValueError

    def __floordiv__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError
            return self.__mul__(other.inv())
        elif isinstance(other, int):
            return self.__mul__(IntM(other, self.modulus).inv())
        else:
            raise ValueError

    def __pow__(self, power: int, modulo=None):
        v = 1
        for i in range(power):
            v *= self.value
            v %= self.modulus
        return IntM(v, self.modulus)

    def inv(self):
        d, x, y = ext_euclid(self.modulus, self.value)
        if d == 1:
            return IntM(y, self.modulus)
        raise ValueError("При вычислении inv получился НОД != 1")

    def __gt__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            raise ValueError

    def __lt__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            raise ValueError

    def __ge__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        else:
            raise ValueError

    def __le__(self, other):
        if isinstance(other, IntM):
            if self.modulus != other.modulus:
                raise ValueError("The modules must match.")
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        else:
            raise ValueError

    def __eq__(self, other):
        if isinstance(other, IntM):
            return self.modulus == other.modulus and self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            raise ValueError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f'{self.value}m{self.modulus}'
