import os
import subprocess
from typing import Optional

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


def generate_object_files(build_configuration: str,
                          language_standard: str,
                          miscellaneous: str,
                          warnings: list[str],
                          source_dir: Optional[str] = None,
                          build_dir: Optional[str] = None) -> bool:

    compile_command: str = 'g++ -c {{source_file_path:s}}.cpp -o {{object_file_path:s}}.o {build_configuration:s} {language_standard:s} {warnings:s} {miscellaneous:s}'

    compile_command_with_flags: str = \
        compile_command.format(build_configuration=flags.get_build_configuration_flags(build_configuration),
                               language_standard=flags.get_language_standard_flag(language_standard),
                               warnings=flags.get_compiler_warning_flags(warnings),
                               miscellaneous=flags.get_miscellaneous_flags(miscellaneous))

    success: bool = True

    for file in cpp_files:

        success = \
            run_command(f'{file:s}.cpp Compilation Results',
                        compile_command_with_flags.format(source_file_path=os.path.join(source_dir, file) if source_dir else file,
                                                          object_file_path=os.path.join( build_dir, file) if  build_dir else file))

        if not success:
            break

    return success


def link_object_files_into_executable(executable_name: str,
                                      object_file_names: list[str],
                                      build_dir: Optional[str] = None):

    link_command: str = 'g++ -o {executable}.exe {object_files:s}'

    if success:
        run_command('Linking Results',
                    link_command.format(executable=os.path.join(build_dir, f'{executable_name:s}.o') if build_dir else executable_name,
                                        object_files=' '.join([os.path.join(build_dir, f'{file_name:s}.o') if build_dir else f'{file_name:s}.o' for file_name in object_file_names])))


if (__name__=='__main__'):

    executable_name = 'present_addition'
    cpp_files = ['main', 'Add']

    build_configuration: str = 'Debug'
    language_standard: str = 'C++ 2020'
    miscellaneous: str = 'Disable Compiler Extensions'
    warnings: list[str] = \
        ['Treat warnings as errors',
          'Avoid a lot of questionable coding practices',
          'Avoid even more questionable coding practices',
          'Follow Effective C++ Style Guidelines',
          'Avoid potentially value-changing implicit conversions',
          'Avoid potentially sign-changing implicit conversions for integers']

    if not os.path.exists('build'):
        os.mkdir('build')

    success = \
        generate_object_files(build_configuration,
                              language_standard,
                              miscellaneous,
                              warnings,
                              'src',
                              'build')

    if success:
        link_object_files_into_executable(executable_name,
                                          cpp_files,
                                          'build')
