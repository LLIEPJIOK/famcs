import numpy as np
from scipy.integrate import quad

# Исходная функция
def x(t):
    return t**2 + t

# Вычисление коэффициентов
def compute_coefficients(N, a, b):
    for n in range(len(a) + 1, N + 1):
        an, _ = quad(lambda t: x(t / np.pi) * np.cos(n * t), -np.pi, np.pi, limit=1000) 
        an /= np.pi
        bn, _ = quad(lambda t: x(t / np.pi) * np.sin(n * t), -np.pi, np.pi, limit=1000) 
        bn /= np.pi
        a.append(an)
        b.append(bn)

# Построение приближения
def approximate_function(t, a0, a, b):
    global f
    approximation = a0
    for n, (an, bn) in enumerate(zip(a, b), start=1):
        approximation += an * np.cos(n * t) + bn * np.sin(n * t)
    return approximation

# Оценка ошибки
def error_norm(a0, a, b):
    integrand = lambda t: (x(t / np.pi) - approximate_function(t, a0, a, b))**2
    error, _ = quad(integrand, -np.pi, np.pi, limit=1000)
    return np.sqrt(error)

# Основной расчет
epsilon = 1e-3
max_n = 100
N = 1  # Начальная степень многочлена
a0, _ = quad(lambda t: x(t / np.pi), -np.pi, np.pi, limit=1000)
a0 /= np.pi  # Коэффициент a0
a0 /= 2  # Учет деления на 2
while True:
    a = []
    b = []
    compute_coefficients(N, a, b)
    error = error_norm(a0, a, b)
    if error < epsilon or N >= max_n:
        break
    N += 1

print(f"Приближение достигнуто при N = {N}")
print("Коэффициенты:")
print(f"a0 = {a0}")
print(f"a = {a}")
print(f"b = {b}")

# Графическое представление
import matplotlib.pyplot as plt

t_values = np.linspace(-np.pi, np.pi, 500)
original = [x(t / np.pi) for t in t_values]
approximation = [approximate_function(t, a0, a, b) for t in t_values]

plt.plot(t_values, original, label="Исходная функция")
plt.plot(t_values, approximation, label="Приближение")
plt.legend()
plt.show()
