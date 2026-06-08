import math
import matplotlib.pyplot as plt

def f(x, u):
    return (u**2 + 2) * math.exp(-u) + 1

def df(x, u):
    # производная (u^2+2)e^{-u} + 1
    return math.exp(-u) * (2*u - u*u - 2)

a = [
    [0,   0,   0,   0], 
    [0.5, 0,   0,   0], 
    [0,   0.5, 0,   0], 
    [0,   0,   1,   0],
]
b = [1/6, 1/3, 1/3, 1/6]
c = [0, 0.5, 0.5, 1]

def rk4_step(x, y, h):
    k = []
    for j in range(4):
        k.append(f(x + c[j] * h, y + h * sum(a[j][l] * k[l] for l in range(j))))

    return y + h * sum(b[j] * k[j] for j in range(4))

def rk4(u0, x0, x_end, eps, h_initial=0.1):
    xs = [x0]
    us = [u0]
    x, u = x0, u0
    h = h_initial
    
    while x < x_end:
        if x + h > x_end:
            h = x_end - x

        # шаг h
        u1 = rk4_step(x, u, h)
        # два шага h/2
        u_half = rk4_step(x, u, h/2)
        u2 = rk4_step(x + h/2, u_half, h/2)

        err = abs(u2 - u1)
        if err > eps:
            h = h / 2
            xs = xs[:1]
            us = us[:1]
            x, u = x0, u0
            continue
            
        xs.append(x + h)
        us.append(u1)
        x += h
        u = u1

    return xs, us

def newton_step(xj, yj, h, eps=1e-3):
    """
    Решение g(y)=0 методом Ньютона для получения y_{j+1}.
    g(y) = y - yj - h/2*(f(yj) + f(y))
    """
    y = yj + h * f(xj, yj)
    while True:
        g  = y - yj - 0.5*h*(f(xj, yj) + f(xj + h, y))
        dg = 1.0 - 0.5*h * df(xj + h, y)
        dy = - g / dg
        y += dy
        if abs(dy) < eps:
            break
    return y

def adams(u0, x0, x_end, eps, h_initial=0.1):
    xs = [x0]
    us = [u0]
    x, u = x0, u0
    h = h_initial

    while x < x_end:
        if x + h > x_end:
            h = x_end - x

        u1 = newton_step(x, u, h, eps)
        u_half = newton_step(x, u, h/2, eps)
        u2 = newton_step(x + h/2, u_half, h/2, eps)
        err = abs(u2 - u1)
        if err > eps:
            h = h / 2
            xs = xs[:1]
            us = us[:1]
            x, u = x0, u0
            continue

        xs.append(x + h)
        us.append(u1)
        x += h
        u = u1

    return xs, us

def linear_interpolate(xs, ys, xq):
    if xq <= xs[0]:
        return ys[0]
    if xq >= xs[-1]:
        return ys[-1]
    for i in range(len(xs)-1):
        x0, x1 = xs[i], xs[i+1]
        if x0 <= xq <= x1:
            y0, y1 = ys[i], ys[i+1]
            t = (xq - x0)/(x1 - x0)
            return y0 + t*(y1 - y0)

if __name__ == "__main__":
    x0, u0 = 0.0, 0.0
    x_end = 1.5
    eps = 1e-3

    xs1, us1 = rk4(u0, x0, x_end, eps)
    xs2, us2 = adams(u0, x0, x_end, eps)

    plt.figure(figsize=(8,5))
    plt.plot(xs1, us1, '.-', label="Рунге-Кутта")
    plt.plot(xs2, us2, '--', label="Адамса")
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.title("Решения задачи Коши u'=(u^2+2)e^{-u}+1 (ε=1e-3)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


    delta = [abs(u1 - linear_interpolate(xs2, us2, x)) for x, u1 in zip(xs1, us1)]

    plt.figure(figsize=(8,5))
    plt.plot(xs1, delta, '.-', label="Разность решений")
    plt.xlabel("x")
    plt.ylabel("Δ(x)")
    plt.title("Модуль разности решений")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
