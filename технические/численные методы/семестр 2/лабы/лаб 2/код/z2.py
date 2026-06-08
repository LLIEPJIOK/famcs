import math

def f(x):
    return math.exp(x)

def gauss_chebyshev_naST(n):
    """КФ НАСТ (Гаусс-Чебышёв) с весом 1/sqrt(1 - x^2)"""
    total = 0
    for k in range(0, n):
        x_k = math.cos((2*k + 1) * math.pi / (2 * n))
        total += f(x_k)
    return (math.pi / n) * total

def composite_rectangle(a, b, n):
    """Вычисление интеграла методом средних прямоугольников с n узлами"""
    h = (b - a) / (n - 1)
    s = 0
    for i in range(n-1):
        x = a + (i + 0.5)*h
        s += f(x) / math.sqrt(1 - x**2)
    return s * h

exact = 3.97746
print(f"Аналитическое значение интеграла: {exact:.10f}\n")

print(f"{'n':>3} | {'НАСТ':>14} | {'Прямоуг.':>14} | {'Погрешн. НАСТ':>14} | {'Погрешн. Прям.':>14}")
print("-"*70)
for n in [2, 4, 8, 16, 32, 64]:
	nast_val = gauss_chebyshev_naST(n)
	rect_val = composite_rectangle(-1, 1, n)
	err_nast = abs(nast_val - exact)
	err_rect = abs(rect_val - exact)
	print(f"{n:>3} | {nast_val:>14.10f} | {rect_val:>14.10f} | {err_nast:>14.2e} | {err_rect:>14.2e}")
