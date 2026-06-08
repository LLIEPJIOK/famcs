import numpy as np

# Исходные коэффициенты системы
A = np.array([
    [-0.13, -0.02, 0],
    [-0.02, 0, 0.1],
    [0, -0.1, 1.0]
])
b = np.array([0, 0.1, 1])

# Перестановка строк для избежания нулей на диагонали
def rearrange_matrix(A, b):
    n = len(b)
    mult1 = A[1][0] / A[0][0]
    mult2 = A[1][2] / A[2][2]
    for i in range(n):
        A[1][i] -= A[0][i] * mult1
        A[1][i] -= A[2][i] * mult2
    b[1] -= b[0] * mult1
    b[1] -= b[2] * mult2
    
    return A, b

# Приведение системы к виду x = Bx + c
def to_iteration_form(A, b):
    n = A.shape[0]
    B = np.zeros_like(A, dtype=float)
    c = np.zeros_like(b, dtype=float)

    for i in range(n):
        for j in range(n):
            if i != j:
                B[i, j] = -A[i, j] / A[i, i]
        c[i] = b[i] / A[i, i]
    return B, c

# Проверка сходимости
def check_convergence(B):
    B_norm = np.max(np.sum(np.abs(B), axis=1))  # Норма строки
    if B_norm >= 1:
        raise ValueError("Матрица B не удовлетворяет условию сходимости (норма >= 1).")
    return B_norm

# Метод последовательных приближений
def simple_iterations(B, c, epsilon=1e-4, max_iterations=1000):
    x_prev = np.zeros_like(c)  # Начальное приближение
    for iteration in range(max_iterations):
        x_next = B @ x_prev + c  # Итерационная формула
        if np.linalg.norm(x_next - x_prev, ord=np.inf) < epsilon:  # Условие выхода
            return x_next, iteration + 1
        x_prev = x_next
    raise ValueError("Метод не сошелся за максимальное количество итераций.")

# Априорная оценка количества итераций
def apriori_iterations(B, x0, c, epsilon):
    x1 = B @ x0 + c
    B_norm = np.max(np.sum(np.abs(B), axis=1))
    return int(np.log(epsilon * (1 - B_norm) / np.linalg.norm(x1 - x0, ord=np.inf)) / np.log(B_norm)) + 1

# Основной блок программы
try:
    # Перестановка строк для устранения нулей на диагонали
    A, b = rearrange_matrix(A, b)

    # Приведение к итерационной форме
    B, c = to_iteration_form(A, b)
    print("Матрица B и вектор c:")
    print("B =")
    print(B)
    print("c =", c)

    B_norm = check_convergence(B)
    print(f"Норма матрицы B: {B_norm:.4f} < 1, метод сходится.")
    print(f"Коэффициент сжатия: {B_norm:.4f}")

    epsilon = 1e-4
    x0 = np.zeros_like(c)
    apriori_estimate = apriori_iterations(B, x0, c, epsilon)
    print(f"Априорная оценка количества итераций: {apriori_estimate}")

    solution, iterations = simple_iterations(B, c, epsilon)
    print(f"Решение: {solution}")
    print(f"Количество итераций: {iterations}")

    # Проверка решения
    residual = b - A @ solution
    print(f"Невязка: {residual}")

except ValueError as e:
    print("Ошибка:", e)
