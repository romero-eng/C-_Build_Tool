#include "Add.h"

int add(int x, int y)
{
    return x + y;
}

double add(double x, double y)
{
    return x + y;
}

double add(double x, int y)
{
    return add(x, (double) y);
}

double add(int x, double y)
{
    return add((double) x, y);
}
