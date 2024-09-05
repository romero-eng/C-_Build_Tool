import codecs
import shutil
import traceback
import platform
from pathlib import Path

from codebase import CodeBase, Dependency
from git import retrieve_repository_from_github


def insert_lines(source_file_path: Path,
                 lines_to_insert: tuple[int, str]) -> None:

    with codecs.open(source_file_path, 'r', 'utf-8') as source_file:
        source_code: list[str] = source_file.readlines()

    sorted_line_numbers: list[int] = \
        [(number if number >= 0 else len(source_code),
          text) for number, text in sorted(lines_to_insert,
                                           key=lambda line: line[0],
                                           reverse=True)]
    
    for line_number, new_line_text in sorted_line_numbers:
        source_code.insert(line_number, new_line_text)

    with codecs.open(source_file_path, 'w+', 'utf-8') as source_file:
        source_file.writelines(source_code)


def remove_lines(source_file_path: Path,
                 line_numbers: list[int] | int) -> None:

    if isinstance(line_numbers, int):
        line_numbers = [line_numbers]

    with codecs.open(source_file_path, 'r', 'utf-8') as source_file:
        source_code_lines = source_file.readlines()

    for line_number in sorted(line_numbers, reverse=True):
        source_code_lines.pop(line_number)

    with codecs.open(source_file_path, 'w+', 'utf-8') as source_file:
        source_file.writelines(source_code_lines)


def insert_OS_guards(source_file_names: list[str],
                     main_path: Path,
                     OS_guard: str) -> None:

    for source_file_name in source_file_names:
    
        source_file_path = main_path/f'{source_file_name:s}.c'
        insert_lines(source_file_path,
                     [( 0, f'#ifdef {OS_guard:s}'),
                      (-1, '#endif')])

        if source_file_path.with_suffix('.h').exists():
            insert_lines(source_file_path.with_suffix('.h'),
                         [( 0, f'#ifdef {OS_guard:s}'),
                          (-1, '#endif')])


def get_fmt_dependency(example_repos_dir: Path) -> Dependency:

    name: str = 'fmt'
    repository_directory: Path = example_repos_dir/name
    fmt_dependency: Dependency

    if not repository_directory.exists():

        retrieve_repository_from_github(repository_directory,
                                        'fmtlib')

        remove_lines(repository_directory/'src'/'fmt.cc',
                     [0, 89, 95, 96, 97, 132, 133, 134, 135])

        fmt_codebase = \
            CodeBase(name,
                     repository_directory,
                     warnings=['Avoid a lot of questionable coding practices',
                               'Avoid even more questionable coding practices'])

        fmt_dependency = fmt_codebase.generate_as_dependency(False)

    else:

        fmt_dependency = \
            Dependency(name,
                       False,
                       repository_directory/'build'/'include',
                       repository_directory/'build'/'lib')

    return fmt_dependency


if (__name__ == '__main__'):

    #"""
    repository_directory: Path = Path.cwd()/'real_world_repos'/'SDL'

    if not repository_directory.exists():

        retrieve_repository_from_github(repository_directory,
                                        'libsdl-org',
                                        'release-2.30.x')

        insert_OS_guards(['SDL_ps2audio'],
                         repository_directory/'src'/'audio'/'ps2',
                         'SDL_AUDIO_DRIVER_PS2')

        insert_OS_guards(['SDL_fcitx'],
                         repository_directory/'src'/'core'/'linux',
                         '__LINUX__') 

        insert_OS_guards(['SDL_wscons_kbd', 'SDL_wscons_mouse'],
                         repository_directory/'src'/'core'/'openbsd',
                         '__OPENBSD__') 

        insert_OS_guards(['geniconv', 'os2cp', 'os2iconv', 'sys2utf8', 'test'],
                         repository_directory/'src'/'core'/'os2'/'geniconv',
                         '__OS2__') 

        insert_OS_guards(['SDL_poll'],
                         repository_directory/'src'/'core'/'unix',
                         '__unix__')
        
        rwopsromfs_file_path: Path = repository_directory/'src'/'file'/'n3ds'/'SDL_rwopsromfs.c'

        insert_lines(rwopsromfs_file_path,
                     [(23, '#include <stdio.h>')])

        insert_lines(rwopsromfs_file_path.with_suffix('.h'),
                     [(21, '#include <stdio.h>')])

    SDL_codebase = \
            CodeBase('SDL',
                     repository_directory,
                     language_standard='C 2018',
                     warnings=['Avoid a lot of questionable coding practices',
                               'Avoid even more questionable coding practices',
                               'Follow Effective C++ Style Guidelines',
                               'Avoid potentially value-changing implicit conversions',
                               'Avoid potentially sign-changing implicit conversions for integers'],
                     miscellaneous='')

    SDL_codebase.generate_as_dependency(True)
    """
    Test_codebase: CodeBase | None = None

    try:

        fmt_dependency: Dependency = \
            get_fmt_dependency(Path.cwd()/'real_world_repos')
    
        Test_codebase = \
            CodeBase('test',
                     Path.cwd()/'real_world_repos'/'Test',
                     warnings=['Avoid a lot of questionable coding practices',
                               'Avoid even more questionable coding practices'])
    
        Test_codebase.add_dependency(fmt_dependency)
        Test_codebase.generate_as_executable()

    except Exception:
        print(traceback.format_exc())

    else:
        Test_codebase.test_executable()

    finally:
        if Test_codebase:
            if Test_codebase.build_directory.exists():
                shutil.rmtree(Test_codebase.build_directory)
    #"""
