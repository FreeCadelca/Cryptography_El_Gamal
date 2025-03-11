import datetime


def mod_pow(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2  # Делим степень на 2
    return result


start = datetime.datetime.now()
print('Время старта: ' + str(start))

print(mod_pow(7, 13112482473320009392758023859082351241249820090394092424332567359254322424, 37481041))

# фиксируем и выводим время окончания работы кода
finish = datetime.datetime.now()
print('Время окончания: ' + str(finish))

# вычитаем время старта из времени окончания
print('Время работы: ' + str(finish - start))

