#include <iostream>
#include <fstream>
#include <string>
using namespace std;

bool isSimpleNum(string word)
{
	if (word[0] == '+')
		word.erase(0, 1);

	for (int i = 0; i < word.length(); i++)
		if (!isdigit(word[i]))
			return false;

	int num = stoi(word);
	for (int i = 2; i <= sqrt(num); i++)
		if (num % i == 0)
			return false;

	return true;
}

int main()
{
	ifstream fin;
	fin.open("IN.txt");
	if (!fin.is_open())
	{
		cout << "Error opening IN!\n";
		exit(1);
	}
	fin.peek();
	if (!fin.good())
	{
		cout << "Error reading IN!\n";
		exit(2);
	}
	ofstream fout;
	fout.open("OUT.txt");
	if (!fout.is_open())
	{
		cout << "Error opening OUT!\n";
		exit(1);
	}
	string dil;
	getline(fin, dil);

	string line;
	while (getline(fin, line))
	{
		int pos1 = 0,
			pos2 = 0,
			min = INT16_MAX,
			max = 0,
			minID = -1,
			maxID = -1,
			minLen = 0,
			maxLen = 0;
		bool maxPl = false, minPl = false;
		while ((pos1 = line.find_first_not_of(dil, pos2)) != -1)
		{
			pos2 = line.find_first_of(dil, pos1);
			string word = line.substr(pos1, pos2 - pos1);

			if (isSimpleNum(word))
			{
				int num = stoi(word);
				if (num > max)
				{
					max = num;
					maxLen = word.length();
					maxID = pos1;
					if (word[0] == '+') 
						maxPl = true;
					else
						maxPl = false;
				}
				if (num < min)
				{
					min = num;
					minLen = word.length();
					minID = pos1;
					if (word[0] == '+')
						minPl = true;
					else
						minPl = false;
				}
			}
		}
		if (minID == maxID)
		{
			fout << "*" << line << '\n';
			continue;
		}

		if (minID > maxID)
		{
			//line.erase(minID, minLen);
			//line.insert(maxID, to_string(min));
			line.replace(minID, minLen, (maxPl ? "+" : "") + to_string(max));

			//line.erase(maxID+minLen, maxLen);
			//line.insert(minID + minLen - maxLen, to_string(max));
			line.replace(maxID, maxLen, (minPl ? "+" : "") + to_string(min));

		}else if (minID < maxID)
		{
			//line.erase(maxID, maxLen);
			//line.insert(minID, to_string(max));
			line.replace(maxID, maxLen, (minPl ? "+" : "") + to_string(min));

			//line.erase(minID + maxLen, minLen);
			//line.insert(maxID + maxLen - minLen, to_string(min));
			line.replace(minID, minLen, (maxPl ? "+" : "") + to_string(max));
		}

		fout << line << '\n';
	}
}

//#include <iostream>
//#include <fstream>
//#include <string>
//using namespace std;
//
//int functionHuiunction(int** arr, int N, int M) 
//{
//	int min = INT16_MAX;
//	int id = -1;
//	for (int i = 0; i < N; i++)
//		for (int j = 0; j < M; j++)
//			if (arr[i][j] <= min && arr[i][j] > 0)
//			{
//				min = arr[i][j];
//				id = i;
//			}
//	return id;
//}
//
//int main()
//{
//	fstream fin;
//	fin.open("IN.txt", ios::in | ios::out | ios::ate);
//	fin << '\n';
//	fin.seekg(0, ios_base::beg);
//	if (!fin.is_open())
//	{
//		cout << "Error opening IN!\n";
//		exit(1);
//	}
//	fin.peek();
//	if (!fin.good())
//	{
//		cout << "Error reading IN!\n";
//		exit(2);
//	}
//	int N, M;
//	fin >> N >> M;
//	int** arr = new int*[N];
//	for (int i = 0; i < N; i++)
//	{
//		arr[i] = new int[M];
//		for (int j = 0; j < M; j++)
//		{
//			fin >> arr[i][j];
//			if (!fin)
//			{
//				cout << "Vi eblan\n";
//				exit(1);
//			}
//		}
//	}
//	fin << "************\n" << functionHuiunction(arr, N, M);
//}