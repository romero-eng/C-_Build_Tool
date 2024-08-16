import subprocess

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-build-configurations/
BUILD_CONFIGURATIONS: dict[str, list[str]] = \
    {'Debug': ['ggdb'],
     'Release': ['O2', 'DNDEBUG']}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-choosing-a-language-standard/
C_PLUS_PLUS_LANGUAGE_STANDARDS: dict[str, str] = \
    {'C++ 2011': '0x',
     'C++ 2014': '1y',
     'C++ 2017': '1z',
     'C++ 2020': '2a',
     'C++ 2023': '2b'}

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


def get_build_configuration_flags(build: str) -> str:

    print(f'Build: {build:s}')

    return ''.join([f'-{flag:s}' for flag in BUILD_CONFIGURATIONS[build]])


def get_language_standard_flag(language_standard: str = 'C++ 2017') -> str:

    print(f'\nLanguage Standard: {language_standard:s}\n')

    return f'-std=c++{C_PLUS_PLUS_LANGUAGE_STANDARDS[language_standard]:s}'


def get_miscellaneous_flags(make_decisions: str | list[str]) -> str:

    if isinstance(make_decisions, str):
        make_decisions = [make_decisions]

    title: str = 'Miscellaneous'
    max_decision_length = max([len(decision) for decision in list(MISCELLANEOUS.keys())])
    print(f'\n{title:s}:\n{'':{'-':s}>{len(title) + 1:d}s}\n{'\n'.join([f'{decision:>{max_decision_length:d}s}: {'ON' if decision in make_decisions else 'OFF':s}' for decision in MISCELLANEOUS.keys()]):s}\n')

    return ' '.join([f'-{flag:s}' for decision, flag in MISCELLANEOUS.items() if decision in make_decisions])


def get_compiler_warning_flags(turn_on_warnings: str | list[str] = []) -> str:

    if isinstance(turn_on_warnings, str):
        turn_on_warnings = [turn_on_warnings]

    title: str = 'Warnings'
    max_warning_length = max([len(warning) for warning in list(WARNING_DECISIONS.keys())])
    print(f'\n{title:s}:\n{'':{'-':s}>{len(title) + 1:d}s}\n{'\n'.join([f'{warning:>{max_warning_length:d}s}: {'ON' if warning in turn_on_warnings else 'OFF':s}' for warning in WARNING_DECISIONS.keys()]):s}\n')

    return ' '.join([f'-W{flag:s}' for warning, flag in WARNING_DECISIONS.items() if warning in turn_on_warnings])


def run_command(command_description: str,
                command: str,
                successful_return_code: int = 0) -> bool:

    results: subprocess.CompletedProcess = \
        subprocess.run(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    success: bool = results.returncode == successful_return_code

    formatted_results: list[str] = [f'\tCommand: {command:s}']
    formatted_results.append(f'\tCommand Results: {'Succesful' if success else 'Failure':s}')

    if results.stdout:
        formatted_results.append(f'\tOutput:\n\n{results.stdout.decode('utf-8'):s}')

    if results.stderr:
        formatted_results.append(f'\t Error:\n\n{results.stderr.decode('utf-8'):s}')

    print(f'\n{command_description:s}:\n{'':{'-':s}>{len(command_description) + 1:d}s}\n{'\n\n'.join(formatted_results):s}\n')

    return success


if (__name__=='__main__'):

    executable_name = 'present_addition'
    cpp_files = ['main', 'Add']

    compile_command: str = 'g++ -c {source_file}.cpp {build_configuration:s} {language_standard:s} {warnings:s} {miscellaneous:s}'
    link_command: str = 'g++ -o {executable}.exe {object_files:s}'

    build_configuration_flags: str = get_build_configuration_flags('Debug')
    language_standard_flags: str = get_language_standard_flag('C++ 2020')
    miscellaneous_flags:str = get_miscellaneous_flags('Disable Compiler Extensions')
    warning_flags: str = \
        get_compiler_warning_flags(['Treat warnings as errors',
                                    'Avoid a lot of questionable coding practices',
                                    'Avoid even more questionable coding practices',
                                    'Follow Effective C++ Style Guidelines',
                                    'Avoid potentially value-changing implicit conversions',
                                    'Avoid potentially sign-changing implicit conversions for integers'])

    for file in cpp_files:
        success = \
            run_command(f'{file:s}.cpp Compilation Results',
                        compile_command.format(source_file=file,
                                               executable=executable_name,
                                               build_configuration=build_configuration_flags,
                                               language_standard=language_standard_flags,
                                               warnings=warning_flags,
                                               miscellaneous=miscellaneous_flags))
        if not success:
            break

    if success:
        run_command('Linking Results',
                    link_command.format(executable=executable_name,
                                        object_files=' '.join([f'{file:s}.o' for file in cpp_files])))
