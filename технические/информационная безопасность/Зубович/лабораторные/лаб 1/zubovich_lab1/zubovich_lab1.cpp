#include <iostream>
#include <string>
#include <unordered_map>

char to_hex(int numb) {
    if (numb <= 9) {
        return '0' + numb;
    }

    return 'A' + numb - 10;
}

int main()
{
    std::unordered_map<int, std::string> mp = {
      {0, " "},
      {7, "•"},
      {8, "◘"},
      {9, "○"},
      {10, "◙"},
      {13, "♪"},
      {27, "←"}
    };
    for (int i = 0; i < 16; i++) {
        for (int j = 0; j < 16; j++) {
            int cur = i * 16 + j;
            if (mp.count(cur)) {
                std::cout << mp[cur];
            }
            else {
                std::cout << char(cur);
            }

            std::cout << "-0x" << to_hex(i) << to_hex(j) << " ";
        }
        std::cout << "\n";
    }
}
