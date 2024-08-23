#include "Arithmetic.h"
#include <iostream>

int main()
{
    std::cout << Arithmetic::add(3, 4) << '\n';
    std::cout << Arithmetic::add(3, 4.1) << '\n';
    std::cout << Arithmetic::add(3.1, 4) << '\n';
    std::cout << Arithmetic::add(3.1, 4.0) << '\n';
    std::cout << Arithmetic::subtract(3, 4) << '\n';
    std::cout << Arithmetic::subtract(3, 4.1) << '\n';
    std::cout << Arithmetic::subtract(3.1, 4) << '\n';
    std::cout << Arithmetic::subtract(3.1, 4.0) << '\n';
    std::cout << Arithmetic::multiply(3, 4) << '\n';
    std::cout << Arithmetic::multiply(3, 4.1) << '\n';
    std::cout << Arithmetic::multiply(3.1, 4) << '\n';
    std::cout << Arithmetic::multiply(3.1, 4.0) << '\n';
    std::cout << Arithmetic::divide(3, 4.1) << '\n';
    std::cout << Arithmetic::divide(3.1, 4) << '\n';
    std::cout << Arithmetic::divide(3.1, 4.0) << '\n';
    return 0;
}
