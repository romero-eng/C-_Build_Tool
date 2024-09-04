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

namespace Arithmetic
{
    IMPORT_OR_EXPORT int add(int x, int y);

    IMPORT_OR_EXPORT double add(double x, double y);

    IMPORT_OR_EXPORT double add(double x, int y);

    IMPORT_OR_EXPORT double add(int x, double y);

    IMPORT_OR_EXPORT int subtract(int x, int y);

    IMPORT_OR_EXPORT double subtract(double x, double y);

    IMPORT_OR_EXPORT double subtract(double x, int y);

    IMPORT_OR_EXPORT double subtract(int x, double y);

    IMPORT_OR_EXPORT int multiply(int x, int y);

    IMPORT_OR_EXPORT double multiply(double x, double y);

    IMPORT_OR_EXPORT double multiply(double x, int y);

    IMPORT_OR_EXPORT double multiply(int x, double y);

    IMPORT_OR_EXPORT double divide(double x, double y);

    IMPORT_OR_EXPORT double divide(double x, int y);

    IMPORT_OR_EXPORT double divide(int x, double y);
}

#endif
