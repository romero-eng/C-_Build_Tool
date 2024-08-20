#include "Divide.h"


double divide(double x, double y)
{
    return x / y;
}

double divide(double x, int y)
{
    return divide(x, (double) y);
}

double divide(int x, double y)
{
    return divide((double) x, y);
}
