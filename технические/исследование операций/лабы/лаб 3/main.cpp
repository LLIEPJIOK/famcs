#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <cmath>

using namespace std;

const long long INF = 1e18;

struct Road
{
	long long u, v, w;
};

long long N, M;
vector<vector<long long>> distMatrix;
vector<Road> roads;

long long calculateSumForPoint(int u, int v, long long w, long long d)
{
	long long total = 0;
	for (int k = 0; k < N; ++k)
	{
		long long du = distMatrix[k][u] + d;
		long long dv = distMatrix[k][v] + (w - d);
		total += min(du, dv);
	}

	return total;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	cin >> N >> M;
	distMatrix.assign(N, vector<long long>(N, INF));
	for (int i = 0; i < N; ++i)
	{
		distMatrix[i][i] = 0;
	}

	roads.reserve(M);
	for (int i = 0; i < M; ++i)
	{
		long long u, v, w;
		cin >> u >> v >> w;
		--u;
		--v;
		distMatrix[u][v] = distMatrix[v][u] = min(distMatrix[u][v], w);
		roads.push_back({u, v, w});
	}

	// Флойд–Уоршелл
	for (int k = 0; k < N; ++k)
	{
		for (int i = 0; i < N; ++i)
		{
			for (int j = 0; j < N; ++j)
			{
				if (distMatrix[i][k] + distMatrix[k][j] < distMatrix[i][j])
				{
					distMatrix[i][j] = distMatrix[i][k] + distMatrix[k][j];
				}
			}
		}
	}

	long long bestSum = INF;
	long long bestType = 0; // 0 = дом, 1 = дорога
	long long bestU = -1, bestV = -1;
	long long bestD = 0;

	// Проверка всех домов
	for (int i = 0; i < N; ++i)
	{
		long long sum = accumulate(distMatrix[i].begin(), distMatrix[i].end(), 0ll);
		if (sum < bestSum)
		{
			bestSum = sum;
			bestType = 0;
			bestU = i;
		}
	}

	// Проверка точек на дорогах
	for (auto [u, v, w] : roads)
	{
		long long l = 1, r = w - 1;
		while (r - l >= 3)
		{
			long long m1 = l + (r - l) / 3;
			long long m2 = r - (r - l) / 3;
			long long sum1 = calculateSumForPoint(u, v, w, m1);
			long long sum2 = calculateSumForPoint(u, v, w, m2);
			if (sum1 < sum2)
			{
				r = m2;
			}
			else
			{
				l = m1;
			}
		}

		for (long long d = l; d <= r; ++d)
		{
			long long sum = calculateSumForPoint(u, v, w, d);
			if (sum < bestSum)
			{
				bestSum = sum;
				bestType = 1;
				bestU = u;
				bestV = v;
				bestD = d;
			}
		}
	}

	if (bestType == 0)
	{
		cout << bestU + 1 << " " << bestSum;
	}
	else
	{
		cout << bestU + 1 << " " << bestV + 1 << " " << bestD;
	}

	return 0;
}
