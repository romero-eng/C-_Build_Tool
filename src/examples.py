import shutil
import traceback
from pathlib import Path

from compile import CodeBase, Dependency


def test_python_build_tool(library_is_C_plus_plus: bool,
                           library_is_dynamic: bool,
                           clean_up_build_directories: bool) -> None:

    Arithmetic_library_codebase: CodeBase | None = None
    Arithmetic_codebase: CodeBase | None = None

    try:

        Arithmetic_library_codebase = \
            CodeBase('Arithmetic',
                     Path.cwd()/'example_repos'/f'C{'++' if library_is_C_plus_plus else '':s}_Library',
                     language_standard='C++ 2020' if library_is_C_plus_plus else 'C 2018',
                     preprocessor_variables=['ACTIVATE_ARITHMETIC_LIBRARY_DYNAMIC_LINKING', 'EXPORT_AS_DLL'] if library_is_dynamic else [])

        Arithmetic_library: Dependency = Arithmetic_library_codebase.generate_as_dependency(library_is_dynamic)

        Arithmetic_codebase = \
            CodeBase('present_arithmetic',
                     Path.cwd()/'example_repos'/f'C++_code{'_with_C_Linkage' if not library_is_C_plus_plus else '':s}',
                     language_standard='C++ 2020',
                     preprocessor_variables=['ACTIVATE_ARITHMETIC_LIBRARY_DYNAMIC_LINKING'] if library_is_dynamic else [])

        Arithmetic_codebase.add_dependency(Arithmetic_library)
        Arithmetic_codebase.generate_as_executable()

    except Exception:
        print(traceback.format_exc())

    else:
        Arithmetic_codebase.test_executable()

    finally:
        if clean_up_build_directories:

            if Arithmetic_library_codebase:
                if Arithmetic_library_codebase.build_directory.exists():
                    shutil.rmtree(Arithmetic_library_codebase.build_directory)

            if Arithmetic_codebase:
                if Arithmetic_codebase.build_directory.exists():
                    shutil.rmtree(Arithmetic_codebase.build_directory)


if (__name__ == '__main__'):

    library_is_C_plus_plus: bool = False
    library_is_dynamic: bool = False
    clean_up_build_directories: bool = True

    test_python_build_tool(library_is_C_plus_plus,
                           library_is_dynamic,
                           clean_up_build_directories)
