#include "Multiply.h"

int multiply(int x, int y)
{
    return x * y;
}

double multiply(double x, double y)
{
    return x * y;
}

double multiply(double x, int y)
{
    return multiply(x, (double) y);
}

double multiply(int x, double y)
{
    return multiply((double) x, y);
}
