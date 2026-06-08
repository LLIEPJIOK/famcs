import math
import matplotlib.pyplot as plt

def linspace(a: float, b: float, num: int) -> list[float]:
    """Возвращает список num равномерно распределённых значений от a до b."""
    if num == 1:
        return [a]
    step: float = (b - a) / (num - 1)
    return [a + i * step for i in range(num)]

def f(x: float) -> float:
    return x * math.sinh(x)

def g(x: float) -> float:
    return abs(5 * x + 3)

def divided_diff(x: list[float], y: list[float]) -> list[float]:
    """Вычисляет коэффициенты разделённых разностей."""
    n: int = len(x)
    coef: list[float] = [y[0]]
    temp: list[float] = y.copy()
    for j in range(1, n):
        for i in range(n - j):
            temp[i] = (temp[i + 1] - temp[i]) / (x[i + j] - x[i])
        coef.append(temp[0])
    return coef

def newton_poly(x_data: list[float], coef: list[float], x_vals: list[float]) -> list[float]:
    """Вычисляет значения интерполяционного многочлена Ньютона."""
    p_vals: list[float] = []
    n: int = len(coef)
    for x in x_vals:
        p: float = 0
        term: float = 1
        for i in range(n):
            p += coef[i] * term
            term *= (x - x_data[i])
        p_vals.append(p)
    return p_vals

def newton_poly_str(x_data: list[float], coef: list[float], degree: int) -> str:
    """Формирует строковое представление многочлена Ньютона."""
    terms: list[str] = []
    for i in range(degree + 1):
        term_str: str = f"({coef[i]:g})"
        for j in range(i):
            term_str += f"*(x {'+' if x_data[j] < 0 else '-'} {abs(x_data[j]):g})"
        terms.append(term_str)
    return " + ".join(terms)

# Список степеней многочленов
degrees: list[int] = [2, 4, 8, 16]

# Подготовка графиков: 2 строки x 4 столбца
fig, axs = plt.subplots(2, 4, figsize=(16, 10))
axs = axs.flatten()

# Плотная сетка для отображения функций
x_dense: list[float] = linspace(-2, 2, 400)

# Построение интерполяции
for idx, n in enumerate(degrees):
    num_nodes: int = n + 1
    x_nodes: list[float] = linspace(-2, 2, num_nodes)

    # Интерполяция для f(x)
    y_nodes_f: list[float] = [f(x) for x in x_nodes]
    coef_f: list[float] = divided_diff(x_nodes, y_nodes_f)
    p_values_f: list[float] = newton_poly(x_nodes, coef_f, x_dense)

    # Интерполяция для g(x)
    y_nodes_g: list[float] = [g(x) for x in x_nodes]
    coef_g: list[float] = divided_diff(x_nodes, y_nodes_g)
    p_values_g: list[float] = newton_poly(x_nodes, coef_g, x_dense)

    # График f(x)
    axs[2 * idx].plot(x_dense, [f(x) for x in x_dense], label="f(x) = xshx", color="blue")
    axs[2 * idx].plot(x_dense, p_values_f, label=f"Ньютон, deg={n}", color="red", linestyle="--")
    axs[2 * idx].scatter(x_nodes, y_nodes_f, color="black")
    axs[2 * idx].set_title(f"Интерполяция f(x), n = {n}")
    axs[2 * idx].legend()
    axs[2 * idx].grid(True)

    # График g(x)
    axs[2 * idx + 1].plot(x_dense, [g(x) for x in x_dense], label="g(x) = |5x+3|", color="green")
    axs[2 * idx + 1].plot(x_dense, p_values_g, label=f"Ньютон, deg={n}", color="purple", linestyle="--")
    axs[2 * idx + 1].scatter(x_nodes, y_nodes_g, color="black")
    axs[2 * idx + 1].set_title(f"Интерполяция g(x), n = {n}")
    axs[2 * idx + 1].legend()
    axs[2 * idx + 1].grid(True)

    if n == 2:
        poly_str_f = newton_poly_str(x_nodes, coef_f, degree=2)
        poly_str_g = newton_poly_str(x_nodes, coef_g, degree=2)
        print("Аналитическое представление многочлена Ньютона 2-й степени:")
        print(f"f(x): {poly_str_f}")
        print(f"g(x): {poly_str_g}")

plt.tight_layout()
plt.show()
