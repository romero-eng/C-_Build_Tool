import os
import json
import shutil
import platform
from typing import Optional

import flags
from command import run_command


def copy_header_files_from_source_into_include(source_directory: str,
                                               include_directory: str) -> None:

    if not os.path.exists(include_directory):
        os.mkdir(include_directory)

    for root, dirs, files in os.walk(source_directory):
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)
        for file in files:
            if os.path.splitext(file)[1] == '.h':
                shutil.copyfile(os.path.join(source_directory, root.split(source_directory)[1], file),
                                os.path.join(include_directory, root.split(source_directory)[1], file))


def retrieve_compilation_settings(src_dir: str) -> tuple[Optional[str],
                                                         Optional[str],
                                                         Optional[str],
                                                         Optional[list[str]]]:

    settings_path: str = os.path.join(src_dir, 'compilation_settings.json')

    settings: dict[str, str | list[str]]

    if os.path.exists(src_dir):
        if os.path.isdir(src_dir):
            if not os.path.exists(settings_path):

                settings = \
                    {'Build': list(flags.FLAGS_PER_BUILD_CONFIGURATION.keys())[0],
                     'Language': f'C++ {2011 + 3*flags.LANGUAGE_STANDARDS.index('2a'):d}',
                     'Warnings': list(flags.FLAG_PER_WARNING.keys()),
                     'Miscellaneous': list(flags.FLAG_PER_MISCELLANEOUS_DECISION.keys())}

                with open(settings_path, 'w') as json_file:
                    json.dump(settings, json_file)

            else:
                with open(settings_path, 'r') as json_file:
                    settings = json.load(json_file)

    build_configuration: Optional[str] = settings['Build'] if 'Build' in settings else None
    language_standard: Optional[str] = settings['Language'] if 'Language' in settings else None
    miscellaneous: Optional[str] = settings['Miscellaneous'] if 'Miscellaneous' in settings else None
    warnings: Optional[list[str]] = settings['Warnings'] if 'Warnings' in settings else None

    return (build_configuration,
            language_standard,
            miscellaneous,
            warnings)


def generate_object_files(source_directory: str,
                          build_directory: str,
                          include_directories: Optional[list[str]] = None) -> bool:

    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    common_directory: str = os.path.commonpath([source_directory, build_directory])

    relative_source_directory: str = source_directory.split(f'{common_directory:s}{os.sep:s}')[1]
    relative_build_directory: str = build_directory.split(f'{common_directory:s}{os.sep:s}')[1]

    (build_configuration,
     language_standard,
     miscellaneous,
     warnings) = \
        retrieve_compilation_settings(source_directory)

    formatted_flags: list[str] = []
    if build_configuration:
        formatted_flags.append(' '.join([f'-{flag:s}' for flag in flags.get_build_configuration_flags(build_configuration)]))  # noqa: E501
    if language_standard:
        formatted_flags.append(' '.join([f'-{flag:s}' for flag in flags.get_language_standard_flag(language_standard)]))
    if warnings:
        formatted_flags.append(' '.join([f'-{flag:s}' for flag in flags.get_warning_flags(warnings)]))
    if miscellaneous:
        formatted_flags.append(' '.join([f'-{flag:s}' for flag in flags.get_miscellaneous_flags(miscellaneous)]))
    if include_directories:
        formatted_flags.append(' '.join([f'-{flag:s}' for flag in flags.get_include_directory_flags(include_directories)]))  # noqa: E501

    compile_command: str = 'g++ -c {{source_file_path:s}} -o {{object_file_path:s}} {flags:s}'
    compile_command = compile_command.format(flags=' '.join(formatted_flags))

    success: bool = True

    for root, _, files in os.walk(source_directory):
        for file in files:
            if os.path.splitext(file)[1] == '.cpp':

                success = \
                    run_command(f'"{os.path.splitext(file)[0]:s}" Compilation Results',
                                compile_command.format(source_file_path=os.path.join(relative_source_directory, root.split(source_directory)[1], file),  # noqa: E501
                                                       object_file_path=os.path.join(relative_build_directory, f'{os.path.splitext(file)[0]:s}.o')),     # noqa: E501
                                common_directory)

                if not success:
                    break

    return success


def link_object_files_into_executable(build_directory: str,
                                      executable_name: str,
                                      library_paths: Optional[list[str]] = None) -> None:

    formatted_flags: list[str] = []

    if library_paths:
        formatted_flags.append(' '.join([f'-{flag:s}' for flag in flags.get_library_flags(library_paths)]))

    link_command: str = 'g++ -o {{executable:s}} {{object_files:s}} {flags:s}'
    link_command = link_command.format(flags=' '.join(formatted_flags))

    run_command('Linking Results',
                link_command.format(executable=f'{executable_name:s}.exe',
                                    object_files=' '.join([file_path for file_path in os.listdir(build_directory) if os.path.splitext(file_path)[1] == '.o'])),  # noqa: E501
                build_directory)


def archive_object_files_into_static_library(library_name: str,
                                             build_directory: str,
                                             library_directory: str,
                                             other_library_paths: Optional[list[str]] = None) -> None:

    formatted_flags: list[str] = []

    if other_library_paths:
        formatted_flags.append(' '.join([f'-{flag:s}' for flag in flags.get_library_flags(other_library_paths)]))

    build_static_library_command: str = 'ar rcs {{library_path:s}} {{object_file_build_paths:s}} {flags:s}'
    build_static_library_command = build_static_library_command.format(flags=' '.join(formatted_flags))

    if not os.path.exists(library_directory):
        os.mkdir(library_directory)

    common_directory: str = \
        os.path.commonpath([build_directory,
                            library_directory])

    relative_build_directory: str = build_directory.split(f'{common_directory:s}{os.sep:s}')[1]
    relative_library_directory: str = library_directory.split(f'{common_directory:s}{os.sep:s}')[1]

    run_command('Archiving into Static Library',
                build_static_library_command.format(library_path=os.path.join(relative_library_directory,
                                                                              f'{library_name:s}.{'lib' if platform.system() == 'Windows' else 'a':s}'),                                                                            # noqa: E501
                                                    object_file_build_paths=' '.join([os.path.join(relative_build_directory, file_path) for file_path in os.listdir(build_directory) if os.path.splitext(file_path)[1] == '.o'])),  # noqa: E501
                common_directory)


def test_executable(executable_directory: str,
                    executable_name: str) -> None:

    if os.path.exists(os.path.join(os.path.join(executable_directory, f'{executable_name:s}.exe'))):
        _ = \
            run_command('Testing Executable',
                        f'{executable_name:s}.exe',
                        executable_directory)


def build_static_library_from_source(source_directory: str,
                                     build_directory: str,
                                     include_directory: str,
                                     library_directory: str,
                                     library_name: str,
                                     other_include_directories: Optional[list[str]] = None,
                                     other_library_paths: Optional[list[str]] = None) -> None:

    success: bool = \
        generate_object_files(source_directory,
                              build_directory,
                              other_include_directories)

    if success:

        copy_header_files_from_source_into_include(source_directory,
                                                   include_directory)

        archive_object_files_into_static_library(library_name,
                                                 build_directory,
                                                 library_directory,
                                                 other_library_paths)


def build_executable_from_source(source_directory: str,
                                 build_directory: str,
                                 executable_name: str,
                                 include_directories: Optional[list[str]] = None,
                                 library_paths: Optional[list[str]] = None) -> None:

    success: bool = \
        generate_object_files(source_directory,
                              build_directory,
                              include_directories)

    if success:
        link_object_files_into_executable(build_directory,
                                          executable_name,
                                          library_paths)

    test_executable(build_directory, executable_name)
