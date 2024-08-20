#include "Subtract.h"

int Math::subtract(int x, int y)
{
    return x - y;
}

double Math::subtract(double x, double y)
{
    return x - y;
}

double Math::subtract(double x, int y)
{
    return subtract(x, (double) y);
}

double Math::subtract(int x, double y)
{
    return subtract((double) x, y);
}
