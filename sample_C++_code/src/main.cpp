#include "Add.h"
#include "Subtract.h"
#include "Multiply.h"
#include "Divide.h"
#include <iostream>

int main()
{
    std::cout << Math::add(3, 4) << '\n';
    std::cout << Math::add(3, 4.1) << '\n';
    std::cout << Math::add(3.1, 4) << '\n';
    std::cout << Math::add(3.1, 4.0) << '\n';
    std::cout << Math::subtract(3, 4) << '\n';
    std::cout << Math::subtract(3, 4.1) << '\n';
    std::cout << Math::subtract(3.1, 4) << '\n';
    std::cout << Math::subtract(3.1, 4.0) << '\n';
    std::cout << Math::multiply(3, 4) << '\n';
    std::cout << Math::multiply(3, 4.1) << '\n';
    std::cout << Math::multiply(3.1, 4) << '\n';
    std::cout << Math::multiply(3.1, 4.0) << '\n';
    std::cout << Math::divide(3, 4.1) << '\n';
    std::cout << Math::divide(3.1, 4) << '\n';
    std::cout << Math::divide(3.1, 4.0) << '\n';
    return 0;
}
