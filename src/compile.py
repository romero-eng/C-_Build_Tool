import os
from typing import Optional

import flags
from command import run_command


def generate_object_files(source_file_paths: list[str],
                          object_file_paths: list[str],
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

    for source_file_path, object_file_path in zip(source_file_paths, object_file_paths):

        success = \
            run_command(f'"{os.path.splitext(os.path.basename(source_file_path))[0]:s}" Compilation Results',
                        compile_command_with_flags.format(source_file_path=source_file_path,
                                                          object_file_path=object_file_path))

        if not success:
            break

    return success


def link_object_files_into_executable(executable_path: str,
                                      object_file_paths: list[str]) -> None:

    link_command: str = 'g++ -o {executable} {object_files:s}'

    run_command('Linking Results',
                link_command.format(executable=executable_path,
                                    object_files=' '.join(object_file_paths)))


def build_executable_from_source(source_file_paths: list[str],
                                 object_file_paths: list[str],
                                 executable_path: str,
                                 build_configuration: Optional[str] = None,
                                 language_standard: Optional[str] = None,
                                 miscellaneous: Optional[str] = None,
                                 warnings: Optional[list[str]] = None) -> None:

    success: bool = \
        generate_object_files(source_file_paths,
                              object_file_paths,
                              build_configuration,
                              language_standard,
                              miscellaneous,
                              warnings)

    if success:
        link_object_files_into_executable(executable_path,
                                          object_file_paths)
