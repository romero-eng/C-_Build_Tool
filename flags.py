

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


def _print_flag_statuses(title: str,
                         known_flag_descriptions: list[str],
                         chosen_descriptions: list[str]) -> None:

    max_description_length: str = max([len(description) for description in known_flag_descriptions])
    print(f'\n{title:s}\n{'':{'-':s}>{len(title) + 1:d}s}\n{'\n'.join([f'{description:>{max_description_length:d}s}: {'ON' if description in chosen_descriptions else 'OFF':s}' for description in known_flag_descriptions]):s}\n')


def _print_chosen_flag(flag_choice: str,
                      chosen_flag_description: str) -> None:

    print(f'\n{flag_choice:s}: {chosen_flag_description:s}')


def get_build_configuration_flags(user_chosen_build_configuration: str) -> str:

    _print_chosen_flag('Build', user_chosen_build_configuration)

    return ' '.join([f'-{flag:s}' for flag in FLAGS_PER_BUILD_CONFIGURATION[user_chosen_build_configuration]])


def get_language_standard_flag(language_standard: str = 'C++ 2017') -> str:

    _print_chosen_flag('Language Standard', language_standard)

    return f'-std=c++{LANGUAGE_STANDARDS[int((int(language_standard.split('C++ ')[1]) - 2011)/3)]:s}'


def get_miscellaneous_flags(user_chosen_misc_decisions: str | list[str]) -> str:

    if isinstance(user_chosen_misc_decisions, str):
        user_chosen_misc_decisions = [user_chosen_misc_decisions]

    _print_flag_statuses('Miscellaneous',
                         list(FLAG_PER_MISCELLANEOUS_DECISION.keys()),
                         user_chosen_misc_decisions)

    return ' '.join([f'-{flag:s}' for misc_decision, flag in FLAG_PER_MISCELLANEOUS_DECISION.items() if misc_decision in user_chosen_misc_decisions])


def get_compiler_warning_flags(user_chosen_warnings: str | list[str] = []) -> str:

    if isinstance(user_chosen_warnings, str):
        user_chosen_warnings = [user_chosen_warnings]

    _print_flag_statuses('Warnings',
                         list(FLAG_PER_WARNING.keys()),
                         user_chosen_warnings)

    return ' '.join([f'-W{flag:s}' for warning, flag in FLAG_PER_WARNING.items() if warning in user_chosen_warnings])
