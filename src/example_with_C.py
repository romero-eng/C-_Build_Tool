import shutil
import traceback
from pathlib import Path

from compile import CodeBase


if (__name__ == '__main__'):

    Arithmetic_codebase: CodeBase | None = None

    try:

        Arithmetic_codebase = \
            CodeBase('Arithmetic',
                     Path.cwd()/f'example_C_code',
                     language_standard='C 2018')

        Arithmetic_codebase.generate_as_executable()

    except Exception:
        print(traceback.format_exc())

    else:
        Arithmetic_codebase.test_executable()

    finally:
        if Arithmetic_codebase:
            if Arithmetic_codebase.build_directory.exists():
                shutil.rmtree(Arithmetic_codebase.build_directory)
