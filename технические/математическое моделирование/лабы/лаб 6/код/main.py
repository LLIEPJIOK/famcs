import math
import random
import numpy as np
from scipy.linalg import solve
import matplotlib.pyplot as plt

def init_i(pi):
	r = random.uniform(0, 1)
	cum = 0.0

	for i, prob in enumerate(pi):
		cum += prob
		if r <= cum:
			return i

	return len(pi) - 1

def next_i(cur_i, p):
	r = random.uniform(0, 1)
	cum = 0.0

	for j, prob in enumerate(p[cur_i]):
		cum += prob
		if r <= cum:
			return j

	return len(p[cur_i]) - 1

def g_gen(a, pi, p):
	def g(h, i, j=-1):
		if i == -1:
			if pi[j] == 0:
				return 0
			
			return h[j] / pi[j]
		
		if p[i][j] == 0:
			return 0
		
		return a[i][j] / p[i][j]
	
	return g

def q_gen(a, pi, p):
	prev = 1
	g = g_gen(a, pi, p)

	def q(h, cur_i, prev_i=-1):
		nonlocal prev

		cur = prev * g(h, prev_i, cur_i)
		prev = cur

		return cur
	
	return q

def monte_carlo(a, f, pi, p, n=100, l=100):
	size = len(a)
	xs = []

	for i in range(size):
		xi = 0.0

		h = [0.0] * size
		h[i] = 1.0

		for _ in range(l):
			q = q_gen(a, pi, p)
			cur_i, prev_i = init_i(pi), -1

			ksi = 0.0
			for _ in range(n + 1):
				ksi += q(h, cur_i, prev_i) * f[cur_i]
				cur_i, prev_i = next_i(cur_i, p), cur_i
			
			xi += ksi

		xs.append(xi / l)

	return xs

def diff(x1, x2):
    size = len(x1)
    s = 0.0

    for i in range(size):
        s += (x1[i] - x2[i])**2

    return math.sqrt(s / size)

if __name__ == "__main__":
	size = 3
	a = [
		[1.0, -0.4, -0.1],
		[0.4, 0.7, -0.1],
		[0.3, 0.2, 1.0]
	]
	f = [-1, 5, -4]

	x = solve(np.array(a), np.array(f))
	print("Точное решение:", x)

	for i in range(size):
		a[i][i] -= 1

	for i in range(size):
		for j in range(size):
			a[i][j] = -a[i][j]

	pi = [1 / size] * size
	p = [[1 / size] * size for _ in range(size)]

	ns = [10, 50, 100, 200, 500]
	ls = [100, 1000, 5000, 10000, 50000]

	print("\nТаблица погрешности:")
	print("N\\L", end="\t")
	for L in ls:
		print(L, end="\t")
	print()

	errors_table = []
	for N in ns:
		row = []
		print(N, end="\t")

		for L in ls:
			xs = monte_carlo(a, f, pi, p, n=N, l=L)
			error = diff(xs, x)
			row.append(error)
			print(f"{error:.4f}", end="\t")

		errors_table.append(row)
		print()

	for i, N in enumerate(ns):
		plt.plot(ls, errors_table[i], marker='o', label=f'N={N}')
	plt.xlabel('Число цепей Маркова')
	plt.ylabel('Ошибка')
	plt.title('Точность решения')
	plt.legend()
	plt.grid(True)
	plt.show()