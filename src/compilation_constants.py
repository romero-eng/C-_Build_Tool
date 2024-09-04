
# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-build-configurations/
FLAGS_PER_BUILD_CONFIGURATION: dict[str, list[str]] = \
    {'Debug': ['ggdb'],
     'Release': ['O2', 'DNDEBUG']}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-choosing-a-language-standard/
C_PLUS_PLUS_LANGUAGE_STANDARDS: list[str] = ['0x', '1y', '1z',  '2a', '2b']
C_LANGUAGE_STANDARDS: list[int] = [1989, 1990, 1999, 2011, 2018]

C_PLUS_PLUS_SOURCE_CODE_EXTENSIONS: list[str] = ['.cc', '.cxx', '.cpp']
C_PLUS_PLUS_HEADER_EXTENSIONS: list[str] = ['.h', '.hpp']

C_SOURCE_CODE_EXTENSIONS: list[str] = ['.c']
C_HEADER_EXTENSIONS: list[str] = ['.h']

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-compiler-extensions/
FLAG_PER_MISCELLANEOUS_DECISION: dict[str, str] = \
    {'Disable Compiler Extensions': 'pedantic-errors'}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-warning-and-error-levels/
# https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#Warning-Options
# https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html
FLAG_PER_WARNING: dict[str, str] = \
    {'Treat warnings as errors': 'error',
     'Avoid a lot of questionable coding practices': 'all',
     'Avoid even more questionable coding practices': 'extra',
     'Follow Effective C++ Style Guidelines': 'effc++',
     'Avoid potentially value-changing implicit conversions': 'conversion',
     'Avoid potentially sign-changing implicit conversions for integers': 'sign-conversion'}
