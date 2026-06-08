import numpy as np
from scipy.integrate import quad

# Определение многочленов Лежандра
def P0(t): return 1
def P1(t): return t
def P2(t): return 0.5 * (3 * t**2 - 1)
def P3(t): return 0.5 * (5 * t**3 - 3 * t)

# Список многочленов
legendre_polynomials = [P0, P1, P2, P3]

# Исходная функция
def x(t):
    return t**2 + abs(t)

# Вычисление коэффициентов c_n
def compute_coefficients():
    coefficients = []
    for n, Pn in enumerate(legendre_polynomials):
        integrand = lambda t: x(t) * Pn(t)
        cn, _ = quad(integrand, -1, 1)  # Численный интеграл
        cn *= (2 * n + 1) / 2
        coefficients.append(cn)
    return coefficients


# Построение приближения
def approximate_function(t, coefficients):
    approximation = sum(cn * Pn(t) for cn, Pn in zip(coefficients, legendre_polynomials))
    return approximation

# Оценка ошибки
def error_norm(coefficients):
    integrand = lambda t: (x(t) - approximate_function(t, coefficients))**2
    error, _ = quad(integrand, -1, 1)
    return np.sqrt(error)

# Основной расчет
coefficients = compute_coefficients()
print("Коэффициенты c_n:", coefficients)

# Оценка точности
error = error_norm(coefficients)
print("Норма ошибки:", error)

# Вывод результата
t_values = np.linspace(-1, 1, 100)
approximation = [approximate_function(t, coefficients) for t in t_values]

import matplotlib.pyplot as plt
plt.plot(t_values, [x(t) for t in t_values], label="Исходная функция")
plt.plot(t_values, approximation, label="Приближение")
plt.legend()
plt.show()
