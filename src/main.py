import os
import traceback

import compile


if (__name__ == '__main__'):

    present_arithmetic: compile.CodeBase = \
        compile.CodeBase('present_arithmetic',
                         os.path.join(os.getcwd(), 'sample_C++_code'))

    try:

        """
        arithmetic_library: compile.CodeBase = \
            compile.CodeBase('Arithmetic',
                             os.path.join(os.getcwd(), 'sample_C++_static_library'))

        compile.build_static_library_from_source(arithmetic_library)
        compile.build_executable_from_source(present_arithmetic,
                                             [arithmetic_library.build_directory/'include'],
                                             [arithmetic_library.build_directory/'lib'],
                                             [arithmetic_library.name])
        """
        arithmetic_library: compile.CodeBase = \
            compile.CodeBase('Arithmetic',
                             os.path.join(os.getcwd(), 'sample_C++_dynamic_library'))

        compile.build_dynamic_library_from_source(arithmetic_library,
                                                  ['ADD_EXPORTS'])
        compile.build_executable_from_source(present_arithmetic,
                                             [arithmetic_library.build_directory/'include'],
                                             [arithmetic_library.build_directory/'lib'],
                                             [arithmetic_library.name])
        #"""

    except Exception:
        print(traceback.format_exc())
