#include "Arithmetic.h"


double Arithmetic_divide_double_double(double x, double y)
{
    return x / y;
}

double Arithmetic_divide_double_int(double x, int y)
{
    return Arithmetic_divide_double_double(x, (double) y);
}

double Arithmetic_divide_int_double(int x, double y)
{
    return Arithmetic_divide_double_double((double) x, y);
}
