import os
import traceback

import compile


if (__name__ == '__main__'):

    present_arithmetic: compile.CodeBase = \
        compile.CodeBase('present_arithmetic',
                         os.path.join(os.getcwd(), 'sample_C++_code'))

    static_arithmetic: compile.CodeBase = \
        compile.CodeBase('Arithmetic',
                         os.path.join(os.getcwd(), 'sample_C++_static_library'))

    dynamic_arithmetic: compile.CodeBase = \
        compile.CodeBase('Arithmetic',
                         os.path.join(os.getcwd(), 'sample_C++_dynamic_library'))

    try:

        """
        compile.build_static_library_from_source(static_arithmetic)
        compile.build_executable_from_source(present_arithmetic,
                                             [os.path.join(static_arithmetic.repository_directory, 'build', 'include')],
                                             [os.path.join(static_arithmetic.repository_directory, 'build', 'lib')],
                                             [static_arithmetic.name])
        """
        compile.build_dynamic_library_from_source(dynamic_arithmetic,
                                                  ['ADD_EXPORTS'])
        compile.build_executable_from_source(present_arithmetic,
                                             [os.path.join(dynamic_arithmetic.repository_directory, 'build', 'include')],  # noqa: E501
                                             [os.path.join(dynamic_arithmetic.repository_directory, 'build', 'lib')],
                                             [dynamic_arithmetic.name])
        #"""  # noqa: E265

    except Exception:
        print(traceback.format_exc())
