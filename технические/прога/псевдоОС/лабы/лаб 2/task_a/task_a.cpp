#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <thread>
#include <vector>
#include <algorithm>
#include <chrono>
#include <Windows.h>

struct Task
{
	Task() = default;

	Task(const std::string& str)
	{
		condition = str;
	}

	friend std::ostream& operator<<(std::ostream& out, const Task& task)
	{
		out << "\tCONDITION:\n"
			<< task.condition;
		return out;
	}

	friend std::istream& operator>>(std::istream& in, Task& task)
	{
		std::string buf;
		while (getline(in, buf))
		{
			task.condition += " " + buf;
		}
		return in;
	}

	std::string condition;
};

std::string to_lower(const std::string& str)
{
	std::string result = str;
	std::transform(result.begin(), result.end(), result.begin(), ::tolower);
	return result;
}

struct case_insensitive_string_comparator
{
	bool operator()(const std::string& str1, const std::string& str2) const
	{
		return to_lower(str1) < to_lower(str2);
	}
};

std::vector<std::string> find_most_common_words(const Task& task)
{
	std::map<std::string, int, case_insensitive_string_comparator> dictionary;
	std::string word;
	for (const char& i : task.condition)
	{
		if (std::ispunct(i) || std::isspace(i) || std::isdigit(i))
		{
			if (!word.empty())
			{
				++dictionary[word];
				word.clear();
			}
		}
		else
		{
			word += i;
		}
	}
	if (!word.empty())
	{
		++dictionary[word];
		word.clear();
	}
	std::vector<std::string> result;
	int mx = 0;
	for (auto& i : dictionary)
	{
		if (i.second > mx)
		{
			mx = i.second;
			result = {i.first};
		}
		else if (i.second == mx)
		{
			result.push_back(i.first);
		}
	}
	return result;
}

void handle_files(const std::string& input_file, const std::string& output_file)
{
	std::ifstream fin(input_file);
	if (!fin.is_open())
	{
		std::cerr << "File \"" << input_file << "\" didn't open!\n";
		return;
	}
	fin.peek();
	if (!fin.good())
	{
		std::cerr << "File \"" << input_file << "\" is empty!\n";
		fin.close();
		return;
	}
	std::ofstream fout(output_file);
	if (!fout.is_open())
	{
		std::cerr << "File \"" << output_file << "\" didn't open!\n";
		fin.close();
		return;
	}
	Task task;
	fin >> task;
	const std::vector<std::string> words = find_most_common_words(task);
	if (words.empty())
	{
		fout << "There are no words in the text!\n";
	}
	else
	{
		fout << "\tRESULT:\n";
		for (auto& word : words)
		{
			fout << word << "\n";
		}
	}
	fout.close();
}

int main()
{
	setlocale(LC_ALL, "russian");
	const auto start_time = std::chrono::high_resolution_clock::now();
	std::thread th(handle_files, "input.txt", "output.txt");
	SetThreadPriority(th.native_handle(), THREAD_PRIORITY_NORMAL);
	th.join();
	const auto end_time = std::chrono::high_resolution_clock::now();
	const auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
	std::cout << "Task finished in " << duration.count() << " milliseconds\n";
}
