#include <iostream>
using namespace std;

int main() {
    setlocale(LC_ALL, "ru");
    int a, b, count = 0;

    cout << "введите длину стороны a: ";
    cin >> a;

    cout << "введите длину стороны b: ";
    cin >> b;

    __asm {
        mov eax, a
        mov ebx, b
        xor ecx, ecx
        loop_start :
        cmp eax, 0
            jle end_loop
            cmp ebx, 0
            jle end_loop
            cmp eax, ebx
            jge a_greater
            idiv ebx
            add ecx, eax
            imul eax, ebx
            sub ebx, eax
            jmp loop_start
            a_greater :
        xchg eax, ebx
            idiv ebx
            add ecx, eax
            imul eax, ebx
            sub ebx, eax
            jmp loop_start
            end_loop :
        mov count, ecx
    }


    cout << "количество полученных квадратов: " << count << endl;

    return 0;
}