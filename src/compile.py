import json
import shutil
import platform
from pathlib import Path

import flags
from command import run_command


class CodeBase:

    def __init__(self,
                 name: str,
                 repository_directory: str) -> None:

        self._name: str = name
        self._repository_directory: Path = Path(repository_directory)
        self._source_directory: Path = self._repository_directory/'src'
        self._build_directory: Path = self._repository_directory/'build'
        self._binary_directory: Path = self._build_directory/'bin'

        repository_exists: bool = self._repository_directory.is_dir() if self._repository_directory.exists() else False
        if not repository_exists:
            raise ValueError(f'The repository for the \'{name:s}\' code base does not exist')

        source_code_exists: bool = self._source_directory.is_dir() if self._source_directory.exists() else False
        if not source_code_exists:
            raise ValueError(f'No directory labelled \'src\' was found in the \'{self._name:s}\' repository, please create it and put your source code to be compiled there')  # noqa: E501

    @property
    def name(self) -> str:
        return self._name

    @property
    def repository_directory(self) -> Path:
        return self._repository_directory

    @property
    def source_directory(self) -> Path:
        return self._source_directory

    @property
    def build_directory(self) -> Path:

        if not self._build_directory.exists():
            self._build_directory.mkdir()

        return self._build_directory

    @property
    def binary_directory(self) -> Path:

        if not self._binary_directory.exists():
            self._binary_directory.mkdir()

        return self._binary_directory


def copy_header_files_from_source_into_include(codebase: CodeBase) -> None:

    include_directory: Path = codebase.build_directory/'include'
    if not include_directory.exists():
        include_directory.mkdir()

    tmp_dir: Path

    for root, dirs, files in codebase.source_directory.walk():
        for dir in dirs:
            tmp_dir = Path(dir)
            if not tmp_dir.exists():
                tmp_dir.mkdir()
        for file in files:
            if Path(file).suffix == '.h':
                shutil.copyfile(codebase.source_directory/root.relative_to(codebase.source_directory)/file,
                                        include_directory/root.relative_to(codebase.source_directory)/file)  # noqa: E127, E501


def retrieve_compilation_settings(codebase: CodeBase) -> dict[str, str | list[str]]:

    settings_path: Path = codebase.build_directory/'compilation_settings.json'

    settings: dict[str, str | list[str]]

    if not settings_path.exists():

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
                          include_directories: list[Path] | None = None,
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

    current_source_file_path: Path
    corresponding_object_file_path: Path
    success: bool = True

    for root, _, files in codebase.source_directory.walk():
        for file in files:

            current_source_file_path = root.relative_to(codebase.repository_directory)/file
            corresponding_object_file_path = (codebase.build_directory/f'{current_source_file_path.stem:s}.o').relative_to(codebase.repository_directory)  # noqa: E501

            if current_source_file_path.suffix in ['.cc', '.cxx', '.cpp']:

                success = \
                    run_command(f'"{current_source_file_path.stem:s}" Compilation Results',
                                f'g++ -c {str(current_source_file_path):s} -o {str(corresponding_object_file_path):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                                codebase.repository_directory)

                if not success:
                    break

    return success


def link_object_files_into_executable(codebase: CodeBase,
                                      library_directories: list[Path] | None = None,
                                      library_names: list[str] | None = None) -> None:

    formatted_flags: list[str] = []

    if library_directories:
        formatted_flags += flags.get_library_directory_flags(library_directories)
    if library_names:
        formatted_flags += flags.get_library_name_flags(library_names)

    object_file_names: list[str] = \
        [str(file_path) for file_path in codebase.build_directory.iterdir() if file_path.suffix == '.o']

    if run_command('Linking Results',
                   f'g++ -o {str(codebase.binary_directory.relative_to(codebase.build_directory)/codebase.name):s}.exe {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            Path.unlink(codebase.build_directory/file_name)


def archive_object_files_into_static_library(codebase: CodeBase,
                                             other_library_directories: list[str] | None = None,
                                             other_library_names: list[str] | None = None) -> None:

    library_directory: Path = codebase.build_directory/'lib'
    if not library_directory.exists():
        library_directory.mkdir()

    formatted_flags: list[str] = []

    if other_library_directories:
        formatted_flags += flags.get_library_directory_flags(other_library_directories)
    if other_library_names:
        formatted_flags += flags.get_library_name_flags(other_library_names)

    object_file_names: list[str] = \
        [str(file_path) for file_path in codebase.build_directory.iterdir() if file_path.suffix == '.o']

    if run_command('Archiving into Static Library',
                   f'ar rcs {str(library_directory.relative_to(codebase.build_directory)/codebase.name):s}.{'lib' if platform.system() == 'Windows' else 'a':s} {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            Path.unlink(codebase.build_directory/file_name)


def create_dynamic_library(codebase: CodeBase,
                           other_library_directories: list[str] | None = None,
                           other_library_names: list[str] | None = None) -> None:

    library_directory: Path = codebase.build_directory/'lib'
    if not library_directory.exists():
        library_directory.mkdir()

    formatted_flags: list[str] = \
        flags.get_dynamic_library_creation_flags(retrieve_compilation_settings(codebase))

    if other_library_directories:
        formatted_flags += flags.get_library_directory_flags(other_library_directories)
    if other_library_names:
        formatted_flags += flags.get_library_name_flags(other_library_names)

    object_file_names: list[str] = \
        [str(file_path) for file_path in codebase.build_directory.iterdir() if file_path.suffix == '.o']

    if run_command('Creating Dynamic Library',
                   f'ld -o {str(library_directory.relative_to(codebase.build_directory)/codebase.name):s}.{'dll' if platform.system() == 'Windows' else 'so':s} {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            Path.unlink(codebase.build_directory/file_name)


def test_executable(codebase: CodeBase) -> None:

    executable_path: Path = codebase.binary_directory/f'{codebase.name:s}.exe'

    if executable_path.exists():
        _ = \
            run_command('Testing Executable',
                        f'{executable_path.stem:s}.exe',
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
                                 include_directories: list[Path] | None = None,
                                 library_directories: list[Path] | None = None,
                                 library_names: list[str] | None = None) -> None:

    success: bool = \
        generate_object_files(codebase,
                              include_directories)

    if success:
        link_object_files_into_executable(codebase,
                                          library_directories,
                                          library_names)

    test_executable(codebase)
