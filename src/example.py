import shutil
import traceback
from pathlib import Path

from compile import CodeBase


if (__name__ == '__main__'):

    """
    arithmetic_library_codebase: CodeBase | None = None
    present_arithmetic_codebase: CodeBase | None = None
    use_dynamic_library: bool = False
    clean_up_build_directories: bool = True
    """

    Arithmetic_codebase: CodeBase

    try:
        """
        arithmetic_library_codebase = \
            CodeBase('Arithmetic',
                     Path.cwd()/f'example_C++_{'dynamic' if use_dynamic_library else 'static':s}_library',
                     preprocessor_variables=['ADD_EXPORTS'] if use_dynamic_library else [])

        arithmetic_library = arithmetic_library_codebase.generate_as_dependency(use_dynamic_library)

        present_arithmetic_codebase = \
            CodeBase('present_arithmetic',
                     Path.cwd()/'example_C++_code')

        present_arithmetic_codebase.add_dependency(arithmetic_library)
        present_arithmetic_codebase.generate_as_executable()
        """

        Arithmetic_codebase = \
            CodeBase('Arithmetic',
                     Path.cwd()/f'example_C_code',
                     language_standard='C 2011')
        Arithmetic_codebase.generate_as_executable()

    except Exception:
        print(traceback.format_exc())

    else:
        #present_arithmetic_codebase.test_executable()
        Arithmetic_codebase.test_executable()

    finally:

        """
        if clean_up_build_directories:
            if arithmetic_library_codebase:
                if arithmetic_library_codebase.build_directory.exists():
                    shutil.rmtree(arithmetic_library_codebase.build_directory)
            if present_arithmetic_codebase:
                if present_arithmetic_codebase.build_directory.exists():
                    shutil.rmtree(present_arithmetic_codebase.build_directory)
        """

        if Arithmetic_codebase.build_directory.exists():
            shutil.rmtree(Arithmetic_codebase.build_directory)
