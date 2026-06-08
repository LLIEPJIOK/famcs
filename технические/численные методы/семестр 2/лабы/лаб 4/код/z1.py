import numpy as np
import matplotlib.pyplot as plt

def fdm(x0, x_end, n):
    h = (x_end - x0) / n

    x = np.linspace(0, 1, n + 1)
    A = np.zeros((n + 1, n + 1))
    b = np.zeros(n + 1)

    # Boundary condition at x=0: 3u'(0) + u(0) = 0 => (3/h) u1 + (1 - 3/h) u0 = 0
    A[0, 0] = 1 - 3 / h
    A[0, 1] = 3 / h
    b[0] = 0

    # Boundary condition at x=1: u'(1) - u(1) = 5 => -(1/h)u_{n-1} + (1/h - 1)u_n = 5
    A[n, n - 1] = -1 / h
    A[n, n] = 1 / h - 1
    b[n] = 5

    for i in range(1, n):
        xi = x[i]
        A[i, i - 1] = 1
        A[i, i] = -(2 + h**2 * (xi**2 + 1))
        A[i, i + 1] = 1
        b[i] = h**2 * (-2 * xi**5 - 2 * xi**3 + 12 * xi)

    u = np.linalg.solve(A, b)

    return x, u

def fdm_solve(x0, x_end, eps=1e-2):
    n = 10
    p = 1 # порядок

    while True:
        x1, u1 = fdm(x0, x_end, n)
        x2, u2 = fdm(x0, x_end, 2 * n)

        max_diff = 0
        for i in range(0, len(u1)):
            max_diff = max(max_diff, abs(u1[i] - u2[2 * i]))

        d = max_diff / (2**p - 1)
        if d <= eps:
            return x2, u2
        
        n *= 2

def f(x, y):
    u, up = y
    return (up, (x*x + 1)*u - 2*x**5 - 2*x**3 + 12*x)

def rk4_step(x, y, h):
    k1 = f(x, y)
    k2 = f(x + h/2, (y[0] + h*k1[0]/2, y[1] + h*k1[1]/2))
    k3 = f(x + h/2, (y[0] + h*k2[0]/2, y[1] + h*k2[1]/2))
    k4 = f(x + h,   (y[0] + h*k3[0],   y[1] + h*k3[1]))

    u_next  = y[0] + (h/6)*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
    up_next = y[1] + (h/6)*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])

    return (u_next, up_next)

def right_border(x0, x_end, u0, steps):
        y = (u0, -u0/3)
        x = x0
        h = (x_end-x0)/steps

        for _ in range(steps):
            y = rk4_step(x, y, h)
            x += h

        return y

def residual(x0, x_end, u0, N):
    u1, up1 = right_border(x0, x_end, u0, N)

    return (up1 - u1) - 5

def shooting(x0, x_end, N):
    h = (x_end - x0) / N

    L, R = -100.0, 100.0

    fL, fR = residual(x0, x_end, L, N), residual(x0, x_end, R, N)
    while R - L > 1e-6:
        M = 0.5*(L + R)
        fM = residual(x0, x_end, M, N)
        if fL * fM < 0:
            R, fR = M, fM
        else:
            L, fL = M, fM

    u0 = 0.5*(L + R)

    xs = [x0 + i*h for i in range(N+1)]
    ys = []

    y = (u0, -u0/3)
    x = x0

    ys.append(y[0])
    for _ in range(N):
        y = rk4_step(x, y, h)
        x += h
        ys.append(y[0])

    return xs, ys

def solve_shooting(x0, x_end, eps=1e-3):
    p = 4 # порядок метода
    N = 10
    
    while True:
        x1, y1 = shooting(x0, x_end, N)
        x2, y2 = shooting(x0, x_end, 2*N)

        max_diff = max(abs(y2[2*i] - y1[i]) for i in range(len(x1)))

        d = max_diff / (2**p - 1)
        if d <= eps:
            return x2, y2

        N *= 2

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

eps = 1e-2
xs1, us1 = fdm_solve(0, 1, eps)
xs2, us2 = solve_shooting(0, 1, eps)

plt.figure()
plt.plot(xs1, us1, label='Метод конечных разностей')
plt.plot(xs2, us2, label='Метод стрельбы')
plt.xlabel('x')
plt.ylabel('u(x)')
plt.legend()
plt.title("Solution of u'' - (x^2 + 1)u = -2x^5 - 2x^3 + 12x")
plt.grid(True)
plt.show()

delta = [abs(u1 - linear_interpolate(xs2, us2, x)) for x, u1 in zip(xs1, us1)]

plt.figure(figsize=(8,5))
plt.plot(xs1, delta, label="Разность решений")
plt.xlabel("x")
plt.ylabel("Δ(x)")
plt.title("Модуль разности решений")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
