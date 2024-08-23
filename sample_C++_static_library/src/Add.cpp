#include "Arithmetic.h"

int Arithmetic::add(int x, int y)
{
    return x + y;
}

double Arithmetic::add(double x, double y)
{
    return x + y;
}

double Arithmetic::add(double x, int y)
{
    return Arithmetic::add(x, (double) y);
}

double Arithmetic::add(int x, double y)
{
    return Arithmetic::add((double) x, y);
}
