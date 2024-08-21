#include "Add.h"

int Math::add(int x, int y)
{
    return x + y;
}

double Math::add(double x, double y)
{
    return x + y;
}

double Math::add(double x, int y)
{
    return add(x, (double) y);
}

double Math::add(int x, double y)
{
    return add((double) x, y);
}
