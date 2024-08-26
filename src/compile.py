import shutil
import platform
from pathlib import Path

import flags
from command import run_command


class Dependency:

    def __init__(self,
                 name: str,
                 is_dynamic: bool,
                 include_directory: str | Path,
                 library_directory: str | Path) -> None:

        self._name: str = name
        self._is_dynamic: bool = is_dynamic
        self._include_directory: Path = Path(include_directory) if isinstance(include_directory, str) else include_directory  # noqa: E501
        self._library_directory: Path = Path(library_directory) if isinstance(library_directory, str) else library_directory  # noqa: E501

        if not self._include_directory.exists():
            raise ValueError(f'Please make sure the include directory for the \'{self._name:s}\' Dependency exists before instantiating it as a Dependency object')  # noqa: E501

        if not self._library_directory.exists():
            raise ValueError(f'Please make sure the library directory for the \'{self._name:s}\' Dependency exists before instantiating it as a Dependency object')  # noqa: E501

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_dynamic(self) -> bool:
        return self._is_dynamic

    @property
    def include_directory(self) -> Path:
        return self._include_directory

    @property
    def library_directory(self) -> Path:
        return self._library_directory


class CodeBase:

    def __init__(self,
                 name: str,
                 repository_directory: str,
                 build_configuration: str = list(flags.FLAGS_PER_BUILD_CONFIGURATION.keys())[0],
                 language_standard: str = f'C++ {2011 + 3*flags.LANGUAGE_STANDARDS.index('2a'):d}',
                 warnings: list[str] = list(flags.FLAG_PER_WARNING.keys()),
                 miscellaneous: list[str] = list(flags.FLAG_PER_MISCELLANEOUS_DECISION.keys())) -> None:

        self._name: str = name
        self._repository_directory: Path = Path(repository_directory)

        repository_exists: bool = self._repository_directory.is_dir() if self._repository_directory.exists() else False
        if not repository_exists:
            raise ValueError(f'The repository for the \'{name:s}\' code base does not exist')
        
        self._build_configuration: str = build_configuration
        self._language_standard: str = language_standard
        self._warnings: list[str] = warnings
        self._miscellaneous: list[str] = miscellaneous

    @property
    def name(self) -> str:
        return self._name

    @property
    def repository_directory(self) -> Path:
        return self._repository_directory

    @property
    def source_directory(self) -> Path:

        self._source_directory: Path = self._repository_directory/'src'

        source_code_exists: bool = self._source_directory.is_dir() if self._source_directory.exists() else False
        if not source_code_exists:
            raise ValueError(f'No directory labelled \'src\' was found in the \'{self._name:s}\' repository, please create it and put your source code to be compiled there')  # noqa: E501

        return self._source_directory

    @property
    def build_directory(self) -> Path:

        self._build_directory: Path = self._repository_directory/'build'

        if not self._build_directory.exists():
            self._build_directory.mkdir()

        return self._build_directory

    @property
    def binary_directory(self) -> Path:

        self._binary_directory: Path = self._build_directory/'bin'

        if not self._binary_directory.exists():
            self._binary_directory.mkdir()

        return self._binary_directory

    @property
    def build_configuration(self) -> str:
        return self._build_configuration

    @property
    def language_standard(self) -> str:
        return self._language_standard

    @property
    def warnings(self) -> list[str]:
        return self._warnings

    @property
    def miscellaneous(self) -> list[str]:
        return self._miscellaneous

    def generate_as_dependency(self,
                            is_dynamic: bool) -> Dependency:

        library_directory: Path = self._build_directory/'lib'
        if not library_directory.exists():
            library_directory.mkdir()

        include_directory: Path = self._build_directory/'include'
        if not include_directory.exists():
            include_directory.mkdir()

        tmp_dir: Path

        for root, dirs, files in self.source_directory.walk():
            for dir in dirs:
                tmp_dir = Path(dir)
                if not tmp_dir.exists():
                    tmp_dir.mkdir()
            for file in files:
                if Path(file).suffix == '.h':
                    shutil.copyfile(self.source_directory/root.relative_to(self.source_directory)/file,
                                        include_directory/root.relative_to(self.source_directory)/file)  # noqa: E127

        return Dependency(self._name,
                          is_dynamic,
                          include_directory,
                          library_directory)


def generate_object_files(codebase: CodeBase,
                          dependencies: list[Dependency] | None = None,
                          preprocessor_variables: list[str] | None = None) -> bool:

    formatted_flags: list[str] = []

    formatted_flags += flags.get_build_configuration_flags(codebase.build_configuration)  # type: ignore[arg-type]  # noqa: E501  # this is all here because mypy apparently can't handle type narrowing
    formatted_flags += flags.get_language_standard_flag(codebase.language_standard)  # type: ignore[arg-type]  # noqa: E501  # this is all here because mypy apparently can't handle type narrowing
    formatted_flags += flags.get_warning_flags(codebase.warnings)
    formatted_flags += flags.get_miscellaneous_flags(codebase.miscellaneous)
    if preprocessor_variables:
        formatted_flags += flags.get_preprocessor_variable_flags(preprocessor_variables)
    if dependencies:
        formatted_flags += flags.get_include_directory_flags([dependency.include_directory for dependency in dependencies] if dependencies else None)  # noqa: E501

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
                                      dependencies: list[Dependency] | None = None) -> None:

    formatted_flags: list[str] = []

    if dependencies:
        formatted_flags += flags.get_library_directory_flags([dependency.library_directory for dependency in dependencies] if dependencies else None)  # noqa: E501
        formatted_flags += flags.get_library_name_flags([dependency.name for dependency in dependencies] if dependencies else None)                    # noqa: E501

    object_file_names: list[str] = \
        [str(file_path) for file_path in codebase.build_directory.iterdir() if file_path.suffix == '.o']

    if run_command('Linking Results',
                   f'g++ -o {str(codebase.binary_directory.relative_to(codebase.build_directory)/codebase.name):s}.exe {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            Path.unlink(codebase.build_directory/file_name)


def archive_object_files_into_static_library(codebase: CodeBase,
                                             secondary_dependencies: list[Dependency] | None = None) -> Dependency:

    formatted_flags: list[str] = []

    if secondary_dependencies:
        formatted_flags += flags.get_library_directory_flags([dependency.library_directory for dependency in secondary_dependencies])  # noqa: E501
        formatted_flags += flags.get_library_name_flags([dependency.name for dependency in secondary_dependencies])                    # noqa: E501

    object_file_names: list[str] = \
        [str(file_path) for file_path in codebase.build_directory.iterdir() if file_path.suffix == '.o']

    static_library: Dependency = codebase.generate_as_dependency(False)

    if run_command('Archiving into Static Library',
                   f'ar rcs {str(static_library.library_directory.relative_to(codebase.build_directory)/codebase.name):s}.{'lib' if platform.system() == 'Windows' else 'a':s} {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            Path.unlink(codebase.build_directory/file_name)

    return static_library


def create_dynamic_library(codebase: CodeBase,
                           secondary_dependencies: list[Dependency] | None = None) -> Dependency:

    formatted_flags: list[str] = flags.get_dynamic_library_creation_flags(codebase.build_configuration)

    if secondary_dependencies:
        formatted_flags += flags.get_library_directory_flags([dependency.library_directory for dependency in secondary_dependencies])  # noqa: E501
        formatted_flags += flags.get_library_name_flags([dependency.name for dependency in secondary_dependencies])                    # noqa: E501

    object_file_names: list[str] = \
        [str(file_path) for file_path in codebase.build_directory.iterdir() if file_path.suffix == '.o']

    dynamic_library: Dependency = codebase.generate_as_dependency(True)

    if run_command('Creating Dynamic Library',
                   f'ld -o {str(dynamic_library.library_directory.relative_to(codebase.build_directory)/codebase.name):s}.{'dll' if platform.system() == 'Windows' else 'so':s} {' '.join(object_file_names):s} {' '.join([f'-{flag:s}' for flag in formatted_flags]):s}',  # noqa: E501
                   codebase.build_directory):
        for file_name in object_file_names:
            Path.unlink(codebase.build_directory/file_name)

    return dynamic_library


def test_executable(codebase: CodeBase) -> None:

    executable_path: Path = codebase.binary_directory/f'{codebase.name:s}.exe'

    if executable_path.exists():
        _ = \
            run_command('Testing Executable',
                        f'{executable_path.stem:s}.exe',
                        codebase.binary_directory)


def build_static_library_from_source(codebase: CodeBase,
                                     secondary_dependencies: list[Dependency] | None = None) -> Dependency | None:

    static_library: Dependency | None = \
        archive_object_files_into_static_library(codebase,
                                                 secondary_dependencies) if generate_object_files(codebase,
                                                                                                  secondary_dependencies) else None  # noqa: E501

    return static_library


def build_dynamic_library_from_source(codebase: CodeBase,
                                      preprocessor_variables: list[str] | None = None,
                                      secondary_dependencies: list[Dependency] | None = None) -> Dependency | None:

    dynamic_library: Dependency | None = \
        create_dynamic_library(codebase,
                               secondary_dependencies) if generate_object_files(codebase,
                                                                                secondary_dependencies,
                                                                                preprocessor_variables) else None

    return dynamic_library


def build_executable_from_source(codebase: CodeBase,
                                 dependencies: list[Dependency] | None = None) -> None:

    success: bool = \
        generate_object_files(codebase,
                              dependencies)

    if success:
        link_object_files_into_executable(codebase,
                                          dependencies)

    test_executable(codebase)
