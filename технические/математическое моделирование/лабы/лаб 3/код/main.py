import math
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gammainc
from scipy.stats import chi2, kstwo # Табличные значения
from scipy.special import betainc # для распределения Фишера

WINDOW = 70

def print_windowed(text):
	print('\n' + '=' * WINDOW)
	print(text)
	print('=' * WINDOW)

def plot(values, pdf, title):
	plt.hist(values, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Эмпирическая плотность')

	xs = [i / 10 for i in range(10 * int(min(values)), int(10 * max(values)) + 1)]
	ys = [pdf(x) for x in xs]
	plt.plot(xs, ys, color='orange', linewidth=2, label='Теоретическая плотность')

	plt.title(title)
	plt.xlabel('x')
	plt.ylabel('Плотность вероятности')
	plt.legend()
	plt.grid(True, alpha=0.3)
	plt.show()

def normal_pdf(m, s2):
	def pdf(x):
		s = math.sqrt(s2)

		return (1 / (s * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - m) / s) ** 2)

	return pdf

def chi2_pdf(k):
	def pdf(x):
		if x < 0:
			return 0.0

		return (1 / (2 ** (k / 2) * math.gamma(k / 2))) * (x ** (k / 2 - 1)) * math.exp(-x / 2)

	return pdf

def fisher_pdf(l, m):
	def pdf(x):
		if x <= 0:
			return 0.0

		num = (l * x) ** l * m ** m
		den = (l * x + m) ** (l + m)
		fraction = num / den

		beta = math.gamma(l / 2) * math.gamma(m / 2) / math.gamma((l + m) / 2)

		return math.sqrt(fraction) / (x * beta)

	return pdf

def normal_cdf(m, s2):
	def cdf(x):
		s = math.sqrt(s2)
		z = (x - m) / s

		return 0.5 * (1 + math.erf(z / math.sqrt(2)))

	return cdf

def chi2_cdf(k):
	def cdf(x):
		if x < 0:
			return 0.0

		return gammainc(k / 2, x / 2)

	return cdf

def fisher_cdf(l, m):
	def cdf(x):
		if x < 0:
			return 0.0

		z = (l * x) / (l * x + m)

		return betainc(l / 2, m / 2, z)

	return cdf

def mean(values):
	return sum(values) / len(values)

def normal_mean(m, s2):
	return m

def chi2_mean(m):
	return m

def fisher_mean(l, m):
	if m <= 2:
		raise ValueError("m must be greater than 2 to have a defined mean")

	return m / (m - 2)

def variance(values, mean):
	return sum((x - mean) ** 2 for x in values) / (len(values) - 1)

def normal_variance(m, s2):
	return s2

def chi2_variance(m):
	return 2 * m

def fisher_variance(l, m):
	if m <= 4:
		raise ValueError("m must be greater than 4 to have a defined variance")

	return (2 * m ** 2 * (l + m - 2)) / (l * (m - 2) ** 2 * (m - 4))

def box_muller_gen():
	def gen():
		u1 = random.uniform(0, 1)
		u2 = random.uniform(0, 1)
		z = math.cos(2 * math.pi * u2) * math.sqrt(-2 * math.log(u1))

		return z

	return gen

def normal_gen(m, s2):
	bmgen = box_muller_gen()

	def gen():
		return m + math.sqrt(s2) * bmgen()

	return gen

def chi2_gen(m):
	bmgen = box_muller_gen()

	def gen():
		return sum(bmgen() ** 2 for _ in range(m))

	return gen

def fisher_gen(l, m):
	x_gen = chi2_gen(l)
	y_gen = chi2_gen(m)

	def gen():
		x = x_gen()
		y = y_gen()

		return (x / l) / (y / m)

	return gen

def kolmogorov(values, cdf, alpha=0.05):
	n = len(values)
	sorted_values = sorted(values)

	d1 = max((i+1)/n - cdf(x) for i, x in enumerate(sorted_values))
	d2 = max(cdf(x) - i/n for i, x in enumerate(sorted_values))
	d = max(d1, d2)

	delta = kstwo.ppf(1-alpha, n)

	return d, delta, d < delta

def pearson(values, pdf, bins=50, l=100, alpha=0.05):
	n = len(values)
	min_v, max_v = min(values), max(values)
	bin_edges = [min_v + i * (max_v - min_v) / bins for i in range(bins + 1)]

	obs = [0] * bins
	for v in values:
		for i in range(bins):
			if bin_edges[i] <= v < bin_edges[i + 1]:
				obs[i] += 1
				break

	exp = []
	for i in range(bins):
		x1, x2 = bin_edges[i], bin_edges[i + 1]
		# аппроксимация
		step = (x2 - x1) / l
		midpoints = [x1 + j * step for j in range(l + 1)]
		area = sum(pdf(x) for x in midpoints) * step
		exp.append(area * n)

	obs_new, exp_new = [], []
	acc_obs, acc_exp = 0, 0
	for o, e in zip(obs, exp):
		acc_obs += o
		acc_exp += e
		if acc_exp >= 5:
			obs_new.append(acc_obs)
			exp_new.append(acc_exp)
			acc_obs, acc_exp = 0, 0
	if acc_exp > 0:
		obs_new[-1] += acc_obs
		exp_new[-1] += acc_exp

	chi_square = sum((o - e) ** 2 / e for o, e in zip(obs_new, exp_new))
	df = len(obs_new) - 1
	delta = chi2.ppf(1 - alpha, df)

	return chi_square, delta, chi_square < delta

def check(values, pdf, cdf, type):
	kolmogorov_stat, delta, is_valid = kolmogorov(values, cdf)
	print(f'Колмогоров ({type}): {kolmogorov_stat}, Критическое значение: {delta}, Статистика: {"Принята" if is_valid else "Отклонена"}')

	chi_square, delta, is_valid = pearson(values, pdf)
	print(f'Хи-квадрат ({type}): {chi_square}, Критическое значение: {delta}, Статистика: {"Принята" if is_valid else "Отклонена"}')

def check_error(gen, pdf, cdf, exp=1000, n=1000):
	kolmogorov_errors = 0
	pearson_errors = 0
	for _ in range(exp):
		values = [gen() for _ in range(n)]
		
		_, _, is_valid = kolmogorov(values, cdf)
		if not is_valid:
			kolmogorov_errors += 1

		_, _, is_valid = pearson(values, pdf)
		if not is_valid:
			pearson_errors += 1

	print(f'Ошибки (Колмогоров, n={n}): {kolmogorov_errors} из {exp} ({(kolmogorov_errors/exp):.2f})')
	print(f'Ошибки (Хи-квадрат, n={n}): {pearson_errors} из {exp} ({(pearson_errors/exp):.2f})')

def simulate_normal(m, s2, n=1000):
	print_windowed(f'Нормальное распределение N({m}, {s2})')

	gen = normal_gen(m, s2)
	values = [gen() for _ in range(n)]
	pdf = normal_pdf(m, s2)

	plot(values, pdf, 'Нормальное распределение')

	mean_val = mean(values)
	expected_mean = normal_mean(m, s2)
	print(f'Выборочное среднее: {mean_val}, Ожидаемое среднее: {expected_mean}')

	variance_val = variance(values, mean_val)
	expected_variance = normal_variance(m, s2)
	print(f'Выборочная дисперсия: {variance_val}, Ожидаемая дисперсия: {expected_variance}')

	cdf = normal_cdf(m, s2)

	check(values, pdf, cdf, 'нормальное')

	chi2pdf = chi2_pdf(4)
	chi2cdf = chi2_cdf(4)
	check(values, chi2pdf, chi2cdf, 'хи-квадрат')

	fisherpdf = fisher_pdf(5, 3)
	fishercdf = fisher_cdf(5, 3)
	check(values, fisherpdf, fishercdf, 'Фишера')

	ns = [100, 1000, 10000]
	for n in ns:
		check_error(gen, pdf, cdf, n=n)

def simulate_chi2(m, n=1000):
	print_windowed(f'Распределение хи-квадрат с {m} степенями свободы')

	gen = chi2_gen(m)
	values = [gen() for _ in range(n)]
	pdf = chi2_pdf(m)

	plot(values, pdf, f'Распределение хи-квадрат с {m} степенями свободы')

	mean_val = mean(values)
	expected_mean = chi2_mean(m)
	print(f'Выборочное среднее: {mean_val}, Ожидаемое среднее: {expected_mean}')

	variance_val = variance(values, mean_val)
	expected_variance = chi2_variance(m)
	print(f'Выборочная дисперсия: {variance_val}, Ожидаемая дисперсия: {expected_variance}')

	cdf = chi2_cdf(m)
	check(values, pdf, cdf, 'хи-квадрат')

	normalcdf = normal_cdf(0, 64)
	normalpdf = normal_pdf(0, 64)
	check(values, normalpdf, normalcdf, 'нормальное')

	fisherpdf = fisher_pdf(5, 3)
	fishercdf = fisher_cdf(5, 3)
	check(values, fisherpdf, fishercdf, 'Фишера')

	ns = [100, 1000, 10000]
	for n in ns:
		check_error(gen, pdf, cdf, n=n)

def simulate_fisher(l, m, n=1000):
	print_windowed(f'Распределение Фишера F({l}, {m})')

	gen = fisher_gen(l, m)
	values = [gen() for _ in range(n)]
	cutoff = np.quantile(values, 0.99)
	values = [x for x in values if x <= cutoff]
	pdf = fisher_pdf(l, m)

	plot(values, pdf, f'Распределение Фишера F({l}, {m})')

	if m >= 2:
		mean_val = mean(values)
		expected_mean = fisher_mean(l, m)
		print(f'Выборочное среднее: {mean_val}, Ожидаемое среднее: {expected_mean}')
	else:
		print('Среднее не определено для m <= 2')
	
	if m >= 4:
		variance_val = variance(values, mean_val)
		expected_variance = fisher_variance(l, m)
		print(f'Выборочная дисперсия: {variance_val}, Ожидаемая дисперсия: {expected_variance}')
	else:
		print('Дисперсия не определена для m <= 4')

	cdf = fisher_cdf(l, m)
	check(values, pdf, cdf, 'Фишера')

	normalcdf = normal_cdf(0, 64)
	normalpdf = normal_pdf(0, 64)
	check(values, normalpdf, normalcdf, 'нормальное')

	chi2pdf = chi2_pdf(4)
	chi2cdf = chi2_cdf(4)
	check(values, chi2pdf, chi2cdf, 'хи-квадрат')

	ns = [100, 1000, 10000]
	for n in ns:
		check_error(gen, pdf, cdf, n=n)

if __name__ == "__main__":
	simulate_normal(m=0, s2=64)
	simulate_chi2(m=4)
	simulate_fisher(l=5, m=3)