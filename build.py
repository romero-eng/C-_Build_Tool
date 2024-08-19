import os
import subprocess

from flags import Flags


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


def generate_object_files(source_file_paths: list[str],
                          object_file_paths: list[str],
                          build_configuration: str,
                          language_standard: str,
                          miscellaneous: str,
                          warnings: list[str]) -> bool:

    compile_command: str = 'g++ -c {{source_file_path:s}} -o {{object_file_path:s}} {build_configuration:s} {language_standard:s} {warnings:s} {miscellaneous:s}'

    compile_command_with_flags: str = \
        compile_command.format(build_configuration=Flags.get_build_configuration_flags(build_configuration),
                                 language_standard=Flags.get_language_standard_flag(language_standard),
                                          warnings=Flags.get_compiler_warning_flags(warnings),
                                     miscellaneous=Flags.get_miscellaneous_flags(miscellaneous))

    success: bool = True

    for source_file_path, object_file_path in zip(source_file_paths, object_file_paths):

        success = \
            run_command(f'"{os.path.splitext(os.path.basename(source_file_path))[0]:s}" Compilation Results',
                        compile_command_with_flags.format(source_file_path=source_file_path,
                                                          object_file_path=object_file_path))

        if not success:
            break

    return success


def link_object_files_into_executable(executable_path: str,
                                      object_file_paths: list[str]):

    link_command: str = 'g++ -o {executable}.exe {object_files:s}'

    if success:
        run_command('Linking Results',
                    link_command.format(executable=executable_path,
                                        object_files=' '.join(object_file_paths)))


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
        generate_object_files([os.path.join('src', f'{file:s}.cpp') for file in cpp_files],
                              [os.path.join('build', f'{file:s}.o') for file in cpp_files],
                              build_configuration,
                              language_standard,
                              miscellaneous,
                              warnings)

    if success:
        link_object_files_into_executable(os.path.join('build', executable_name),
                                          [os.path.join('build', f'{file:s}.o') for file in cpp_files])
