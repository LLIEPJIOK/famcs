import math

import matplotlib.pyplot as plt


def plot(values, title, bins=100):
    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')

    plt.title(title)
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.grid(True, alpha=0.3)

    plt.axhline(y=len(values) / bins, color='red', linestyle='--', alpha=0.7,
                label='Приблизительное равномерное распределение')
    plt.legend()

    plt.show()


def kolmogorov_func(x, eps=1e-3):
    sum = 0
    i = 1

    while True:
        s = (-1) ** (i - 1) * math.exp(-2 * i ** 2 * x ** 2)
        sum += s

        if abs(s) < eps:
            break

        i += 1

    return 1 - 2 * sum


def kolmogorov_inv(x, eps=1e-3):
    l, r = 0, 2 ** 8

    while kolmogorov_func(r) < x:
        r *= 2

    while r - l > eps:
        mid = (l + r) / 2
        f = kolmogorov_func(mid)
        if f < x:
            l = mid
        else:
            r = mid

    return (l + r) / 2


def kolmogorov(values, eps):
    values.sort()

    n = len(values)
    d = 0

    for i in range(n):
        d = max(d, abs(i / n - values[i]))
        d = max(d, abs((i + 1) / n - values[i]))

    delta = kolmogorov_inv(1 - eps)

    return math.sqrt(n) * d < delta


def chi_square_func(histogram, pk, n):
    if len(histogram) != len(pk):
        raise ValueError('Different histogram and pk lengths')

    chi_square = 0

    for i in range(len(histogram)):
        cur = pow(histogram[i] - n * pk[i], 2) / (n * pk[i])
        chi_square += cur

    return chi_square


def pearson(values, k):
    n = len(values)
    p = 1 / k

    histogram = [0] * k
    pk = [p] * k

    for v in values:
        histogram[int(v / p)] += 1

    chi_square = chi_square_func(histogram, pk, n)
    delta = 44.99  # табличное значение для e=0.05

    return chi_square < delta


def mk_generator(params):
    (a, b, m) = params

    def gen():
        nonlocal a

        a = (b * a) % m

        return a / m

    return gen


def lc_generator(params):
    (a, b, c, m) = params

    def gen():
        nonlocal a

        a = (a * b + c) % m

        return a / m

    return gen


def mm_generator(first_params, second_params, k):
    first_gen = mk_generator(first_params)
    second_gen = lc_generator(second_params)

    v = [first_gen() for _ in range(k)]

    def gen():
        nonlocal v

        s = int(second_gen() * k)
        a = v[s]
        v[s] = first_gen()

        return a

    return gen


def mk_method(params, eps, k, n=1000):
    gen = mk_generator(params)
    values = [gen() for _ in range(n)]
    plot(values, "Мультипликативный конгруэнтный метод", k)

    satisfiability = kolmogorov(values, eps)
    print(f"Проверка Колмогорова для МКМ: {satisfiability}")
    satisfiability = pearson(values, k)
    print(f"Проверка Пирсона для МКМ: {satisfiability}")


def mm_method(first_params, second_params, k, eps, n=1000):
    gen = mm_generator(first_params, second_params, k)
    values = [gen() for _ in range(n)]
    plot(values, "Метод Макларена-Марсальи", k)

    satisfiability = kolmogorov(values, eps)
    print(f"Проверка Колмогорова для Макларена-Марсальи: {satisfiability}")
    satisfiability = pearson(values, k)
    print(f"Проверка Пирсона для Макларена-Марсальи: {satisfiability}")


if __name__ == '__main__':
    first_params = (24389, 24389, 2 ** 31)
    second_params = (214013, 214013, 2531011, 2 ** 24)
    k = 32
    eps = 0.05

    mk_method(first_params, eps, k)
    mm_method(first_params, second_params, k, eps)
