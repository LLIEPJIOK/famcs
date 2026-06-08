#include <iomanip>
#include <iostream>
#include <string>
#include <sstream>
#include <unordered_map>
#include <Windows.h>

// Функция преобразования числа в символ в шестнадцатеричном формате
char to_hex(int numb) {
    if (numb <= 9) {
        return '0' + numb;
    }
    return 'A' + numb - 10;
}

// Функция для замены символа, если он не может быть отображен
wchar_t safe_char(wchar_t ch) {
    if (ch < 0x20 || (ch > 0x7E && ch < 0xA0) || (ch > 0xFF)) {
        return L'?'; // Заменяем символ на вопросительный знак
    }
    return ch;
}

int main() {
    // Настройка консоли для использования UTF-8
    SetConsoleOutputCP(CP_UTF8);
    
    std::unordered_map<int, std::wstring> mp = {
        {0, L" "},
        {7, L"•"},
        {8, L"◘"},
        {9, L"○"},
        {10, L"◙"},
        {13, L"♪"},
        {27, L"←"}
    };

    // Используем std::wcout для поддержки Unicode
    for (int i = 0; i < 16; i++) {
        for (int j = 0; j < 16; j++) {
            int cur = i * 16 + j;
            if (mp.count(cur)) {
                std::wcout << safe_char(mp[cur][0]);
            } else {
                std::wcout << safe_char(wchar_t(cur));
            }
            std::wcout << L"-0x" << to_hex(i) << to_hex(j) << L" ";
        }
        std::wcout << L"\n";
    }
}
