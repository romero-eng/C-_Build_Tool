import os
import traceback

import compile


if (__name__ == '__main__'):

    executable_name: str = 'present_addition'
    repo_directory: str = os.path.join(os.getcwd(), 'sample_C++_code')

    """
    math_static_library_name: str = 'Math'
    math_static_library_repo_directory: str = os.path.join(os.getcwd(), 'sample_C++_static_library')
    """
    math_dynamic_library_name: str = 'Math'
    math_dynamic_library_repo_directory: str = os.path.join(os.getcwd(), 'sample_C++_dynamic_library')
    math_dynamic_library_preprocessor_variables: list[str] = ['ADD_EXPORTS']
    #"""

    try:
        """
        compile.build_static_library_from_source(math_static_library_repo_directory,
                                                 math_static_library_name)

        compile.build_executable_from_source(repo_directory,
                                             executable_name,
                                             [os.path.join(math_static_library_repo_directory, 'build', 'include')],
                                             [os.path.join(math_static_library_repo_directory, 'build', 'lib')],
                                             [math_static_library_name])
        """
        compile.build_dynamic_library_from_source(math_dynamic_library_repo_directory,
                                                  math_dynamic_library_name,
                                                  math_dynamic_library_preprocessor_variables)

        compile.build_executable_from_source(repo_directory,
                                             executable_name,
                                             [os.path.join(math_dynamic_library_repo_directory, 'build', 'include')],
                                             [os.path.join(math_dynamic_library_repo_directory, 'build', 'lib')],
                                             [math_dynamic_library_name])
        #"""

    except Exception:
        print(traceback.format_exc())
