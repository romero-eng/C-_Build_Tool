#ifndef ARITHMETIC_H
#define ARITHMETIC_H

#ifdef _WIN32
  #ifdef ACTIVATE_ARITHMETIC_LIBRARY_DYNAMIC_LINKING
    #ifdef EXPORT_AS_DLL
      #define IMPORT_OR_EXPORT __declspec(dllexport)
    #else
      #define IMPORT_OR_EXPORT __declspec(dllimport)
    #endif
  #else
    #define IMPORT_OR_EXPORT
  #endif
#else
  #define IMPORT_OR_EXPORT
#endif

#ifdef __cplusplus
extern "C"
{
#endif

IMPORT_OR_EXPORT double add(double x, double y);

IMPORT_OR_EXPORT double subtract(double x, double y);

IMPORT_OR_EXPORT double multiply(double x, double y);

IMPORT_OR_EXPORT double divide(double x, double y);

#ifdef __cplusplus
}
#endif

#endif
