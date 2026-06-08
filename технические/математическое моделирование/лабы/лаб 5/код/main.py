import math
import random
import matplotlib.pyplot as plt
from scipy.integrate import dblquad

def g(x, y):
    return math.atan(x + y)

def int_gen(fb, lb):
    fbd, fbu = fb
    lbd, lbu = lb

    def gen():
        nonlocal fbd, fbu, lbd, lbu

        x = random.uniform(fbd, fbu)
        y = random.uniform(lbd, lbu)

        return g(x, y)

    return gen

def area(fb, sd):
    fbd, fbu = fb
    lbd, lbu = sd

    return (fbu - fbd) * (lbu - lbd)

def monte_carlo(fb, sd, n=100_000):
    gen = int_gen(fb, sd)
    values = [gen() for _ in range(n)]

    return area(fb, sd) * sum(values) / n

if __name__ == "__main__":
    fb = (math.exp(1), math.pi)
    sd = (math.exp(3), math.pi**3)

    exact, error = dblquad(
        lambda y, x: g(x, y), 
        fb[0], fb[1],
        lambda x: sd[0], lambda x: sd[1]
    )
    print(f"Точный результат: {exact:.8f} (ошибка={error:.2e})\n")

    ns = [100, 500, 1000, 5000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    results = []
    errors = []

    for n in ns:
        approx = monte_carlo(fb, sd, n)
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
