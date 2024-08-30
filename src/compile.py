import re
import shutil
import platform
from pathlib import Path

from command import run_command


# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-build-configurations/
FLAGS_PER_BUILD_CONFIGURATION: dict[str, list[str]] = \
    {'Debug': ['ggdb'],
     'Release': ['O2', 'DNDEBUG']}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-choosing-a-language-standard/
C_PLUS_PLUS_LANGUAGE_STANDARDS: list[str] = ['0x', '1y', '1z',  '2a', '2b']
C_LANGUAGE_STANDARDS: list[int] = [1989, 1990, 1999, 2011, 2018]

C_PLUS_PLUS_SOURCE_CODE_EXTENSIONS: list[str] = ['.cc', '.cxx', '.cpp']
C_PLUS_PLUS_HEADER_EXTENSION: str = '.hpp'

C_SOURCE_CODE_EXTENSIONS: list[str] = ['.c']
C_HEADER_EXTENSION: str = '.h'

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-compiler-extensions/
FLAG_PER_MISCELLANEOUS_DECISION: dict[str, str] = \
    {'Disable Compiler Extensions': 'pedantic-errors'}

# https://www.learncpp.com/cpp-tutorial/configuring-your-compiler-warning-and-error-levels/
# https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#Warning-Options
# https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html
FLAG_PER_WARNING: dict[str, str] = \
    {'Treat warnings as errors': 'error',
     'Avoid a lot of questionable coding practices': 'all',
     'Avoid even more questionable coding practices': 'extra',
     'Follow Effective C++ Style Guidelines': 'effc++',
     'Avoid potentially value-changing implicit conversions': 'conversion',
     'Avoid potentially sign-changing implicit conversions for integers': 'sign-conversion'}


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
    def library_path(self) -> Path:
        return self._library_directory/f'lib{self._name:s}.{('dll' if self._is_dynamic else 'lib') if platform.system() == 'Windows' else ('so' if self._is_dynamic else 'a'):s}'  # noqa: E501

    def exists(self) -> bool:
        return (self._include_directory.is_dir() if self._include_directory.exists() else False) and (self.library_path.is_file() if self.library_path.exists() else False)  # noqa: E501


class CodeBase:

    def __init__(self,
                 name: str,
                 repository_directory: Path,
                 build_configuration: str = list(FLAGS_PER_BUILD_CONFIGURATION.keys())[0],
                 language_standard: str = f'C++ {2011 + 3*C_PLUS_PLUS_LANGUAGE_STANDARDS.index('2a'):d}',
                 warnings: str | list[str] = list(FLAG_PER_WARNING.keys()),
                 miscellaneous: str | list[str] = list(FLAG_PER_MISCELLANEOUS_DECISION.keys()),
                 preprocessor_variables: list[str] = []) -> None:

        self._name: str = name

        # Initialize the Repository directory and make sure it already exists
        self._repository_directory: Path = repository_directory
        repository_exists: bool = self._repository_directory.is_dir() if self._repository_directory.exists() else False
        if not repository_exists:
            raise ValueError(f'The repository for the \'{name:s}\' code base does not exist')

        # Initialize the Source directory and make sure it already exists
        self._source_directory: Path = self._repository_directory/'src'
        source_code_exists: bool = self._source_directory.is_dir() if self._source_directory.exists() else False
        if not source_code_exists:
            raise ValueError(f'No directory labelled \'src\' was found in the \'{self._name:s}\' repository, please create it and put your source code to be compiled there')  # noqa: E501

        # Initialize the Build and Binary directories
        self._build_directory: Path = self._repository_directory/'build'
        self._binary_directory: Path = self._build_directory/'bin'

        # Set the build configuration, and check to make sure it makes sense
        self._build_configuration: str = build_configuration
        if self._build_configuration not in FLAGS_PER_BUILD_CONFIGURATION:
            raise ValueError(f"The following build configuration is not recognized: {self._build_configuration:s}")   # noqa: E501

        # Set the warning, and check to make sure they make sense
        self._warnings: list[str] = [warnings] if isinstance(warnings, str) else warnings
        for warning in self._warnings:
            if warning not in FLAG_PER_WARNING:
                raise ValueError(f'The following warning is not recognized: {warning:s}')

        # Set the miscellaneous decisions, and check to make sure they make sense
        self._miscellaneous: list[str] = [miscellaneous] if isinstance(miscellaneous, str) else miscellaneous
        for decision in self._miscellaneous:
            if decision not in FLAG_PER_MISCELLANEOUS_DECISION:
                raise ValueError(f'The following miscellanous decision is not recognized: {decision:s}')

        # Set the language standard, and check to make sure it makes sense
        self._language_standard: str = language_standard

        two_digit_year: int
        self._utility: str
        self._language_standard_flag: str
        self._source_code_extensions: list[str]
        self._header_file_extension: str

        language_standard_recognized: bool = False
        matched_C_Plus_Plus_standard: re.Match[str] | None = re.fullmatch(r'C\++ 20(\d\d)', self._language_standard)
        matched_C_standard: re.Match[str] | None = re.fullmatch(r'C (19|20)(\d\d)', self._language_standard)

        if matched_C_Plus_Plus_standard:

            two_digit_year = int(matched_C_Plus_Plus_standard.groups()[0])
            if two_digit_year - 11 >= 0:
                if (two_digit_year - 11) % 3 == 0:
                    language_standard_recognized = True
                    self._utility = 'g++'
                    self._language_standard_flag = f'++{C_PLUS_PLUS_LANGUAGE_STANDARDS[int((int(matched_C_Plus_Plus_standard.groups()[0]) - 11)/3)]:s}'  # noqa: E501
                    self._source_code_extensions = C_PLUS_PLUS_SOURCE_CODE_EXTENSIONS
                    self._header_file_extension = C_PLUS_PLUS_HEADER_EXTENSION

        elif matched_C_standard:

            century: int = int(matched_C_standard.groups()[0])
            two_digit_year = int(matched_C_standard.groups()[1])

            if 100*century + two_digit_year in C_LANGUAGE_STANDARDS:
                language_standard_recognized = True
                self._utility = 'gcc'
                self._language_standard_flag = f'{two_digit_year:2d}'
                self._source_code_extensions = C_SOURCE_CODE_EXTENSIONS
                self._header_file_extension = C_HEADER_EXTENSION

                # This is not a valid warning for C compilation
                if 'Follow Effective C++ Style Guidelines' in self._warnings:
                    self._warnings.remove('Follow Effective C++ Style Guidelines')

        if not language_standard_recognized:
            raise ValueError(f'The following Language Standard is not recognized: {self._language_standard:s}')

        # Initialize the list of preprocessor variables
        self._preprocessor_variables: list[str] = preprocessor_variables

        # Initialize the list of Dependencies
        self._dependencies: list[Dependency] = []

    def __str__(self) -> str:

        def format_flag_statuses(title: str,
                                 known_flag_descriptions: list[str],
                                 chosen_descriptions: list[str]) -> str:

            max_description_length: int = max([len(description) for description in known_flag_descriptions])
            formatted_flag_statuses: str = \
                f'{title:s} Options:\n{'':{'-':s}>{len(title) + 9:d}s}\n{'\n'.join([f'{description:>{max_description_length:d}s}: {'ON' if description in chosen_descriptions else 'OFF':s}' for description in known_flag_descriptions]):s}'  # noqa: E231, E501

            return formatted_flag_statuses

        def format_chosen_flag(flag_choice: str,
                               chosen_flag_description: str) -> str:

            return f'{flag_choice:s}: {chosen_flag_description:s}'

        description: str = \
            (f'{'':{'=':s}<200s}\n{'':{'=':s}<200s}\n\n' +                     # noqa: E231
             '\n\n'.join([format_chosen_flag('Build Configuration',
                                             self._build_configuration),
                          format_chosen_flag('Language Standard',
                                             self._language_standard),
                          format_flag_statuses('Warning',
                                               list(FLAG_PER_WARNING.keys()),
                                               self._warnings),
                          format_flag_statuses('Miscellaneous',
                                               list(FLAG_PER_MISCELLANEOUS_DECISION.keys()),
                                               self._miscellaneous)]))

        return f'\n{description:s}'

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
        return self._build_directory

    @property
    def binary_directory(self) -> Path:
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

    @property
    def dependencies(self) -> list[Dependency]:
        return self._dependencies

    def _generate_object_files(self) -> None:

        print(self)

        # Get flags from the compilation settings
        formatted_flags: list[str] = \
            (FLAGS_PER_BUILD_CONFIGURATION[self._build_configuration] +
             [f'std=c{self._language_standard_flag:s}'] +
             [f'W{flag:s}' for warning, flag in FLAG_PER_WARNING.items() if warning in self._warnings] +
             [flag for decision, flag in FLAG_PER_MISCELLANEOUS_DECISION.items() if decision in self._miscellaneous] +  # noqa: E501
             [f'D {variable:s}' for variable in self._preprocessor_variables])

        # Get optional flags based on Dependencies
        if self._dependencies:
            formatted_flags += list(set([f'I {str(dependency.include_directory):s}' for dependency in self._dependencies]))  # noqa: E501

        # Initialize the Build directory
        if not self._build_directory.exists():
            self._build_directory.mkdir()
            print(f'\nCreating Build Directory: {str(self._build_directory):s}\n')

        # Initialize variables for the upcoming for-loop
        tmp_source_file_path: Path
        tmp_object_file_path: Path

        # Initialize the compile command
        compile_command: str = '{utility:s} -c {input_source:s} -o {output_object:s} {compilation_flags:s}'

        # Walk through the Source directory and compile each individual source file
        for root, _, files in self._source_directory.walk():
            for file in files:

                # Get the file paths for the source file and corresponding object file
                tmp_source_file_path = root/file
                tmp_object_file_path = self._build_directory/f'{tmp_source_file_path.stem:s}.o'

                # If the source code file is C/C++,...
                if tmp_source_file_path.suffix in self._source_code_extensions:

                    # ..., then compile it
                    run_command(f'"{tmp_source_file_path.stem:s}" Compilation Results',
                                compile_command.format(utility=self._utility,
                                                       input_source=str(tmp_source_file_path.relative_to(self._repository_directory)),   # noqa: E501
                                                       output_object=str(tmp_object_file_path.relative_to(self._repository_directory)),  # noqa: E501
                                                       compilation_flags=' '.join([f'-{flag:s}' for flag in formatted_flags])),          # noqa: E501
                                self._repository_directory)

    def generate_as_executable(self) -> None:

        # Generate and retrieve the object file paths
        self._generate_object_files()
        object_paths: list[Path] = [file_path for file_path in self._build_directory.glob('*.o')]

        # Get flags from each library directory per dependency
        formatted_flags = \
            [f'L {str(dependency.library_path.parent):s}' for dependency in self._dependencies] + \
            [f'l{str(dependency.name):s}' for dependency in self._dependencies]

        # Initialize the Binary directory
        if not self._binary_directory.exists():
            self._binary_directory.mkdir()
            print(f'\nCreating Binary Directory: {str(self._binary_directory):s}\n')

        # Initialize the path for the to-be-compiled executable within the Binary directory
        executable_path: Path = self._binary_directory/f'{self._name:s}.exe'

        # Initialize the command for the executable creation
        link_command: str = '{utility:s} -o {output_executable:s} {input_objects:s} {linking_flags:s}'

        # Run the object linking command within the Build Directory
        run_command('Linking Results',
                    link_command.format(utility=self._utility,
                                        output_executable=str(executable_path.relative_to(self._build_directory)),
                                        input_objects=' '.join([object_path.name for object_path in object_paths]),
                                        linking_flags=' '.join([f'-{flag:s}' for flag in formatted_flags])),
                    self._build_directory)

        # Remove the object files afterwards
        for object_path in object_paths:
            Path.unlink(object_path)

    def generate_as_dependency(self,
                               is_dynamic: bool) -> Dependency:

        # Generate and retrieve the object file paths
        self._generate_object_files()
        object_paths: list[Path] = [file_path for file_path in self._build_directory.glob('*.o')]

        # Initialize the Library Directory
        library_directory: Path = self._build_directory/'lib'
        if not library_directory.exists():
            library_directory.mkdir()
            print(f'\nCreating Library Directory: {str(library_directory):s}\n')

        # Initialize the Include Directory
        include_directory: Path = self._build_directory/'include'
        if not include_directory.exists():
            include_directory.mkdir()

        # Finally, create the Dependency with the Include and Library directories
        codebase_as_dependency: Dependency = \
            Dependency(self._name,
                       is_dynamic,
                       include_directory,
                       library_directory)

        tmp_dir: Path

        # Walk through the Source directory and copy over the header files to the Include directory
        for root, dirs, files in self._source_directory.walk():
            for dir in dirs:
                tmp_dir = Path(dir)
                if not tmp_dir.exists():
                    tmp_dir.mkdir()
            for file in files:
                if Path(file).suffix == self._header_file_extension:
                    shutil.copyfile(self._source_directory/root.relative_to(self._source_directory)/file,
                                         include_directory/root.relative_to(self._source_directory)/file)  # noqa: E127

        # Create the flags for the object linking command based on libraries
        linking_flags = \
            [f'L {str(dependency.library_path.parent):s}' for dependency in self._dependencies] + \
            [ f'l{str(dependency.library_path.name  ):s}' for dependency in self._dependencies]      # noqa: E201, E202

        # Add further flags based on library type
        if is_dynamic:
            linking_flags += ['shared']
            if self._build_configuration == 'Release':
                linking_flags += ['s']
        else:
            linking_flags += ['r', 'c', 's']

        # Initialize the command for the library creation
        create_command: str = '{utility:s} {linking_flags:s} -o {output_library:s} {input_objects:s}'

        # Run the library creation command within the Build Directory
        run_command('Creating Dynamic Library' if is_dynamic else 'Archiving into Static Library',
                    create_command.format(utility=self._utility if is_dynamic else 'ar',
                                          output_library=str(codebase_as_dependency.library_path.relative_to(self._build_directory)),  # noqa: E501
                                          input_objects=' '.join([object_path.name for object_path in object_paths]),
                                          linking_flags=' '.join([f'-{flag:s}' for flag in linking_flags])),
                    self._build_directory)

        # Remove the object files afterwards
        for object_path in object_paths:
            Path.unlink(object_path)

        return codebase_as_dependency

    def add_dependency(self,
                       new_dependency: Dependency) -> None:
        self._dependencies.append(new_dependency)

    def test_executable(self) -> None:

        # Initialize the compiled executable path (within the Build directory)
        executable_path: Path = self._binary_directory/f'{self._name:s}.exe'

        # If the executable has already been compiled,...
        if executable_path.exists():

            # Move any .dll/.so files to the Binary directory for testing
            for dependency in self._dependencies:
                if dependency.is_dynamic:
                    shutil.copyfile(dependency.library_path,
                                    self._binary_directory/dependency.library_path.name)

            # Actually test the executable
            run_command('Testing Executable',
                        f'{executable_path.stem:s}.exe',
                        self._binary_directory)
