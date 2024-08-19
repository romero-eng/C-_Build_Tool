import subprocess

import flags


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

    build_configuration_flags: str = flags.get_build_configuration_flags('Debug')
    language_standard_flags: str = flags.get_language_standard_flag('C++ 2020')
    miscellaneous_flags:str = flags.get_miscellaneous_flags('Disable Compiler Extensions')
    warning_flags: str = \
        flags.get_compiler_warning_flags(['Treat warnings as errors',
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
