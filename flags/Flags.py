

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-build-configurations/
BUILD_CONFIGURATIONS: dict[str, list[str]] = \
    {'Debug': ['ggdb'],
     'Release': ['O2', 'DNDEBUG']}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-choosing-a-language-standard/
LANGUAGE_STANDARDS: list[str] = ['0x', '1y', '1z',  '2a', '2b']

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-compiler-extensions/
MISCELLANEOUS: dict[str, str] = \
    {'Disable Compiler Extensions': 'pedantic-errors'}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-warning-and-error-levels/
# https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#Warning-Options
# https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html
WARNING_DECISIONS: dict[str, str] = \
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


def get_build_configuration_flags(build: str) -> str:

    _print_chosen_flag('Build',
                       build)

    return ' '.join([f'-{flag:s}' for flag in BUILD_CONFIGURATIONS[build]])


def get_language_standard_flag(language_standard: str = 'C++ 2017') -> str:

    _print_chosen_flag('Language Standard',
                       language_standard)

    return f'-std=c++{LANGUAGE_STANDARDS[int((int(language_standard.split('C++ ')[1]) - 2011)/3)]:s}'


def get_miscellaneous_flags(make_decisions: str | list[str]) -> str:

    if isinstance(make_decisions, str):
        make_decisions = [make_decisions]

    _print_flag_statuses('Miscellaneous',
                         list(MISCELLANEOUS.keys()),
                         make_decisions)

    return ' '.join([f'-{flag:s}' for decision, flag in MISCELLANEOUS.items() if decision in make_decisions])


def get_compiler_warning_flags(turn_on_warnings: str | list[str] = []) -> str:

    if isinstance(turn_on_warnings, str):
        turn_on_warnings = [turn_on_warnings]

    _print_flag_statuses('Warnings',
                         list(WARNING_DECISIONS.keys()),
                         turn_on_warnings)

    return ' '.join([f'-W{flag:s}' for warning, flag in WARNING_DECISIONS.items() if warning in turn_on_warnings])
