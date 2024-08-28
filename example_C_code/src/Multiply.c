#include "Arithmetic.h"

int Arithmetic_multiply_int_int(int x, int y)
{
    return x * y;
}

double Arithmetic_multiply_double_double(double x, double y)
{
    return x * y;
}

double Arithmetic_multiply_double_int(double x, int y)
{
    return Arithmetic_multiply_double_double(x, (double) y);
}

double Arithmetic_multiply_int_double(int x, double y)
{
    return Arithmetic_multiply_double_double((double) x, y);
}
