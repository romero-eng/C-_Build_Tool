import codecs
import shutil
import traceback
import platform
from pathlib import Path

from command import run_command
from codebase import CodeBase, Dependency
from git import retrieve_repository_from_github
from compilation_constants import C_SOURCE_CODE_EXTENSIONS, C_HEADER_EXTENSIONS


def insert_lines(source_file_path: Path,
                 lines_to_insert: list[tuple[int, str]]) -> None:

    with codecs.open(source_file_path, 'r', 'utf-8') as source_file:
        source_code: list[str] = source_file.readlines()

    sorted_line_numbers: list[int] = \
        [(number if number >= 0 else len(source_code),
          text) for number, text in sorted(lines_to_insert,
                                           key=lambda line: line[0],
                                           reverse=True)]
    
    for line_number, new_line_text in sorted_line_numbers:
        source_code.insert(line_number, f'{new_line_text:s}\n')

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


def change_lines(source_file_path: Path,
                 lines_to_insert: list[tuple[int, str]]) -> None:

    with codecs.open(source_file_path, 'r', 'utf-8') as source_file:
        source_code_lines = source_file.readlines()

    for line_number, new_line_text in lines_to_insert:
        source_code_lines[line_number] = f'{new_line_text:s}\n'

    with codecs.open(source_file_path, 'w+', 'utf-8') as source_file:
        source_file.writelines(source_code_lines)


def insert_OS_guards(source_file_names: list[str],
                     main_path: Path,
                     OS_guard: str) -> None:
    
    def _insert(source_file_path: Path,
                OS_guard: str) -> None:

        with codecs.open(source_file_path, 'r', 'utf-8') as source_file:
            source_code: list[str] = source_file.readlines()

        source_code.insert(0, f'#ifdef {OS_guard:s}')
        source_code.append('#endif')

        with codecs.open(source_file_path, 'w+', 'utf-8') as source_file:
            source_file.writelines(source_code)

    source_file_path: Path

    for source_file_name in source_file_names:
    
        source_file_path = main_path/f'{source_file_name:s}.c'
        _insert(source_file_path, OS_guard)

        if source_file_path.with_suffix('.h').exists():
            _insert(source_file_path.with_suffix('.h'), OS_guard)


def get_fmt_dependency(example_repos_dir: Path) -> Dependency:

    fmt_dependency: Dependency

    (repository_directory,
     repo_already_exists) = \
        retrieve_repository_from_github(example_repos_dir,
                                        'fmt',
                                        'fmtlib')

    source_directory: Path = repository_directory/'src'
    include_directory: Path = repository_directory/'include'
    build_directory: Path = repository_directory/'build'
    library_directory: Path = build_directory/'lib'
    is_dynamic: bool = False

    if not repo_already_exists:

        for child in repository_directory.iterdir():
            if child.is_file():
                Path.unlink(child)

        for child in repository_directory.iterdir():
            if child.is_dir():
                if child not in [source_directory,
                                 include_directory,
                                 repository_directory/'.git']:
                    shutil.rmtree(child)

        remove_lines(source_directory/'fmt.cc',
                     [0, 89, 95, 96, 97, 132, 133, 134, 135])

        fmt_codebase = \
            CodeBase('fmt',
                     repository_directory,
                     warnings=['Avoid a lot of questionable coding practices',
                               'Avoid even more questionable coding practices'])

        fmt_dependency = fmt_codebase.generate_as_dependency(is_dynamic)

    else:

        fmt_dependency = \
            Dependency('fmt',
                       include_directory,
                       False,
                       is_dynamic,
                       library_directory)

    return fmt_dependency


def get_libusb_dependency(example_repos_dir: Path) -> Dependency:

    name: str = 'libusb'
    libusb_dependency: Dependency

    (repository_directory,
     repo_already_exists) = \
        retrieve_repository_from_github(example_repos_dir,
                                        name,
                                        name)

    source_directory: Path = repository_directory/'src'
    include_directory: Path = repository_directory/'include'
    build_directory: Path = repository_directory/'build'
    library_directory: Path = build_directory/'lib'
    is_dynamic: bool = False

    if not repo_already_exists:

        run_command('Run Autotools',
                    'C:\\msys64\\msys2_shell.cmd -ucrt64 -defterm -no-start -here -c "./bootstrap.sh"' if platform.system() == 'Windows' else './bootstrap.sh',
                    repository_directory)

        run_command('Run Configuration',
                    'C:\\msys64\\msys2_shell.cmd -ucrt64 -defterm -no-start -here -c "./configure"' if platform.system() == 'Windows' else './configure',
                    repository_directory)

        for child in repository_directory.iterdir():
            if child.is_file():
                if child.suffix not in (C_SOURCE_CODE_EXTENSIONS + C_HEADER_EXTENSIONS):
                    Path.unlink(child)
            elif child.is_dir():
                if child not in [repository_directory/name,
                                 repository_directory/'.git']:
                    shutil.rmtree(child)
        
        shutil.rmtree(repository_directory/name/'.deps')
        shutil.rmtree(repository_directory/name/'os'/'.deps')

        for child in (repository_directory/name).iterdir():
            if child.is_file():
                if child.suffix not in (C_SOURCE_CODE_EXTENSIONS + C_HEADER_EXTENSIONS):
                    Path.unlink(child)

        shutil.move(repository_directory/'config.h',
                    repository_directory/name/'config.h')

        shutil.copytree(repository_directory/name,
                        source_directory)

        shutil.rmtree(repository_directory/name)

        include_directory.mkdir()

        shutil.move(source_directory/f'{name:s}.h',
                    include_directory/f'{name:s}.h')
        
        change_lines(source_directory/'libusbi.h',
                     [(26, '#include "config.h"')])
        
        change_lines(source_directory/'os'/'darwin_usb.c',
                     [(21, '#include "../config.h"')])

        insert_OS_guards(['darwin_usb'],
                         source_directory/'os',
                         '__APPLE__')
        
        change_lines(source_directory/'os'/'events_posix.c',
                     [(20, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'threads_posix.c',
                     [(21, '#include "../libusbi.h"')])

        insert_OS_guards(['events_posix', 'threads_posix'],
                         source_directory/'os',
                         '_POSIX_VERSION')
        
        change_lines(source_directory/'os'/'events_windows.c',
                     [(20, '#include "../config.h"'),
                      (22, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'threads_windows.c',
                     [(21, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'windows_common.c',
                     [(24, '#include "../config.h"'),
                      (28, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'windows_usbdk.c',
                     [(23, '#include "../config.h"'),
                      (28, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'windows_winusb.c',
                     [(25, '#include "../config.h"'),
                      (33, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'linux_netlink.c',
                     [(23, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'linux_udev.c',
                     [(22, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'linux_usbfs.c',
                     [(24, '#include "../libusbi.h"')])

        insert_OS_guards(['linux_netlink', 'linux_udev', 'linux_usbfs'],
                         source_directory/'os',
                         '__LINUX__')
        
        change_lines(source_directory/'os'/'netbsd_usb.c',
                     [(18, '#include "../config.h"')])

        insert_OS_guards(['netbsd_usb'],
                         source_directory/'os',
                         '__NetBSD__')
        
        change_lines(source_directory/'os'/'null_usb.c',
                     [(18, '#include "../libusbi.h"')])
        
        change_lines(source_directory/'os'/'openbsd_usb.c',
                     [(18, '#include "../config.h"')])

        insert_OS_guards(['openbsd_usb'],
                         source_directory/'os',
                         '__OPENBSD__')
        
        change_lines(source_directory/'os'/'sunos_usb.c',
                     [(19, '#include "../config.h"')])

        insert_OS_guards(['sunos_usb'],
                         source_directory/'os',
                         '__sun')

        libusb_codebase: CodeBase = \
            CodeBase(name,
                     repository_directory,
                     language_standard='C 2018',
                     warnings=['Avoid a lot of questionable coding practices',
                               'Avoid even more questionable coding practices',
                               'Follow Effective C++ Style Guidelines',
                               'Avoid potentially value-changing implicit conversions',
                               'Avoid potentially sign-changing implicit conversions for integers'],
                     miscellaneous=[''])

        libusb_dependency = libusb_codebase.generate_as_dependency(is_dynamic)
    
    else:

        libusb_dependency = \
            Dependency(name,
                       include_directory,
                       False,
                       is_dynamic,
                       library_directory)

    return libusb_dependency


if (__name__ == '__main__'):

    #"""
    (repository_directory,
     repo_already_exists) = \
        retrieve_repository_from_github(Path.cwd()/'real_world_repos',
                                        'SDL',
                                        'libsdl-org',
                                        'release-2.30.x')

    source_directory: Path = repository_directory/'src'
    include_directory: Path = repository_directory/'include'

    if not repo_already_exists:

        for child in repository_directory.iterdir():
            if child.is_file():
                Path.unlink(child)

        for child in repository_directory.iterdir():
            if child.is_dir():
                if child not in [source_directory,
                                 include_directory,
                                 repository_directory/'.git']:
                    shutil.rmtree(child)

        things = \
            [(['SDL_ps2audio'],     source_directory/'audio'/'ps2',           'SDL_AUDIO_DRIVER_PS2'),
             (['SDL_fcitx'   ],     source_directory/'core'/'linux',          '__LINUX__'),
             (['SDL_wscons_kbd',
               'SDL_wscons_mouse'], source_directory/'core'/'openbsd',        '__OPENBSD__'),
             (['geniconv',
               'os2cp',
               'os2iconv',
               'sys2utf8',
               'test'],             source_directory/'core'/'os2'/'geniconv', '__OS2__'),
             (['SDL_poll'],         source_directory/'core'/'unix',           '__unix__')]

        for files, source_file_path, OS_guard in things:
            insert_OS_guards(files,
                             source_file_path,
                             OS_guard)

        rwopsromfs_file_path: Path = source_directory/'file'/'n3ds'/'SDL_rwopsromfs.c'

        insert_lines(rwopsromfs_file_path,
                     [(23, '#include <stdio.h>')])

        insert_lines(rwopsromfs_file_path.with_suffix('.h'),
                     [(21, '#include <stdio.h>')])
        
        insert_OS_guards(['hid'],
                         source_directory/'hidapi'/'linux',
                         '__LINUX__')
        
        insert_OS_guards(['hid'],
                         source_directory/'hidapi'/'mac',
                         '__APPLE__')
        
        insert_OS_guards(['SDL_syslocale'],
                         source_directory/'locale'/'android',
                         '__ANDROID__')
        
        insert_OS_guards(['SDL_sysurl'],
                         source_directory/'misc'/'android',
                         '__ANDROID__')
        
        insert_OS_guards(['SDL_syslocale'],
                         source_directory/'locale'/'emscripten',
                         '__EMSCRIPTEN__')
        
        insert_OS_guards(['SDL_sysurl'],
                         source_directory/'misc'/'emscripten',
                         '__EMSCRIPTEN__')
        
        insert_OS_guards(['SDL_sysurl'],
                         source_directory/'misc'/'riscos',
                         '__RISCOS__')
        
        insert_OS_guards(['SDL_syslocale'],
                         source_directory/'locale'/'n3ds',
                         '_3DS')
        
        insert_OS_guards(['SDL_syslocale'],
                         source_directory/'locale'/'vita',
                         'PSP2_SDK_VERSION')
        
        insert_OS_guards(['SDL_sysurl'],
                         source_directory/'misc'/'vita',
                         'PSP2_SDK_VERSION')
        
        insert_OS_guards(['SDL_gdk_main'],
                         source_directory/'main'/'gdk',
                         '__GDK__')

        insert_OS_guards(['SDL_sysurl'],
                         source_directory/'misc'/'unix',
                         '__unix__')

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
    
    SDL_codebase.add_dependency(get_libusb_dependency(Path.cwd()/'real_world_repos'))

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
