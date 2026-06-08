import math
import matplotlib.pyplot as plt
from typing import List, Callable, Optional

def f(x: float) -> float:
    return x * math.sinh(x)

def g(x: float) -> float:
    return abs(5 * x + 3)

def second_derivative_f1(x: float) -> float:
    return x * math.sinh(x) + 2 * math.cosh(x)

def second_derivative_f2(x: float) -> float:
    return 0

def linspace(a: float, b: float, num: int) -> List[float]:
    """Возвращает список num равномерно распределённых значений от a до b."""
    if num == 1:
        return [a]
    step = (b - a) / (num - 1)
    return [a + i * step for i in range(num)]

def tridiagonal_solve(a: List[float], c: List[float], b: List[float], f: List[float]) -> List[float]:
    """Решает трёхдиагональную СЛАУ методом прогонки."""
    n: int = len(f)
    alpha: List[float] = [0] * n
    beta: List[float] = [0] * n

    alpha[0] = -b[0] / c[0]
    beta[0] = f[0] / c[0]

    for i in range(1, n):
        denom: float = c[i] + a[i] * alpha[i - 1]
        alpha[i] = -b[i] / denom
        beta[i] = (f[i] - a[i] * beta[i - 1]) / denom

    x: List[float] = [0] * n
    x[-1] = beta[-1]
    for i in range(n - 2, -1, -1):
        x[i] = alpha[i] * x[i + 1] + beta[i]

    return x

def cubic_spline(x_vals: List[float], y_vals: List[float], d2_start: float, d2_end: float) -> List[float]:
    """Строит коэффициенты кубического сплайна."""
    n: int = len(x_vals) - 1
    h: List[float] = [x_vals[i + 1] - x_vals[i] for i in range(n)]

    a: List[float] = [0] * (n - 1)
    c: List[float] = [0] * (n - 1)
    b: List[float] = [0] * (n - 1)
    f: List[float] = [0] * (n - 1)

    # коэффициенты, умноженные на 6
    for i in range(n - 1):
        a[i] = h[i]
        c[i] = 2 * (h[i] + h[i + 1])
        b[i] = h[i + 1]
        f[i] = 6 * ((y_vals[i + 2] - y_vals[i + 1]) / h[i + 1] - (y_vals[i + 1] - y_vals[i]) / h[i])

    # отнимаем значения M0 и Mn
    f[0] -= a[0] * d2_start
    f[-1] -= b[-1] * d2_end

    d2_vals: List[float] = [0] * (n + 1)
    d2_vals[1:-1] = tridiagonal_solve(a, c, b, f)
    d2_vals[0] = d2_start
    d2_vals[-1] = d2_end

    return d2_vals

def spline_evaluate(x_vals: List[float], y_vals: List[float], d2_vals: List[float], x: float) -> Optional[float]:
    """Вычисляет значение сплайна в точке x."""
    n: int = len(x_vals) - 1
    for i in range(n):
        if x_vals[i] <= x <= x_vals[i + 1]:
            h: float = x_vals[i + 1] - x_vals[i]
            A: float = (x_vals[i + 1] - x) / h
            B: float = (x - x_vals[i]) / h
            C: float = (A**3 - A) * h**2 / 6
            D: float = (B**3 - B) * h**2 / 6
            return A * y_vals[i] + B * y_vals[i + 1] + C * d2_vals[i] + D * d2_vals[i + 1]
    return None

def plot_spline(f: Callable[[float], float], d2_f: Callable[[float], float], title: str, fidx: Callable[[int], int], color1: str, color2: str) -> None:
    """Строит графики интерполяции с помощью кубического сплайна."""
    for idx, n in enumerate(degrees):
        x_nodes: List[float] = linspace(-2, 2, n + 1)
        y_nodes: List[float] = [f(x) for x in x_nodes]

        d2_vals: List[float] = cubic_spline(x_nodes, y_nodes, d2_f(x_nodes[0]), d2_f(x_nodes[-1]))

        y_spline: List[float] = [spline_evaluate(x_nodes, y_nodes, d2_vals, x) for x in x_dense]

        axs[fidx(idx)].plot(x_dense, [f(x) for x in x_dense], label="Оригинальная функция", color=color1)
        axs[fidx(idx)].plot(x_dense, y_spline, label="Кубический сплайн", color=color2, linestyle="--")
        axs[fidx(idx)].scatter(x_nodes, y_nodes, color="black", zorder=3)
        axs[fidx(idx)].set_title(f"{title}, n = {n}")
        axs[fidx(idx)].legend()
        axs[fidx(idx)].grid(True)

degrees: List[int] = [2, 4, 8, 16]
x_dense: List[float] = linspace(-2, 2, 400)

fig, axs = plt.subplots(2, 4, figsize=(16, 10))
axs = axs.flatten()

plot_spline(f, second_derivative_f1, "f(x) = xshx", lambda x: 2 * x, "blue", "red")
plot_spline(g, second_derivative_f2, "g(x) = |5x+3|", lambda x: 2 * x + 1, "green", "purple")

plt.tight_layout()
plt.show()
