#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <thread>
#include <vector>
#include <algorithm>
#include <Windows.h>

#undef max
#undef min

int iii = 0;

struct Task
{
	Task() = default;

	explicit Task(const std::string& str)
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

struct Info
{
	int completed_tasks = 0;
	int no_solution_tasks = 0;
	long long time = 0;
	bool is_working = true;
	std::map<int, std::string> results;
};

class Handler
{
public:
	static void func()
	{
		while (true)
		{
			if (working_threads_ == 0)
			{
				break;
			}
			std::cout << "--------------------------------------------\n";
			for (int i = 0; i < thread_count_; ++i)
			{
				std::cout << "Thread #" << i + 1 << "\tcompleted tasks - " << infos_[i].completed_tasks << "\t" << (infos_[i].is_working ? "(working)\n" : ("not working\n"));
			}
			std::cout << "--------------------------------------------\n";
			std::this_thread::sleep_for(std::chrono::seconds(1));
		}
	}
	static void handle_thread(const int id)
	{
		while (cur_task_ < task_count_)
		{
			auto start = std::chrono::high_resolution_clock::now();
			int task = cur_task_++;
			std::string result = handle_task(tasks_[task]);
			if (result.empty())
			{
				infos_[id].results[task] = "There are no words in the text!";
				++infos_[id].no_solution_tasks;
			}
			else
			{
				infos_[id].results[task] = result;
			}
			++infos_[id].completed_tasks;
			auto end = std::chrono::high_resolution_clock::now();
			auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
			infos_[id].time += duration.count();
			min_time_ = std::min(min_time_, duration.count());
			max_time_ = std::max(max_time_, duration.count());
		}
		--working_threads_;
	}

	static std::vector<Task> random_generate_tasks(const int task_count, const int thread_count)
	{
		working_threads_ = 0;
		task_count_ = task_count;
		cur_task_ = 0;
		thread_count_ = thread_count;
		infos_.resize(thread_count);
		tasks_.clear();
		const std::string puncts = " -!,.?:;\n\t";
		for (int i = 0; i < task_count; ++i)
		{
			std::string str;
			const int number_of_words = rand() % 100;
			for (int j = 0; j < number_of_words; ++j)
			{
				if (j != 0)
				{
					str += puncts[rand() % puncts.size()];
				}
				str += generate_random_string(rand() % 10 + 1);
			}
			tasks_.emplace_back(str);
		}
		return tasks_;
	}

	static void inc_working_threads()
	{
		++working_threads_;
	}

	static const std::vector<Task>& get_tasks()
	{
		return tasks_;
	}

	static const std::vector<Info>& get_infos()
	{
		return infos_;
	}

	static int get_working_threads()
	{
		return working_threads_;
	}

	static long long get_min_time()
	{
		return min_time_;
	}

	static long long get_max_time()
	{
		return max_time_;
	}

private:
	struct case_insensitive_string_comparator
	{
		bool operator()(const std::string& str1, const std::string& str2) const
		{
			return to_lower(str1) < to_lower(str2);
		}
	};

	static std::string to_lower(const std::string& str)
	{
		std::string result = str;
		std::transform(result.begin(), result.end(), result.begin(), ::tolower);
		return result;
	}

	static std::vector<std::string> find_most_common_words(const std::string& str)
	{
		std::map<std::string, int, case_insensitive_string_comparator> dictionary;
		std::string word;
		for (const char& i : str)
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

	static std::string handle_task(const Task& task)
	{
		const std::vector<std::string> words = find_most_common_words(task.condition);
		std::string result;
		for (int i = 0; i < words.size(); ++i)
		{
			if (i != 0)
			{
				result += "\n";
			}
			result += words[i];
		}
		return result;
	}

	static std::string generate_random_string(const int length)
	{
		const std::string characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
			"abcdefghijklmnopqrstuvwxyz"
			"ÀÁÂÃÄÅ¨ÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß"
			"àáâãäå¸æçèéêëìíîïðñòóôõö÷øùúûüýþÿ";
		std::string random_string;
		for (int i = 0; i < length; ++i)
		{
			random_string += characters[rand() % characters.size()];
		}

		return random_string;
	}

	static int working_threads_;
	static int task_count_;
	static int thread_count_;
	static int cur_task_;
	static long long min_time_;
	static long long max_time_;
	static std::vector<Task> tasks_;
	static std::vector<Info> infos_;
};

int Handler::cur_task_ = 0;
int Handler::task_count_ = 0;
int Handler::thread_count_ = 0;
int Handler::working_threads_ = 0;
long long Handler::min_time_ = INT64_MAX;
long long Handler::max_time_ = INT64_MIN;
std::vector<Task> Handler::tasks_ = {};
std::vector<Info> Handler::infos_ = {};

int main()
{
	setlocale(LC_ALL, "russian");
	std::srand(static_cast<unsigned int>(std::time(nullptr)));
	int task_count, thread_count;
	std::cout << "Enter task_count\n";
	while (!(std::cin >> task_count) || task_count < 0)
	{
		std::cout << "Invalid input. Please enter a non-negative integer for task_count: ";
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	}

	std::cout << "Enter thread_count\n";
	while (!(std::cin >> thread_count) || thread_count <= 0)
	{
		std::cout << "Invalid input. Please enter a positive integer for thread_count: ";
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	}
	Handler::random_generate_tasks(task_count, thread_count);
	for (int i = 0; i < thread_count; ++i)
	{
		std::thread th(&Handler::handle_thread, i);
		SetThreadPriority(th.native_handle(), THREAD_PRIORITY_NORMAL);
		th.detach();
		Handler::inc_working_threads();
	}
	std::thread th(&Handler::func);
	//SetThreadPriority(th.native_handle(), THREAD_PRIORITY_LOWEST);
	SetThreadPriority(th.native_handle(), THREAD_PRIORITY_HIGHEST);
	th.join();
	const auto tasks = Handler::get_tasks();
	const auto infos = Handler::get_infos();
	std::vector<std::string> results(task_count);
	for (auto& i : infos)
	{
		for (auto& j : i.results)
		{
			results[j.first] = j.second;
		}
	}
	const auto start_time = std::chrono::high_resolution_clock::now();
	std::ofstream fout("output.txt");
	if (!fout.is_open())
	{
		std::cerr << "Can't open file to write results!\n";
	}
	else
	{
		if (task_count == 0)
		{
			fout << "There was no tasks\n";
		}
		for (int i = 0; i < task_count; ++i)
		{
			fout << "-------------------------------------------\n"
				<< "----------------- Task " << i + 1 << " ------------------\n"
				<< tasks[i] << "\n"
				<< "-------------------------------------------\n"
				<< "\tRESULT:\n"
				<< results[i] << "\n\n";
		}
		fout.close();
	}
	const auto end_time = std::chrono::high_resolution_clock::now();
	const auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
	int no_solution_tasks = 0;
	for (auto& i : infos)
	{
		no_solution_tasks += i.no_solution_tasks;
	}
	std::cout << "-------------------------------------------\n"
		<< "--------------- Information ---------------\n"
		<< task_count << " tasks completed\n"
		<< "0 problems weren't solved due to an error\n"
		<< no_solution_tasks << " tasks haven't got solution\n"
		<< (Handler::get_min_time() == INT64_MAX ? "-" : std::to_string(Handler::get_min_time())) <<
		" milliseconds - min time for task\n"
		<< (Handler::get_max_time() == INT64_MIN ? "-" : std::to_string(Handler::get_max_time())) <<
		" milliseconds - max time for task\n"
		<< duration.count() << " milliseconds for writing output file\n";
	for (int i = 0; i < thread_count; ++i)
	{
		std::cout << "-------------------------------------------\n"
			<< "---------------- Thread " << i + 1 << " -----------------\n"
			<< infos[i].completed_tasks << " tasks were completed\n"
			<< infos[i].time << " milliseconds -  time needed to complete this tasks\n";
	}
}
