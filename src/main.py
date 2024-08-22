import os
import traceback

import compile


if (__name__ == '__main__'):

    math_library_name: str = 'Math'
    math_library_source_directory: str = os.path.join(os.getcwd(), 'sample_C++_library', 'src')
    math_build_directory: str = os.path.join(os.path.dirname(math_library_source_directory), 'build')
    math_include_directory: str = os.path.join(os.path.dirname(math_library_source_directory), 'include')
    math_library_directory: str = os.path.join(os.path.dirname(math_library_source_directory), 'lib')

    executable_name: str = 'present_addition'
    source_directory: str = os.path.join(os.getcwd(), 'sample_C++_code', 'src')

    build_directory: str = os.path.join(os.path.dirname(source_directory), 'build')
    math_library_path: str = os.path.join(math_library_directory, f'{math_library_name:s}.lib')

    try:

        compile.build_static_library_from_source(math_library_source_directory,
                                                 math_build_directory,
                                                 math_include_directory,
                                                 math_library_directory,
                                                 math_library_name)

        compile.build_executable_from_source(source_directory,
                                             build_directory,
                                             executable_name,
                                             [math_include_directory],
                                             [math_library_path])

    except Exception:
        print(traceback.format_exc())
