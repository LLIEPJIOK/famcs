import math

def f(x):
    return math.cos(x)**2

def composite_simpson(f, a, b, n):
    """Вычисление интеграла по составной формуле Симпсона с n отрезками (n должно быть чётным)"""
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i*h
        if i % 2 == 0:
            s += 2 * f(x)
        else:
            s += 4 * f(x)
    return s * h / 3

def composite_rectangle(f, a, b, n):
    """Вычисление интеграла методом средних прямоугольников с n разбиениями"""
    h = (b - a) / n
    s = 0
    for i in range(n):
        x = a + (i + 0.5)*h
        s += f(x)
    return s * h

def runge_rule(I_h, I_h2, p):
    """
    Оценка погрешности по правилу Рунге:
    |I(h/2) - I(h)| / (2^p - 1)
    """
    return abs(I_h2 - I_h) / (2**p - 1)

def adaptive_integration(method, f, a, b, eps, p, initial_n=4):
    """
    Адаптивное вычисление интеграла с заданной точностью eps.
    method: функция для вычисления интеграла (composite_simpson или composite_rectangle)
    p: порядок метода (для Симпсона p=4, для прямоугольников p=2)
    """
    n = initial_n
    I_h = method(f, a, b, n)
    n *= 2
    I_h2 = method(f, a, b, n)
    
    error = runge_rule(I_h, I_h2, p)
    while error > eps:
        I_h = I_h2
        n *= 2
        I_h2 = method(f, a, b, n)
        error = runge_rule(I_h, I_h2, p)
    return I_h2, n, error

a = 0
b = math.pi
eps = 1e-6
exact = math.pi / 2  # Аналитически: ∫ cos²x dx = (π/2)

# Симпсон
simpson_value, n_simpson, error_simpson = adaptive_integration(composite_simpson, f, a, b, eps, p=4, initial_n=4)
h_simpson = (b - a) / n_simpson
# Прямоугольники (метод средних прямоугольников)
rectangle_value, n_rectangle, error_rectangle = adaptive_integration(composite_rectangle, f, a, b, eps, p=2, initial_n=4)
h_rectangle = (b - a) / n_rectangle

print("Метод Симпсона:")
print(f"  Приближённое значение интеграла: {simpson_value:.8f}")
print(f"  Шаг h: {h_simpson:.8f} (n = {n_simpson})")
print(f"  Оценка погрешности по Рунге: {error_simpson:.2e}")
print(f"  Точное значение: {exact:.8f}")
print(f"  Абсолютная погрешность: {abs(simpson_value - exact):.2e}")
print()
print("Метод прямоугольников (средних):")
print(f"  Приближённое значение интеграла: {rectangle_value:.8f}")
print(f"  Шаг h: {h_rectangle:.8f} (n = {n_rectangle})")
print(f"  Оценка погрешности по Рунге: {error_rectangle:.2e}")
print(f"  Точное значение: {exact:.8f}")
print(f"  Абсолютная погрешность: {abs(rectangle_value - exact):.2e}")
