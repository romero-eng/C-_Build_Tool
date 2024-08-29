#include "Arithmetic.hpp"

int Arithmetic::subtract(int x, int y)
{
    return x - y;
}

double Arithmetic::subtract(double x, double y)
{
    return x - y;
}

double Arithmetic::subtract(double x, int y)
{
    return Arithmetic::subtract(x, (double) y);
}

double Arithmetic::subtract(int x, double y)
{
    return Arithmetic::subtract((double) x, y);
}
