import os
import json
import shutil
import platform

import flags
from command import run_command


def copy_header_files_from_source_into_include(repo_directory: str) -> None:

    source_directory: str = os.path.join(repo_directory, 'src')
    include_directory: str = os.path.join(repo_directory, 'build', 'include')
    if not os.path.exists(include_directory):
        os.mkdir(include_directory)

    relative_root: str

    for root, dirs, files in os.walk(source_directory):
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)
        for file in files:
            if os.path.splitext(file)[1] == '.h':
                relative_root = root.split(source_directory)[1]
                shutil.copyfile(os.path.join(source_directory, relative_root, file),
                                os.path.join(include_directory, relative_root, file))


def retrieve_compilation_settings(repo_directory) -> dict[str, str | list[str]]:

    settings_path: str = os.path.join(repo_directory, 'build', 'compilation_settings.json')

    settings: dict[str, str | list[str]]

    if os.path.exists(repo_directory):
        if os.path.isdir(repo_directory):
            if not os.path.exists(settings_path):

                settings = \
                    {'Build Configuration': list(flags.FLAGS_PER_BUILD_CONFIGURATION.keys())[0],
                     'Language Standard': f'C++ {2011 + 3*flags.LANGUAGE_STANDARDS.index('2a'):d}',
                     'Warnings': list(flags.FLAG_PER_WARNING.keys()),
                     'Miscellaneous': list(flags.FLAG_PER_MISCELLANEOUS_DECISION.keys())}

                with open(settings_path, 'w') as json_file:
                    json.dump(settings, json_file, indent=4)

            else:
                with open(settings_path, 'r') as json_file:
                    settings = json.load(json_file)

    return settings


def generate_object_files(repo_directory: str,
                          include_directories: list[str] | None = None,
                          preprocessor_variables: list[str] | None = None) -> bool:

    source_directory: str = os.path.join(repo_directory, 'src')
    build_directory: str = os.path.join(repo_directory, 'build')
    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    settings: dict[str, str | list[str]] = retrieve_compilation_settings(repo_directory)

    formatted_flags: list[str] = []

    if 'Build Configuration' in settings:
        formatted_flags += flags.get_build_configuration_flags(settings['Build Configuration'])  # type: ignore[arg-type]  # noqa: E501  # this is all here because mypy apparently can't handle type narrowing
    if 'Language Standard' in settings:
        formatted_flags += flags.get_language_standard_flag(settings['Language Standard'])  # type: ignore[arg-type]  # noqa: E501  # this is all here because mypy apparently can't handle type narrowing
    if 'Warnings' in settings:
        formatted_flags += flags.get_warning_flags(settings['Warnings'])
    if 'Miscellaneous' in settings:
        formatted_flags += flags.get_miscellaneous_flags(settings['Miscellaneous'])
    if preprocessor_variables:
        formatted_flags += flags.get_preprocessor_variable_flags(preprocessor_variables)
    if include_directories:
        formatted_flags += flags.get_include_directory_flags(include_directories)

    compile_command: str = 'g++ -c {source_file_path:s} -o {object_file_path:s} {flags:s}'

    compile_command = \
        compile_command.format(source_file_path=os.path.join('src', '{relative_source_file_path:s}'),
                               object_file_path=os.path.join('build', '{object_file_name:s}.o'),
                               flags=' '.join([f'-{flag:s}' for flag in formatted_flags]))

    success: bool = True

    for root, _, files in os.walk(source_directory):
        for file in files:
            if os.path.splitext(file)[1] in ['.cc', '.cxx', '.cpp']:

                success = \
                    run_command(f'"{os.path.splitext(file)[0]:s}" Compilation Results',
                                compile_command.format(relative_source_file_path=os.path.join(root.split(source_directory)[1], file),  # noqa: E501
                                                       object_file_name=os.path.splitext(file)[0]),
                                repo_directory)

                if not success:
                    break

    return success


def link_object_files_into_executable(repo_directory: str,
                                      executable_name: str,
                                      library_directories: list[str] | None = None,
                                      library_names: list[str] | None = None) -> None:

    build_directory: str = os.path.join(repo_directory, 'build')
    bin_directory: str = os.path.join(build_directory, 'bin')
    if not os.path.exists(bin_directory):
        os.mkdir(bin_directory)

    formatted_flags: list[str] = []

    if library_directories:
        formatted_flags += flags.get_library_directory_flags(library_directories)
    if library_names:
        formatted_flags += flags.get_library_name_flags(library_names)

    object_file_names: list[str] = \
        [file_path for file_path in os.listdir(build_directory) if os.path.splitext(file_path)[1] == '.o']

    if run_command('Linking Results',
                   f'g++ -o {os.path.join('bin', executable_name):s}.exe {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',
                   build_directory):
        for file_name in object_file_names:
            os.remove(os.path.join(build_directory, file_name))


def archive_object_files_into_static_library(library_name: str,
                                             repo_directory: str,
                                             other_library_directories: list[str] | None = None,
                                             other_library_names: list[str] | None = None) -> None:

    build_directory: str = os.path.join(repo_directory, 'build')
    library_directory: str = os.path.join(build_directory, 'lib')
    if not os.path.exists(library_directory):
        os.mkdir(library_directory)

    formatted_flags: list[str] = []

    if other_library_directories:
        formatted_flags += flags.get_library_directory_flags(other_library_directories)
    if other_library_names:
        formatted_flags += flags.get_library_name_flags(other_library_names)

    object_file_names: list[str] = \
        [file_path for file_path in os.listdir(build_directory) if os.path.splitext(file_path)[1] == '.o']

    if run_command('Archiving into Static Library',
                   f'ar rcs {os.path.join('lib', library_name):s}.{'lib' if platform.system() == 'Windows' else 'a':s} {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',
                   build_directory):
        for file_name in object_file_names:
            os.remove(os.path.join(build_directory, file_name))


def test_executable(repo_directory: str,
                    executable_name: str) -> None:

    bin_directory = os.path.join(repo_directory, 'build', 'bin')
    if os.path.exists(os.path.join(os.path.join(bin_directory, f'{executable_name:s}.exe'))):
        _ = \
            run_command('Testing Executable',
                        f'{executable_name:s}.exe',
                        bin_directory)


def build_static_library_from_source(repo_directory: str,
                                     library_name: str,
                                     other_include_directories: list[str] | None = None,
                                     other_library_directories: list[str] | None = None,
                                     other_library_names: list[str] | None = None) -> None:

    success: bool = \
        generate_object_files(repo_directory,
                              other_include_directories)

    if success:

        copy_header_files_from_source_into_include(repo_directory)

        archive_object_files_into_static_library(library_name,
                                                 repo_directory,
                                                 other_library_directories,
                                                 other_library_names)


def build_executable_from_source(repo_directory: str,
                                 executable_name: str,
                                 include_directories: list[str] | None = None,
                                 library_directories: list[str] | None = None,
                                 library_names: list[str] | None = None) -> None:

    success: bool = \
        generate_object_files(repo_directory,
                              include_directories)

    if success:
        link_object_files_into_executable(repo_directory,
                                          executable_name,
                                          library_directories,
                                          library_names)

    test_executable(repo_directory, executable_name)
