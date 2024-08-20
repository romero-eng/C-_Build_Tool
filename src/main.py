import os

import compile
import repository


if (__name__ == '__main__'):

    executable_name: str = 'present_addition'
    source_directory: str = os.path.join(os.getcwd(), 'sample_C++_code', 'src')

    (source_file_paths,
     object_file_paths,
     executable_path) = \
        repository.get_file_paths(source_directory,
                                  executable_name)

    compile.build_executable_from_source(source_file_paths,
                                         object_file_paths,
                                         executable_path,
                                         'Debug',
                                         'C++ 2020',
                                         'Disable Compiler Extensions',
                                         ['Treat warnings as errors',
                                          'Avoid a lot of questionable coding practices',
                                          'Avoid even more questionable coding practices',
                                          'Follow Effective C++ Style Guidelines',
                                          'Avoid potentially value-changing implicit conversions',
                                          'Avoid potentially sign-changing implicit conversions for integers'])
