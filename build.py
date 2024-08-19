import os

import compile


if (__name__=='__main__'):

    executable_name = 'present_addition'
    cpp_files = ['main', 'Add']

    build_configuration: str = 'Debug'
    language_standard: str = 'C++ 2020'
    miscellaneous: str = 'Disable Compiler Extensions'
    warnings: list[str] = \
        ['Treat warnings as errors',
          'Avoid a lot of questionable coding practices',
          'Avoid even more questionable coding practices',
          'Follow Effective C++ Style Guidelines',
          'Avoid potentially value-changing implicit conversions',
          'Avoid potentially sign-changing implicit conversions for integers']

    if not os.path.exists('build'):
        os.mkdir('build')

    compile.build_executable_from_source([os.path.join('src', f'{file:s}.cpp') for file in cpp_files],
                                         [os.path.join('build', f'{file:s}.o') for file in cpp_files],
                                         os.path.join('build', executable_name),
                                         build_configuration,
                                         language_standard,
                                         miscellaneous,
                                         warnings)
