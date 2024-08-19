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


def _print_flag_statuses(title: str,
                         known_flag_descriptions: list[str],
                         chosen_descriptions: list[str]) -> None:

    max_description_length: str = max([len(description) for description in known_flag_descriptions])
    print(f'\n{title:s}\n{'':{'-':s}>{len(title) + 1:d}s}\n{'\n'.join([f'{description:>{max_description_length:d}s}: {'ON' if description in chosen_descriptions else 'OFF':s}' for description in known_flag_descriptions]):s}\n')


def _print_chosen_flag(flag_choice: str,
                      chosen_flag_description: str) -> None:

    print(f'\n{flag_choice:s}: {chosen_flag_description:s}')


def get_build_configuration_flags(user_chosen_build_configuration: str) -> str:

    if user_chosen_build_configuration not in FLAGS_PER_BUILD_CONFIGURATION:
        raise ValueError(f"The following build configuration is not recognized: {user_chosen_build_configuration:s}")

    _print_chosen_flag('Build', user_chosen_build_configuration)

    return ' '.join([f'-{flag:s}' for flag in FLAGS_PER_BUILD_CONFIGURATION[user_chosen_build_configuration]])


def get_language_standard_flag(user_specified_language_standard: str) -> str:

    matched_standard: re.Match = re.fullmatch(r'C\++ 20(\d\d)', user_specified_language_standard)
    
    standard_recognized: bool = False
    if matched_standard:
        two_digit_year: int = int(matched_standard.groups()[0])
        if two_digit_year - 11 >= 0:
            if (two_digit_year - 11) % 3 == 0:
                language_standard_flag: str = LANGUAGE_STANDARDS[int((two_digit_year - 11)/3)]
                standard_recognized = True

    if not standard_recognized:
        raise ValueError(f'The following Language Standard is not recognized: {user_specified_language_standard:s}')

    _print_chosen_flag('Language Standard', user_specified_language_standard)

    return f'-std=c++{language_standard_flag:s}'


def get_miscellaneous_flags(user_chosen_misc_decisions: str | list[str]) -> str:

    if isinstance(user_chosen_misc_decisions, str):

        if user_chosen_misc_decisions not in FLAG_PER_MISCELLANEOUS_DECISION:
            raise ValueError(f'The following miscellanous decision is not recognized: {user_chosen_misc_decisions:s}')

        user_chosen_misc_decisions = [user_chosen_misc_decisions]

    else:

        for decision in user_chosen_misc_decisions:
            if decision not in FLAG_PER_MISCELLANEOUS_DECISION:
                raise ValueError(f'The following miscellanous decision is not recognized: {decision:s}')

    _print_flag_statuses('Miscellaneous',
                         list(FLAG_PER_MISCELLANEOUS_DECISION.keys()),
                         user_chosen_misc_decisions)

    return ' '.join([f'-{flag:s}' for decision, flag in FLAG_PER_MISCELLANEOUS_DECISION.items() if decision in user_chosen_misc_decisions])


def get_compiler_warning_flags(user_chosen_warnings: str | list[str] = []) -> str:

    for warning in user_chosen_warnings:
        if warning not in FLAG_PER_WARNING:
            raise ValueError(f'The following warning is not recognized: {warning:s}')

    if isinstance(user_chosen_warnings, str):
        user_chosen_warnings = [user_chosen_warnings]

    _print_flag_statuses('Warnings',
                         list(FLAG_PER_WARNING.keys()),
                         user_chosen_warnings)

    return ' '.join([f'-W{flag:s}' for warning, flag in FLAG_PER_WARNING.items() if warning in user_chosen_warnings])
