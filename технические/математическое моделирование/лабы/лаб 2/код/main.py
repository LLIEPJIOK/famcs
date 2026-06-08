import matplotlib.pyplot as plt
import random
import math
from scipy.stats import chi2 # Табличные значения

def plot(values, pmf, title):
	min_k = min(values)
	max_k = max(values)
	ks = list(range(min_k, max_k + 1))
	n = len(values)

	plt.figure(figsize=(10, 6))
	plt.hist(values, 
					 bins=range(min(values), max(values)+2), 
					 alpha=0.7, 
					 rwidth=0.8,
					 color='skyblue', 
					 edgecolor='black',
					 align="left",
					 label='Эмпирические частоты'
					 )

	pmf_vals = [pmf(k) * n for k in ks]
	plt.plot(ks, 
					 pmf_vals,
					 linewidth=2, 
					 color='orange',
					 label='Теоретические частоты'
					 )

	plt.title(title)
	plt.xlabel('Количество неудач')
	plt.ylabel('Частота')
	plt.grid(True, alpha=0.3)
	plt.legend()
	plt.show()

def nb_pmf(params):
	r, p = params

	def pmf(k):
		if k < 0:
			return 0.0
		
		return math.comb(k + r - 1, r - 1) * (p ** r) * ((1 - p) ** k)
			
	return pmf

def geom_pmf(params):
	p = params[0]

	def pmf(k):
		if k < 0:
			return 0.0
		
		return (1 - p) ** k * p

	return pmf

def uniform_gen():
	def gen():
		u = random.uniform(0, 1)
		return u
	
	return gen

def nb_gen(params):
	r, p = params
	ugen = uniform_gen()

	def gen():
		successes = 0
		failures = 0

		while successes < r:
			u = ugen()
			if u < p:
				successes += 1
			else:
				failures += 1

		return failures
	
	return gen

def geom_gen(params):
	p = params[0]
	ugen = uniform_gen()

	def gen():
		failures = 0
		
		while True:
			u = ugen()

			if u < p:
				return failures

			failures += 1

	return gen

def mean(values):
    return sum(values)/len(values)

def variance(values):
    mn = mean(values)
    return sum((x - mn) ** 2 for x in values) / (len(values) - 1)

def pearson(values, pmf, alpha=0.05):
	n = len(values)
	max_k = max(values)
	obs = [0] * (max_k + 1)

	for v in values:
			obs[v] += 1

	exp = [n * pmf(k) for k in range(max_k + 1)]

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

	df = len(obs_new)
	delta = chi2.ppf(1 - alpha, df)

	return chi_square, delta, chi_square < delta

def nb_modeling(params, other_params, n=1000):	
	pmf = nb_pmf(params)
	r, p = params
	gen = nb_gen(params)
	results = [gen() for _ in range(n)]
	plot(results, pmf, f'Отрицательное биномиальное распределение (r={r}, p={p})')

	mean_emp = mean(results)
	var_emp = variance(results)

	mean_theor = r * (1 - p) / p
	var_theor = mean_theor / p

	print(f"Математическое ожидание: {mean_emp:.4f}, ожидаемое: {mean_theor:.4f}")
	print(f"Дисперсия: {var_emp:.4f}, ожидаемая: {var_theor:.4f}")

	chi_square, delta, h0 = pearson(results, pmf)
	print(f"Chi-square: {chi_square:.4f}, критическое значение: {delta:.4f}, H0 {'не отвергнута' if h0 else 'отвергнута'}")

	other_pmf = geom_pmf(other_params)
	chi_square_other, delta_other, h0_other = pearson(results, other_pmf)
	print(f"Chi-square (геом.): {chi_square_other:.4f}, критическое значение: {delta_other:.4f}, H0 {'не отвергнута' if h0_other else 'отвергнута'}")

def geom_modeling(params, other_params, n=1000):	
	pmf = geom_pmf(params)
	p = params[0]
	gen = geom_gen(params)
	results = [gen() for _ in range(n)]
	plot(results, pmf, f'Геометрическое распределение (p={p})')

	mean_emp = mean(results)
	var_emp = variance(results)

	mean_theor = (1 - p) / p
	var_theor = mean_theor / p

	print(f"Математическое ожидание: {mean_emp:.4f}, ожидаемое: {mean_theor:.4f}")
	print(f"Дисперсия: {var_emp:.4f}, ожидаемая: {var_theor:.4f}")

	chi_square, delta, h0 = pearson(results, pmf)
	print(f"Chi-square: {chi_square:.4f}, критическое значение: {delta:.4f}, H0 {'не отвергнута' if h0 else 'отвергнута'}")

	other_pmf = nb_pmf(other_params)
	chi_square_other, delta_other, h0_other = pearson(results, other_pmf)
	print(f"Chi-square (бином.): {chi_square_other:.4f}, критическое значение: {delta_other:.4f}, H0 {'не отвергнута' if h0_other else 'отвергнута'}")

def nb(params, other_params, n=1000):
	print("\n\n--- Отрицательное биномиальное распределение ---")
	nb_modeling(params, other_params, n)

	gen = nb_gen(params)
	pmf = nb_pmf(params)
	num_experiments = 1000
	check_n = [n // 10, n, 10 * n]

	for cur_n in check_n:
		rejections = 0
		for _ in range(num_experiments):
			results = [gen() for _ in range(cur_n)]
			_, _, ho = pearson(results, pmf)

			if not ho:
				rejections += 1
		
		print(f"n={cur_n}: H0 отвергнута в {rejections} из {num_experiments} экспериментов ({(rejections / num_experiments):.2f})")

def geom(params, other_params, n=1000):
	print("\n\n--- Геометрическое распределение ---")
	geom_modeling(params, other_params, n)

	gen = geom_gen(params)
	pmf = geom_pmf(params)
	num_experiments = 1000
	check_n = [n // 10, n, 10 * n]

	for cur_n in check_n:
		rejections = 0
		for _ in range(num_experiments):
			results = [gen() for _ in range(cur_n)] 
			_, _, ho = pearson(results, pmf)

			if not ho:
				rejections += 1
		
		print(f"n={cur_n}: H0 отвергнута в {rejections} из {num_experiments} экспериментов ({(rejections / num_experiments):.2f})")

if __name__ == "__main__":
	nb_params = (4, 0.2)
	geom_params = (0.25,)

	nb(nb_params, geom_params)
	geom(geom_params, nb_params)