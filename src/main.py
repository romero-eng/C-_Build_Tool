import os
import traceback

import compile


if (__name__ == '__main__'):
    try:

        present_arithmetic: compile.CodeBase = \
            compile.CodeBase('present_arithmetic',
                             os.path.join(os.getcwd(), 'sample_C++_code'))

        #"""
        compile.build_executable_from_source(present_arithmetic,
                                             [compile.build_static_library_from_source(compile.CodeBase('Arithmetic',
                                                                                                        os.path.join(os.getcwd(), 'sample_C++_static_library')))])
        """
        compile.build_executable_from_source(present_arithmetic,
                                             [compile.build_dynamic_library_from_source(compile.CodeBase('Arithmetic',
                                                                                                         os.path.join(os.getcwd(), 'sample_C++_dynamic_library')),
                                                                                        ['ADD_EXPORTS'])])
        #"""

    except Exception:
        print(traceback.format_exc())
