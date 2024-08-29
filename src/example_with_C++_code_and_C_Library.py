import shutil
import traceback
from pathlib import Path

from compile import CodeBase, Dependency


if (__name__ == '__main__'):

    Arithmetic_library_codebase: CodeBase | None = None
    Arithmetic_codebase: CodeBase | None = None

    library_is_C_plus_plus: bool = True
    use_dynamic_library: bool = False
    clean_up_build_directories: bool = False

    try:

        Arithmetic_library_codebase = \
            CodeBase('Arithmetic',
                     Path.cwd()/f'example_C{'++' if library_is_C_plus_plus else '':s}_{'dynamic' if use_dynamic_library else 'static':s}_library',
                     language_standard='C++ 2020' if library_is_C_plus_plus else 'C 2018',
                     preprocessor_variables=['ADD_EXPORTS'] if use_dynamic_library else [])

        Arithmetic_library: Dependency = Arithmetic_library_codebase.generate_as_dependency(use_dynamic_library)

        Arithmetic_codebase = \
            CodeBase('present_arithmetic',
                     Path.cwd()/f'example_C++_code{'_with_C_Linkage' if not library_is_C_plus_plus else '':s}',
                     language_standard='C++ 2020')

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
