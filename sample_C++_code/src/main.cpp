#include "Math.h"
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is " << add<int>(3, 4) << '\n';
    std::cout << "The sum of 3 and 4 is " << add<double>(3, 4.1) << '\n';
    return 0;
}
