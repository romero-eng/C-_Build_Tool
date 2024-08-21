import os
import traceback

import compile


if (__name__ == '__main__'):

    #"""
    executable_name: str = 'present_addition'
    source_directory: str = os.path.join(os.getcwd(), 'sample_C++_code', 'src')
    
    build_directory: str = os.path.join(os.path.dirname(source_directory), 'build')
    math_include_directory: str = os.path.join(os.getcwd(), 'sample_C++_library', 'include')
    math_library_path: str = os.path.join(os.getcwd(), 'sample_C++_library', 'library', 'Math.lib')
    """
    library_name: str = 'Math'
    source_directory: str = os.path.join(os.getcwd(), 'sample_C++_library', 'src')

    build_directory: str = os.path.join(os.path.dirname(source_directory), 'build')
    include_directory: str = os.path.join(os.path.dirname(source_directory), 'include')
    library_directory: str = os.path.join(os.path.dirname(source_directory), 'library')
    #"""

    try:

        """
        compile.build_static_library_from_source(source_directory,
                                                 build_directory,
                                                 include_directory,
                                                 library_directory,
                                                 library_name,
                                                 'Debug',
                                                 'C++ 2020',
                                                 'Disable Compiler Extensions',
                                                 ['Treat warnings as errors',
                                                  'Avoid a lot of questionable coding practices',
                                                  'Avoid even more questionable coding practices',
                                                  'Follow Effective C++ Style Guidelines',
                                                  'Avoid potentially value-changing implicit conversions',
                                                  'Avoid potentially sign-changing implicit conversions for integers'])
        """
        compile.build_executable_from_source(source_directory,
                                             build_directory,
                                             executable_name,
                                             'Debug',
                                             'C++ 2020',
                                             'Disable Compiler Extensions',
                                             ['Treat warnings as errors',
                                              'Avoid a lot of questionable coding practices',
                                              'Avoid even more questionable coding practices',
                                              'Follow Effective C++ Style Guidelines',
                                              'Avoid potentially value-changing implicit conversions',
                                              'Avoid potentially sign-changing implicit conversions for integers'],
                                              [math_include_directory],
                                              [math_library_path])
        #"""

    except Exception:
        print(traceback.format_exc())
