import re


# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-build-configurations/
FLAGS_PER_BUILD_CONFIGURATION: dict[str, list[str]] = \
    {'Debug': ['ggdb'],
     'Release': ['O2', 'DNDEBUG']}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-choosing-a-language-standard/
LANGUAGE_STANDARDS: list[str] = ['0x', '1y', '1z',  '2a', '2b']

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

def get_build_configuration_flags(user_chosen_build_configuration: str) -> list[str]:

    flags: list[str] = FLAGS_PER_BUILD_CONFIGURATION[user_chosen_build_configuration]

    return flags


def get_language_standard_flag(user_specified_language_standard: str) -> list[str]:

    flags: list[str] = [f'std=c++{LANGUAGE_STANDARDS[int((int(re.fullmatch(r'C\++ 20(\d\d)', user_specified_language_standard).groups()[0]) - 11)/3)]:s}']

    return flags


def get_miscellaneous_flags(user_chosen_misc_decisions: str | list[str]) -> list[str]:

    flags: list[str] = [flag for decision, flag in FLAG_PER_MISCELLANEOUS_DECISION.items() if decision in user_chosen_misc_decisions]  # noqa: E501

    return flags


def get_warning_flags(user_chosen_warnings: str | list[str]) -> list[str]:

    flags: list[str] = [f'W{flag:s}' for warning, flag in FLAG_PER_WARNING.items() if warning in user_chosen_warnings]

    return flags


def get_dynamic_library_creation_flags(user_chosen_build_configuration: str) -> list[str]:

    flags = ['shared']

    if user_chosen_build_configuration == 'Release':
        flags.append('s')

    return flags
