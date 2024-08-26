import os
import traceback

import compile


if (__name__ == '__main__'):
    try:
        #"""
        arithmetic_library: compile.Dependency | None = \
            compile.build_static_library_from_source(compile.CodeBase('Arithmetic',
                                                                      os.path.join(os.getcwd(), 'sample_C++_static_library')))  # noqa: E501
        """
        arithmetic_library: compile.Dependency | None = \
            compile.build_dynamic_library_from_source(compile.CodeBase('Arithmetic',
                                                                       os.path.join(os.getcwd(), 'sample_C++_dynamic_library')),  # noqa: E501
                                                      ['ADD_EXPORTS'])
        #"""

        if arithmetic_library:

            present_arithmetic_exec: compile.CodeBase = \
                compile.CodeBase('present_arithmetic',
                                 os.path.join(os.getcwd(), 'sample_C++_code'))

            present_arithmetic_exec.dependencies.append(arithmetic_library)

            compile.build_executable_from_source(present_arithmetic_exec)

    except Exception:
        print(traceback.format_exc())
