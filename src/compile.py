import os
from typing import Optional

import flags
from command import run_command


def generate_object_files(source_directory: str,
                          build_directory: str,
                          relative_source_file_paths: list[str],
                          relative_object_file_build_paths: list[str],
                          build_configuration: Optional[str] = None,
                          language_standard: Optional[str] = None,
                          miscellaneous: Optional[str] = None,
                          warnings: Optional[list[str]] = None) -> bool:

    compile_command: str = 'g++ -c {{source_file_path:s}} -o {{object_file_path:s}}{build_configuration:s}{language_standard:s}{warnings:s}{miscellaneous:s}'  # noqa: E501

    compile_command_with_flags: str = \
        compile_command.format(build_configuration=flags.get_build_configuration_flags(build_configuration),
                                 language_standard=flags.get_language_standard_flag(language_standard),         # noqa: E127, E501
                                          warnings=flags.get_compiler_warning_flags(warnings),                  # noqa: E127, E501
                                     miscellaneous=flags.get_miscellaneous_flags(miscellaneous))                # noqa: E127, E501

    success: bool = True
    common_directory: str = \
        os.path.commonpath([source_directory,
                            build_directory])
    relative_source_directory: str = source_directory.split(f'{common_directory:s}{os.sep:s}')[1]
    relative_build_directory: str = build_directory.split(f'{common_directory:s}{os.sep:s}')[1]

    for relative_source_file_path, relative_object_file_path in zip(relative_source_file_paths, relative_object_file_build_paths):

        success = \
            run_command(f'"{os.path.splitext(os.path.basename(relative_source_file_path))[0]:s}" Compilation Results',
                        compile_command_with_flags.format(source_file_path=os.path.join(relative_source_directory, relative_source_file_path),
                                                          object_file_path=os.path.join( relative_build_directory, relative_object_file_path)),
                        common_directory)

        if not success:
            break

    return success


def link_object_files_into_executable(build_directory: str,
                                      executable_name: str,
                                      relative_object_file_build_paths: list[str]) -> None:

    link_command: str = 'g++ -o {executable} {object_files:s}'

    run_command('Linking Results',
                link_command.format(executable=f'{executable_name:s}.exe',
                                    object_files=' '.join(relative_object_file_build_paths)),
                build_directory)


def build_executable_from_source(source_directory: str,
                                 build_directory: str, 
                                 relative_source_file_paths: list[str],
                                 relative_object_file_build_paths: list[str],
                                 executable_name: str,
                                 build_configuration: Optional[str] = None,
                                 language_standard: Optional[str] = None,
                                 miscellaneous: Optional[str] = None,
                                 warnings: Optional[list[str]] = None) -> None:

    success: bool = \
        generate_object_files(source_directory,
                              build_directory,
                              relative_source_file_paths,
                              relative_object_file_build_paths,
                              build_configuration,
                              language_standard,
                              miscellaneous,
                              warnings)

    if success:
        link_object_files_into_executable(build_directory,
                                          executable_name,
                                          relative_object_file_build_paths)


def test_executable(build_directory: str,
                    executable_name: str) -> None:

    if os.path.exists(os.path.join(os.path.join(build_directory, f'{executable_name:s}.exe'))):
        _ = \
            run_command('Testing Executable',
                        f'{executable_name:s}.exe',
                        build_directory)
