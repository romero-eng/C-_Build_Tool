import os
import shutil

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


def generate_object_files(repo_directory: str,
                          include_directories: list[str] | None = None,
                          preprocessor_variables: list[str] | None = None) -> bool:

    source_directory: str = os.path.join(repo_directory, 'src')
    build_directory: str = os.path.join(repo_directory, 'build')
    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    formatted_flags: list[str] = \
        flags.retrieve_compilation_flags(repo_directory,
                                         preprocessor_variables)

    if include_directories:
        formatted_flags += flags.get_include_directory_flags(include_directories)

    compile_command: str = 'g++ -c {source_file_path:s} -o {object_file_path:s} {flags:s}'

    compile_command = \
        compile_command.format(source_file_path=os.path.join(source_directory, '{relative_source_file_path:s}'),
                               object_file_path=os.path.join(build_directory, '{object_file_name:s}.o'),
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

    formatted_flags: list[str] = []

    if library_directories:
        formatted_flags += flags.get_library_directory_flags(library_directories)

    if library_names:
        formatted_flags += flags.get_library_name_flags(library_names)

    link_command: str = 'g++ -o {{executable:s}} {{object_files:s}} {flags:s}'
    link_command = link_command.format(flags=' '.join([f'-{flag:s}' for flag in formatted_flags]))

    build_directory: str = os.path.join(repo_directory, 'build')
    bin_directory: str = os.path.join(build_directory, 'bin')
    if not os.path.exists(bin_directory):
        os.mkdir(bin_directory)

    object_file_names: list[str] = \
        [file_path for file_path in os.listdir(build_directory) if os.path.splitext(file_path)[1] == '.o']

    success: bool = \
        run_command('Linking Results',
                    link_command.format(executable=os.path.join('bin', f'{executable_name:s}.exe'),
                                        object_files=' '.join(object_file_names)),
                    build_directory)

    if success:
        for file_name in object_file_names:
            os.remove(os.path.join(build_directory, file_name))


def archive_object_files_into_static_library(library_name: str,
                                             repo_directory: str,
                                             other_library_directories: list[str] | None = None,
                                             other_library_names: list[str] | None = None) -> None:

    formatted_flags: list[str] = []

    if other_library_directories:
        formatted_flags += flags.get_library_directory_flags(other_library_directories)

    if other_library_names:
        formatted_flags += flags.get_library_name_flags(other_library_names)

    build_static_library_command: str = 'ar rcs {{library_path:s}} {{object_file_build_paths:s}} {flags:s}'
    build_static_library_command = \
        build_static_library_command.format(flags=' '.join([f'-{flag:s}' for flag in formatted_flags]))

    build_directory: str = os.path.join(repo_directory, 'build')
    library_directory: str = os.path.join(build_directory, 'lib')
    if not os.path.exists(library_directory):
        os.mkdir(library_directory)

    object_file_names: list[str] = \
        [file_path for file_path in os.listdir(build_directory) if os.path.splitext(file_path)[1] == '.o']

    success: bool = \
        run_command('Archiving into Static Library',
                    build_static_library_command.format(library_path=os.path.join('lib', f'{library_name:s}.lib'),
                                                        object_file_build_paths=' '.join(object_file_names)),
                    build_directory)
    if success:
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
