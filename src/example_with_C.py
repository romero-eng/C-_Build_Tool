import shutil
import traceback
from pathlib import Path

from compile import CodeBase, Dependency


if (__name__ == '__main__'):

    Add_library_codebase: CodeBase | None = None
    Add_codebase: CodeBase | None = None

    try:

        Add_library_codebase = \
            CodeBase('Arithmetic',
                     Path.cwd()/'example_C_library',
                     language_standard='C 2018')

        Add_library: Dependency = Add_library_codebase.generate_as_dependency(False)

        Add_codebase = \
            CodeBase('Arithmetic',
                     Path.cwd()/'example_C_code',
                     language_standard='C 2018')

        Add_codebase.add_dependency(Add_library)
        Add_codebase.generate_as_executable()

    except Exception:
        print(traceback.format_exc())

    else:
        Add_codebase.test_executable()

    finally:

        if Add_library_codebase:
            if Add_library_codebase.build_directory.exists():
                shutil.rmtree(Add_library_codebase.build_directory)
        if Add_codebase:
            if Add_codebase.build_directory.exists():
                shutil.rmtree(Add_codebase.build_directory)
