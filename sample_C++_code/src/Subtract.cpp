#include "Subtract.h"

int subtract(int x, int y)
{
    return x - y;
}

double subtract(double x, double y)
{
    return x - y;
}

double subtract(double x, int y)
{
    return subtract(x, (double) y);
}

double subtract(int x, double y)
{
    return subtract((double) x, y);
}
