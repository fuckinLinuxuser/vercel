#include <iostream>
#include <string>

int main() {
    double a, b;
    char op;
    std::string res = "Результат";

    std::cout <<"Введите первое число: ";
    std::cin >> a;
            
    std::cout <<"Введите второе число: ";
    std::cin >> b;
    
    std::cout <<"Введите оператор: ";
    std::cin >> op;
    
    if (op == '+') {
        std::cout << a + b << std::endl;
    } else if (op == '-') {
        std::cout << a - b << std::endl;
    } else if (op == '*') {
        std::cout << a * b << std::endl;
    } else if (op == '/') {
        std::cout << a / b << std::endl;
    return 0;
    }
}