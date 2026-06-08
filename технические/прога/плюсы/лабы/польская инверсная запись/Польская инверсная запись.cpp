#include <iostream>
#include <fstream>
#include <string>
#include <stack>

int main()
{
    //в польскую
    std::ifstream fin("in.txt");
    if (!fin.is_open())
    {
        std::cerr << "Входной файл не открылся\n";
        exit(1);
    }
    fin.peek();
    if (!fin.good())
    {
        std::cerr << "Файл пустой\n";
        exit(2);
    }
    char ch;
    std::string str;
    std::stack <char> schar;
    while (fin.peek() == ' ')
        fin.ignore();
    while (fin.peek() != '\n' && !fin.eof())
    {
        if (isdigit(fin.peek()))
        {
            double numb;
            fin >> numb;
            str += std::to_string(numb) + " ";
            continue;
        }
        fin.get(ch);
        if (ch == '(')
        {
            schar.push(ch);
            continue;
        }
        if (ch == ')')
        {
            while (schar.top() != '(')
            {
                str = str + schar.top() + " ";
                schar.pop();
            }
            schar.pop();
            continue;
        }
        if (schar.empty())
        {
            schar.push(ch);
            continue;
        }
        do
        {
            char bufs = schar.top();
            if (bufs == '(' || (bufs == '+' || bufs == '-') && (ch == '*' || ch == '/'))
                break;
            else
            {
                str = str +  bufs + " ";
                schar.pop();
            }
        } while (!schar.empty());
        schar.push(ch);
    }
    fin.close();
    while (!schar.empty())
    {
        str = str + schar.top() + " ";
        schar.pop();
    }
    std::cout << str << '\n'; //вывод в польской

    //из польской
    std::stack <double> sint;
    while (!str.empty())
    {
        if (isdigit(str[0]))
        {
            int i = str.find(' ');
            double numb = stod(str.substr(0, i));
            str.erase(0, i);
            while (str[0] == ' ')
                str.erase(0, 1);
            sint.push(numb);
            continue;
        }
        ch = str[0];
        if (ch == '-')
        {
            if (sint.size() == 1)
            {
                double numb = -sint.top();
                sint.pop();
                sint.push(numb);
                str.erase(0, 1);
                while (str[0] == ' ')
                    str.erase(0, 1);
                continue;
            }
            double numb2 = sint.top();
            sint.pop();
            double numb1 = sint.top();
            sint.pop();
            sint.push(numb1 - numb2);
            str.erase(0, 1);
            while (str[0] == ' ')
                str.erase(0, 1);
            continue;
        }
        if (ch == '+')
        {
            if (sint.size() == 1)
            {
                str.erase(0, 2);
                continue;
            }
            double numb2 = sint.top();
            sint.pop();
            double numb1 = sint.top();
            sint.pop();
            sint.push(numb1 + numb2);
            str.erase(0, 1);
            while (str[0] == ' ')
                str.erase(0, 1);
            continue;
        }
        if (ch == '*')
        {
            double numb2 = sint.top();
            sint.pop();
            double numb1 = sint.top();
            sint.pop();
            sint.push(numb1 * numb2);
            str.erase(0, 1);
            while (str[0] == ' ')
                str.erase(0, 1);
            continue;
        }
        if (ch == '/')
        {
            double numb2 = sint.top();
            sint.pop();
            double numb1 = sint.top();
            sint.pop();
            sint.push(numb1 / numb2);
            str.erase(0, 1);
            while (str[0] == ' ')
                str.erase(0, 1);
            continue;
        }
    }
    std::cout << sint.top() << '\n';//вывод результата
    return 0;
}