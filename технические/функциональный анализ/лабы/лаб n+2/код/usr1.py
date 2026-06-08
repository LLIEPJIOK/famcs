import numpy as np
import matplotlib.pyplot as plt

# Уравнение g(x)
def g(x):
    return 2 * x + x / (1 + x**2) - np.arctan(x) - 4

# Производная от phi(x)
def phi_prime(x):
    return (8*x+3 +2*x**2+2*np.arctan(x)*x) / (3+x*x**2)**2

# Выражение phi(x) (переписанное уравнение x = phi(x))
def phi(x):
    return (4 + np.arctan(x)) / (2 + 1 / (1 + x**2))

# Метод простых итераций
def simple_iterations(x0, epsilon, max_iterations=1000):
    x = x0
    iteration = 0
    for _ in range(max_iterations):
        iteration += 1
        x_next = phi(x)
        if abs(x_next - x) < epsilon:
            return x_next, iteration
        x = x_next
    raise ValueError("Метод не сошелся за максимальное количество итераций")

# Построение графика функции g(x)
x_values = np.linspace(-5, 5, 500)
g_values = [g(x) for x in x_values]

plt.plot(x_values, g_values, label="g(x)")
plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
plt.title("График функции g(x)")
plt.xlabel("x")
plt.ylabel("g(x)")
plt.grid(True)
plt.legend()
plt.show()

# Начальное приближение и интервал
x0 = 1.5  # Интервал определён из графика
epsilon = 1e-4

# Проверка условия сходимости
phi_prime_values = [phi_prime(x) for x in x_values]
q = max(abs(phi_prime(x)) for x in np.linspace(1, 2, 500))  # Максимум |phi'(x)| на интервале корня
print(f"Максимум |phi'(x)| = {q:.4f}")
if q >= 1:
    raise ValueError("Условие сходимости не выполнено. Попробуйте изменить phi(x).")

# Априорная оценка количества итераций
N_apriori = int(np.log(epsilon * (1 - q) / abs(phi(x0) - x0)) / np.log(q)) + 1
print(f"Априорная оценка количества итераций: {N_apriori}")

# Решение методом последовательных приближений
root, iteration = simple_iterations(x0, epsilon)
print(f"Корень: {root:.6f}, найден за {iteration} итераций")
