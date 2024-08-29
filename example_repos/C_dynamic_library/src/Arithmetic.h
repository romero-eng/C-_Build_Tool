#ifndef ARITHMETIC_H
#define ARITHMETIC_H

#ifdef _WIN32
  #ifdef PREPARE_ARITHMETIC_LIBRARY_FOR_DLL_EXPORT
    #define ADDAPI __declspec(dllexport)
  #else
    #define ADDAPI __declspec(dllimport)
  #endif
#else
  #define ADDAPI
#endif

#ifdef __cplusplus
extern "C"
{
#endif

ADDAPI double add(double x, double y);

ADDAPI double subtract(double x, double y);

ADDAPI double multiply(double x, double y);

ADDAPI double divide(double x, double y);

#ifdef __cplusplus
}
#endif

#endif
