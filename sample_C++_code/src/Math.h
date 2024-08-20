#ifndef MATH_H
#define MATH_H

#include <type_traits>

template<typename N>
concept IsSignedIntegral = std::is_integral<N>::value && std::is_signed<N>::value;

template<typename N>
concept IsFloatingPoint = std::is_floating_point<N>::value;

template<typename N>
concept IsANumber = IsSignedIntegral<N> || IsFloatingPoint<N>;

template<IsANumber return_N, IsANumber first_N, IsANumber second_N>
return_N add(first_N x, second_N y)
{
    return x + y;
}

#endif
