#include "Math.h"
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is " << add<int>(3, 4) << '\n';
    std::cout << "The sum of 3 and 4.1 is " << add<double>(3, 4.1) << '\n';
    std::cout << "The sum of 3.1 and 4 is " << add<double>(3.1, 4) << '\n';
    std::cout << "The sum of 3.1 and 4.0 is " << add<double>(3.1, 4.0) << '\n';
    std::cout << "The subtraction of 3 and 4 is " << subtract<int>(3, 4) << '\n';
    std::cout << "The subtraction of 3 and 4.1 is " << subtract<double>(3, 4.1) << '\n';
    std::cout << "The subtraction of 3.1 and 4 is " << subtract<double>(3.1, 4) << '\n';
    std::cout << "The subtraction of 3.1 and 4.0 is " << subtract<double>(3.1, 4.0) << '\n';
    std::cout << "The multiplication of 3 and 4 is " << multiply<int>(3, 4) << '\n';
    std::cout << "The multiplication of 3 and 4.1 is " << multiply<double>(3, 4.1) << '\n';
    std::cout << "The multiplication of 3.1 and 4 is " << multiply<double>(3.1, 4) << '\n';
    std::cout << "The multiplication of 3.1 and 4.0 is " << multiply<double>(3.1, 4.0) << '\n';
    return 0;
}
