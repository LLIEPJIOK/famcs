#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

//      ------- Функция для считывания вагонов со входного пути (файла) ----------

vector<unsigned int> GetCarriageEntrance(vector<unsigned int>& carriage_entrance)
{
    fstream entrance("вход.txt", ios::in | ios::out);
    unsigned int buffer;
    while (!entrance.eof())
    {
        entrance >> buffer;
        carriage_entrance.push_back(buffer);
    }
    entrance.close();
    return carriage_entrance;
}

//      ---------- Функция для въезда вагонов в выходной путь(файл) ---------------

void Exit(vector<unsigned int>& carriage_exit, int& k_exit)
{
    fstream exit("выход.txt", ios::in | ios::out | ios::trunc);
    k_exit++;
    for (int i = k_exit - 1; i >= 0; i--)
    {
        exit << carriage_exit[i] << " ";
    }
    exit.close();
}

//      ----------- Функция для выезда вагонов из входного пути(файла) -------------

void EntranceOut(vector<unsigned int>& carriage_entrance, int& k_entr)
{
    fstream entrance("вход.txt", ios::in | ios::out | ios::trunc);
    k_entr--;
    for (int i = 0; i < k_entr; i++)
    {
        entrance << carriage_entrance[i] << " ";
    }
    entrance.close();
}

//      ------------- Функция для въезда вагонов во входной путь(файл) ---------------

void EntranceIn(vector<unsigned int>& carriage_entrance, int& k_entr)
{
    fstream entrance("вход.txt", ios::in | ios::out | ios::trunc);
    k_entr++;
    for (int i = 0; i < k_entr; i++)
    {
        entrance << carriage_entrance[i] << " ";
    }
    entrance.close();
}

//      --------------- Функция для въезда вагонов в тупик(3-ий файл) ----------------

void ImpasseIn(vector<unsigned int>& carriage_impasse, int& k_imp)
{
    fstream impasse("тупик.txt", ios::in | ios::out | ios::trunc);
    k_imp++;
    for (int i = 0; i < k_imp; i++)
    {
        impasse << carriage_impasse[i] << " ";
    }
    impasse.close();
}

//      --------------- Функция для выезда вагонов из тупика(3-ий файл) ---------------

void ImpasseOut(vector<unsigned int>& carriage_impasse, int& k_imp)
{
    fstream impasse("тупик, ios::in | ios::out | ios::trunc);
    k_imp--;
    for (int i = 0; i < k_imp; i++)
    {
        impasse << carriage_impasse[i] << " ";
    }
    impasse.close();
}

//              Функция для для проверки на наличие:
//              1. в тупике вагона отличного от первого вагона на выходе;
//              2. на входе последнего вагона отличного от первого вагона на выходе.

int CheckWay (vector<unsigned int>& carriage_exit, vector<unsigned int>& carriage_impasse, vector<unsigned int>& carriage_entrance, int& k_imp)
{
    if (k_imp  > 0 && carriage_exit[carriage_exit.size() - 1] != carriage_impasse.front())
    {
        return 1;
    }
    else
    {
        if (carriage_exit[carriage_exit.size() - 1] != carriage_entrance[carriage_entrance.size() - 1])
        {
            return 2;
        }
        else
            return 3;
    }
}

int main()
{
    
//    ----------------- Проверка на существование входа, выхода и тупика,---------------
//    ------------ а также создание выхода и тупика, если таковых не найдено -----------
    
    setlocale(LC_ALL, "Rus");
    fstream entrance("вход.txt");
    if (!entrance)
    {
        system("pause");
        return 1;
    }
    
    ofstream exit("выход.txt", ios::in | ios::out);
    if (!exit)
    {
        entrance.close();
        system("pause");
        return 2;
    }
    
    ofstream impasse("тупик.txt", ios::in | ios::out);
    if (!impasse)
    {
        entrance.close();
        exit.close();
        system("pause");
        return 3;
    }
    
    entrance.close();
    exit.close();
    impasse.close();
    
    // вектор для вагонов на входе
    vector <unsigned int> carriage_entrance;
    // вектор для вагонов на выходе
    vector <unsigned int> carriage_exit;
    // вектор для вагонов в тупике
    vector <unsigned int> carriage_impasse;
    
    // берём информацию о вагонах на входе
    GetCarriageEntrance(carriage_entrance);
    
    // количество вагоном на выходе, на входе и в тупике соответственно
    int k_exit = 0, k_entr = carriage_entrance.size(), k_imp = 0;
    
    // отправляем первый вагон на выход
    carriage_exit.push_back(carriage_entrance[k_entr - 1]);
    carriage_entrance.pop_back();
    EntranceOut(carriage_entrance, k_entr);
    Exit(carriage_exit, k_exit);
    
//  ------------ Сортировка вагонов на выход до тех пор, --------------
//  ------------ пока на входе и в тупике их не останется -------------
    
    while (k_entr > 0 || k_imp > 0)
    {
        switch (CheckWay(carriage_exit, carriage_impasse, carriage_entrance, k_imp))
        {
                
//  ---------------- Перевозка вагона из тупика ------------------------
//  ---------------- на вход и из входа на выход -----------------------
                
            case 1:
                carriage_entrance.push_back(carriage_impasse.front());
                carriage_exit.push_back(carriage_impasse.front());
                carriage_impasse.pop_back();
                ImpasseOut(carriage_impasse, k_imp);
                EntranceIn(carriage_entrance, k_entr);
                carriage_entrance.pop_back();
                EntranceOut(carriage_entrance, k_entr);
                Exit(carriage_exit, k_exit);
                break;
                        
//  -------- Перевозка вагона из входа на выход (мимо тупика) ---------
                        
            case 2:
                carriage_exit.push_back(carriage_entrance[carriage_entrance.size() - 1]);
                carriage_entrance.pop_back();
                EntranceOut(carriage_entrance, k_entr);
                Exit(carriage_exit, k_exit);
                break;
                
//  -------------- Перевозка вагона из входа в тупик -------------------
                
            case 3:
                carriage_impasse.push_back(carriage_entrance[carriage_entrance.size() - 1]);
                carriage_entrance.pop_back();
                EntranceOut(carriage_entrance, k_entr);
                ImpasseIn(carriage_impasse, k_imp);
                break;
                
            default:
                break;
        }
    }
    
//  ----------------------------- Конец --------------------------------
    
    system("pause");
    return 0;
}
// Классная задача, пришлось посидеть подумать как реализовать демонстрацию происходящего.
