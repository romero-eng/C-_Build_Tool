import os
import json
import shutil
import platform

import flags
from command import run_command


class CodeBase:

    def __init__(self,
                 name: str,
                 repository_directory: str) -> None:

        self._name: str = name
        self._repository_directory: str = repository_directory
        self._source_directory: str = os.path.join(self._repository_directory, 'src')
        self._build_directory: str = os.path.join(self._repository_directory, 'build')
        self._binary_directory: str = os.path.join(self._build_directory, 'bin')

        repository_exists: bool = os.path.isdir(self._repository_directory) if os.path.exists(self._repository_directory) else False
        if not repository_exists:
            raise ValueError(f'The repository for the \'{name:s}\' code base does not exist')

        source_code_exists: bool = os.path.isdir(self._source_directory) if os.path.exists(self._source_directory) else False
        if not source_code_exists:
            raise ValueError(f'No directory labelled \'src\' was found in the \'{self._name:s}\' repository, please create it and put your source code to be compiled there')

        if not os.path.exists(self._build_directory):
            os.mkdir(self._build_directory)

        if not os.path.exists(self._binary_directory):
            os.mkdir(self._binary_directory)

    @property
    def name(self) -> str:
        return self._name

    @property
    def repository_directory(self) -> str:
        return self._repository_directory

    @property
    def source_directory(self) -> str:
        return self._source_directory

    @property
    def build_directory(self) -> str:
        return self._build_directory

    @property
    def binary_directory(self) -> str:
        return self._binary_directory


def copy_header_files_from_source_into_include(codebase: CodeBase) -> None:

    include_directory: str = os.path.join(codebase.build_directory, 'include')
    if not os.path.exists(include_directory):
        os.mkdir(include_directory)

    relative_root: str

    for root, dirs, files in os.walk(codebase.source_directory):
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)
        for file in files:
            if os.path.splitext(file)[1] == '.h':
                relative_root = root.split(codebase.source_directory)[1]
                shutil.copyfile(os.path.join(codebase.source_directory, relative_root, file),
                                os.path.join(include_directory, relative_root, file))


def retrieve_compilation_settings(codebase: CodeBase) -> dict[str, str | list[str]]:

    settings_path: str = os.path.join(codebase.build_directory, 'compilation_settings.json')

    settings: dict[str, str | list[str]]

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


def generate_object_files(codebase: CodeBase,
                          include_directories: list[str] | None = None,
                          preprocessor_variables: list[str] | None = None) -> bool:

    settings: dict[str, str | list[str]] = retrieve_compilation_settings(codebase)

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

    for root, _, files in os.walk(codebase.source_directory):
        for file in files:
            if os.path.splitext(file)[1] in ['.cc', '.cxx', '.cpp']:

                success = \
                    run_command(f'"{os.path.splitext(file)[0]:s}" Compilation Results',
                                compile_command.format(relative_source_file_path=os.path.join(os.path.relpath(codebase.source_directory, root), file),  # noqa: E501
                                                       object_file_name=os.path.splitext(file)[0]),
                                codebase.repository_directory)

                if not success:
                    break

    return success


def link_object_files_into_executable(codebase: CodeBase,
                                      library_directories: list[str] | None = None,
                                      library_names: list[str] | None = None) -> None:

    formatted_flags: list[str] = []

    if library_directories:
        formatted_flags += flags.get_library_directory_flags(library_directories)
    if library_names:
        formatted_flags += flags.get_library_name_flags(library_names)

    object_file_names: list[str] = \
        [file_path for file_path in os.listdir(codebase.build_directory) if os.path.splitext(file_path)[1] == '.o']

    if run_command('Linking Results',
                   f'g++ -o {os.path.join('bin', codebase.name):s}.exe {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            os.remove(os.path.join(codebase.build_directory, file_name))


def archive_object_files_into_static_library(codebase: CodeBase,
                                             other_library_directories: list[str] | None = None,
                                             other_library_names: list[str] | None = None) -> None:

    library_directory: str = os.path.join(codebase.build_directory, 'lib')
    if not os.path.exists(library_directory):
        os.mkdir(library_directory)

    formatted_flags: list[str] = []

    if other_library_directories:
        formatted_flags += flags.get_library_directory_flags(other_library_directories)
    if other_library_names:
        formatted_flags += flags.get_library_name_flags(other_library_names)

    object_file_names: list[str] = \
        [file_path for file_path in os.listdir(codebase.build_directory) if os.path.splitext(file_path)[1] == '.o']

    if run_command('Archiving into Static Library',
                   f'ar rcs {os.path.join('lib', codebase.name):s}.{'lib' if platform.system() == 'Windows' else 'a':s} {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            os.remove(os.path.join(codebase.build_directory, file_name))


def create_dynamic_library(codebase: CodeBase,
                           other_library_directories: list[str] | None = None,
                           other_library_names: list[str] | None = None) -> None:

    library_directory: str = os.path.join(codebase.build_directory, 'lib')
    if not os.path.exists(library_directory):
        os.mkdir(library_directory)

    formatted_flags: list[str] = \
        flags.get_dynamic_library_creation_flags(retrieve_compilation_settings(codebase))

    if other_library_directories:
        formatted_flags += flags.get_library_directory_flags(other_library_directories)
    if other_library_names:
        formatted_flags += flags.get_library_name_flags(other_library_names)

    object_file_names: list[str] = \
        [file_path for file_path in os.listdir(codebase.build_directory) if os.path.splitext(file_path)[1] == '.o']

    if run_command('Creating Dynamic Library',
                   f'ld -o {os.path.join('lib', codebase.name):s}.{'dll' if platform.system() == 'Windows' else 'so':s} {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            os.remove(os.path.join(codebase.build_directory, file_name))


def test_executable(codebase: CodeBase) -> None:

    if os.path.exists(os.path.join(os.path.join(codebase.binary_directory, f'{codebase.name:s}.exe'))):
        _ = \
            run_command('Testing Executable',
                        f'{codebase.name:s}.exe',
                        codebase.binary_directory)


def build_static_library_from_source(codebase: CodeBase,
                                     other_include_directories: list[str] | None = None,
                                     other_library_directories: list[str] | None = None,
                                     other_library_names: list[str] | None = None) -> None:

    success: bool = \
        generate_object_files(codebase,
                              other_include_directories)

    if success:

        copy_header_files_from_source_into_include(codebase)

        archive_object_files_into_static_library(codebase,
                                                 other_library_directories,
                                                 other_library_names)


def build_dynamic_library_from_source(codebase: CodeBase,
                                      preprocessor_variables: list[str] | None = None,
                                      other_include_directories: list[str] | None = None,
                                      other_library_directories: list[str] | None = None,
                                      other_library_names: list[str] | None = None) -> None:

    success: bool = \
        generate_object_files(codebase,
                              other_include_directories,
                              preprocessor_variables)

    if success:

        copy_header_files_from_source_into_include(codebase)

        create_dynamic_library(codebase,
                               other_library_directories,
                               other_library_names)


def build_executable_from_source(codebase: CodeBase,
                                 include_directories: list[str] | None = None,
                                 library_directories: list[str] | None = None,
                                 library_names: list[str] | None = None) -> None:

    success: bool = \
        generate_object_files(codebase,
                              include_directories)

    if success:
        link_object_files_into_executable(codebase,
                                          library_directories,
                                          library_names)

    test_executable(codebase)
