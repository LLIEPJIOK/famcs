#include <fstream>
#include <iostream>
#include <vector>
#include <thread>
#include <Windows.h>

using namespace std;

struct Task
{
    friend std::ostream& operator<<(std::ostream& out, const Task& task)
    {
        out << task.koefs.size() - 1;
        for (int i = 0; i < task.koefs.size(); ++i)
        {
            out << task.koefs[i] << " ";
        }
        out << "\n" << task.c;
        return out;
    }

    friend std::istream& operator>>(std::istream& in, Task& task)
    {
        int deg;
        in >> deg;
        if (deg < 0)
        {
            cout << "Invalid degree" << endl;
            exit(0);
        }
        task.koefs.resize(deg + 1);
        for (int i = 0; i <= deg; ++i)
        {
            if (!(in >> task.koefs[i]))
            {
                cout << "Invalid input" << endl;
                exit(0);
            }
        }
        if (!(in >> task.c))
        {
            cout << "Invalid input" << endl;
            exit(0);
        }
        string str;
        if (in >> str)
        {
	        cout << "Invalid input" << endl;
            exit(0);
        }
        return in;
    }

    vector<int> koefs;
    int c;
};

void Reader(string in, string out)
{
    ifstream fin(in);
    if (!fin.is_open()) {
        cout << "Error opening input file" << endl;
        return;
    }
    /*if (!fin)
    {
        cout << "Error opening input file" << endl;
        return;
    }*/
    ofstream fout(out);
    if (!fout.is_open()) {
        cout << "Error opening output file" << endl;
        return;
    }
    /*if (!fout)
    {
        cout << "Error opening output file" << endl;
        return;
    }*/
    Task task;
    fin >> task;
    vector<int> a(task.koefs.size());
    a[0] = task.koefs[0];
    for (int i = 1; i < a.size(); ++i)
    {
        a[i] = a[i - 1] * task.c + task.koefs[i];
    }
    fout << a.size() - 2 << "\n";
    for (int i = 0; i < a.size() - 1; ++i)
    {
        fout << a[i] << " ";
    }
    fout << "\n" << a.back() << "\n";
}

int main()
{
    const auto start = std::chrono::high_resolution_clock::now();
    thread th(Reader, "input.txt", "output.txt");
    if (!th.joinable())
    {
        cerr << "Error starting the thread" << endl;
        return 1;
    }
    SetThreadPriority(th.native_handle(), THREAD_PRIORITY_NORMAL);
    th.join();
    const auto end = std::chrono::high_resolution_clock::now();
    const auto total = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Finished in " << total.count() << " milliseconds\n";
    return 0;
}