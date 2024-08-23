import os
import traceback

import compile


if (__name__ == '__main__'):

    math_library_name: str = 'Math'
    executable_name: str = 'present_addition'

    math_library_repo_directory: str = \
        os.path.join(os.getcwd(), 'sample_C++_library')
    repo_directory: str = \
        os.path.join(os.getcwd(), 'sample_C++_code')

    try:

        compile.build_static_library_from_source(math_library_repo_directory,
                                                 math_library_name)

        compile.build_executable_from_source(repo_directory,
                                             executable_name,
                                             [os.path.join(math_library_repo_directory, 'build', 'include')],
                                             [os.path.join(math_library_repo_directory, 'build', 'lib')],
                                             [math_library_name])

    except Exception:
        print(traceback.format_exc())
