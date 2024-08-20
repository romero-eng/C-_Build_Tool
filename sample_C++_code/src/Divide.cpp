#include "Divide.h"


double Math::divide(double x, double y)
{
    return x / y;
}

double Math::divide(double x, int y)
{
    return divide(x, (double) y);
}

double Math::divide(int x, double y)
{
    return divide((double) x, y);
}
