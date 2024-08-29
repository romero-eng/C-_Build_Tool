#include "Arithmetic.hpp"

int Arithmetic::multiply(int x, int y)
{
    return x * y;
}

double Arithmetic::multiply(double x, double y)
{
    return x * y;
}

double Arithmetic::multiply(double x, int y)
{
    return Arithmetic::multiply(x, (double) y);
}

double Arithmetic::multiply(int x, double y)
{
    return Arithmetic::multiply((double) x, y);
}
