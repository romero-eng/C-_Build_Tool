#include "Arithmetic.hpp"


double Arithmetic::divide(double x, double y)
{
    return x / y;
}

double Arithmetic::divide(double x, int y)
{
    return Arithmetic::divide(x, (double) y);
}

double Arithmetic::divide(int x, double y)
{
    return Arithmetic::divide((double) x, y);
}
