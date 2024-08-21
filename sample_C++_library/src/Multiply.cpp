#include "Multiply.h"

int Math::multiply(int x, int y)
{
    return x * y;
}

double Math::multiply(double x, double y)
{
    return x * y;
}

double Math::multiply(double x, int y)
{
    return multiply(x, (double) y);
}

double Math::multiply(int x, double y)
{
    return multiply((double) x, y);
}
