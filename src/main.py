import os
import traceback

import compile
import repository


if (__name__ == '__main__'):

    library_name: str = 'Math'
    executable_name: str = 'present_addition'
    #source_directory: str = os.path.join(os.getcwd(), 'sample_C++_code', 'src')
    source_directory: str = os.path.join(os.getcwd(), 'sample_C++_library', 'src')

    (relative_source_file_paths,
     relative_object_file_build_paths,
     build_directory,
     include_directory,
     library_directory) = \
        repository.get_file_paths(source_directory)

    try:

        compile.build_static_library_from_source(source_directory,
                                                 build_directory,
                                                 include_directory,
                                                 library_directory,
                                                 relative_source_file_paths,
                                                 relative_object_file_build_paths,
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
                                             relative_source_file_paths,
                                             relative_object_file_build_paths,
                                             executable_name,
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

    except Exception:
        print(traceback.format_exc())
