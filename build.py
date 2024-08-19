import os

import compile


if (__name__=='__main__'):

    executable_name = 'present_addition'
    cpp_files = ['main', 'Add']

    if not os.path.exists(os.path.join('sample_C++_code', 'build')):
        os.mkdir(os.path.join('sample_C++_code', 'build'))

    compile.build_executable_from_source([os.path.join('sample_C++_code', 'src', f'{file:s}.cpp') for file in cpp_files],
                                         [os.path.join('sample_C++_code', 'build', f'{file:s}.o') for file in cpp_files],
                                         os.path.join('sample_C++_code', 'build', executable_name),
                                         'Debug',
                                         'C++ 2020',
                                         'Disable Compiler Extensions',
                                         ['Treat warnings as errors',
                                          'Avoid a lot of questionable coding practices',
                                          'Avoid even more questionable coding practices',
                                          'Follow Effective C++ Style Guidelines',
                                          'Avoid potentially value-changing implicit conversions',
                                          'Avoid potentially sign-changing implicit conversions for integers'])
