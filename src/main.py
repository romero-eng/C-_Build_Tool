import os
import traceback

import compile


if (__name__ == '__main__'):

    math_library_name: str = 'Math'
    math_library_repo_directory: str = os.path.join(os.getcwd(), 'sample_C++_library')
    preprocessor_variables: list[str] = ['ADD_EXPORTS']

    """
    executable_name: str = 'present_addition'
    repo_directory: str = os.path.join(os.getcwd(), 'sample_C++_code')
    """

    try:

        """
        compile.build_static_library_from_source(math_library_repo_directory,
                                                 math_library_name)
        """

        #=======================================================================================================================================================================#
        #=======================================================================================================================================================================#

        compile.generate_object_files(math_library_repo_directory,
                                      preprocessor_variables = ['ADD_EXPORTS'])

        #=======================================================================================================================================================================#
        #=======================================================================================================================================================================#
        #=======================================================================================================================================================================#

        """
        compile.build_executable_from_source(repo_directory,
                                             executable_name,
                                             [os.path.join(math_library_repo_directory, 'build', 'include')],
                                             [os.path.join(math_library_repo_directory, 'build', 'lib')],
                                             [math_library_name])
        """

    except Exception:
        print(traceback.format_exc())
