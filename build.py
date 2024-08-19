import os

import compile


if (__name__=='__main__'):

    executable_name: str = 'present_addition'
    source_directory: str = os.path.join('sample_C++_code', 'src')
    build_directory: str = os.path.join('sample_C++_code', 'build')
    cpp_files: list[str] = ['main', 'Add']

    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    compile.build_executable_from_source([os.path.join(source_directory, f'{file:s}.cpp') for file in cpp_files],
                                         [os.path.join(build_directory, f'{file:s}.o') for file in cpp_files],
                                         os.path.join(build_directory, executable_name),
                                         'Debug',
                                         'C++ 2020',
                                         'Disable Compiler Extensions',
                                         ['Treat warnings as errors',
                                          'Avoid a lot of questionable coding practices',
                                          'Avoid even more questionable coding practices',
                                          'Follow Effective C++ Style Guidelines',
                                          'Avoid potentially value-changing implicit conversions',
                                          'Avoid potentially sign-changing implicit conversions for integers'])
