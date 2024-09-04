import platform
from pathlib import Path


class Dependency:

    def __init__(self,
                 name: str,
                 is_dynamic: bool,
                 is_header_only: bool,
                 include_directory: str | Path,
                 library_directory: str | Path) -> None:

        if not include_directory.exists():
            raise ValueError(f'Please make sure the include directory for the \'{self._name:s}\' Dependency exists before instantiating it as a Dependency object')  # noqa: E501
    
        if not is_header_only:
            if not library_directory.exists():
                raise ValueError(f'Please make sure the library directory for the \'{self._name:s}\' Dependency exists before instantiating it as a Dependency object')  # noqa: E501

        self._name: str = name
        self._is_dynamic: bool = is_dynamic
        self._is_header_only: bool = is_header_only
        self._include_directory: Path = Path(include_directory) if isinstance(include_directory, str) else include_directory  # noqa: E501
        self._library_directory: Path = Path(library_directory) if isinstance(library_directory, str) else library_directory  # noqa: E501

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_dynamic(self) -> bool:
        return self._is_dynamic

    @property
    def is_header_only(self) -> bool:
        return self._is_header_only

    @property
    def include_directory(self) -> Path:
        return self._include_directory

    @property
    def extension(self) -> str:

        if self._is_header_only:
            raise ValueError(f'The \'{self._name:s}\' Dependency is a header-only library, it doesn\'t make sense to ask for the Library file extension.')  # noqa: E501

        extension: str

        match platform.system():
            case 'Windows':
                extension = 'dll' if self.is_dynamic else 'lib'
            case _:
                extension = 'so' if self.is_dynamic else 'a'

        return extension

    @property
    def library_path(self) -> Path:

        if self._is_header_only:
            raise ValueError(f'The \'{self._name:s}\' Dependency is a header-only library, it doesn\'t make sense to ask for the Library file path.')  # noqa: E501

        return self._library_directory/f'lib{self._name:s}.{self.extension:s}'


    def exists(self) -> bool:

        dependency_exists: bool = self._include_directory.is_dir() if self._include_directory.exists() else False

        if not self._is_header_only:
            dependency_exists |= self.library_path.is_file() if self.library_path.exists() else False

        return dependency_exists
