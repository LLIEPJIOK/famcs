import math
import random
import matplotlib.pyplot as plt
from scipy.integrate import quad

def g(x):
    return math.exp(-x) / (x * math.sqrt(1 + x**3))

def p(x):
    return math.exp(-(x - 4))

def exp_gen(l, d):
    def gen():
        u = random.uniform(0, 1)

        return -1 / l * math.log(1 - u) + d

    return gen

def int_gen(l, d):
    egen = exp_gen(l, d)

    def gen():
        x = egen()

        return g(x) / p(x)

    return gen

def monte_carlo(n=100_000):
    gen = int_gen(1, 4)
    values = [gen() for _ in range(n)]

    return sum(values) / n

if __name__ == "__main__":
    l, r = 4, math.inf

    exact, error = quad(g, l, r)
    print(f"Точный результат: {exact:.8f} (ошибка={error:.2e})\n")

    ns = [100, 500, 1000, 5000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    results = []
    errors = []

    for n in ns:
        approx = monte_carlo(n)
        abs_err = abs(approx - exact)
        results.append(approx)
        errors.append(abs_err)
        print(f"n={n:>7} -> Монте-Карло: {approx:.8f}, ошибка={abs_err:.8e}")

    plt.figure(figsize=(8,5))
    plt.plot(ns, errors, marker='o')
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Зависимость точности метода Монте-Карло от числа итераций")
    plt.xlabel("Число итераций n")
    plt.ylabel("Абсолютная ошибка")
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.show()
