import shutil
from pathlib import Path

from compile import CodeBase
from git import retrieve_repository_from_github


if (__name__ == '__main__'):

    repository_directory: Path = Path.cwd()/'example_repos'/'fmt'

    if not repository_directory.exists():

        retrieve_repository_from_github(repository_directory,
                                        'fmtlib',
                                        '4.x')

        for child in repository_directory.iterdir():
            if child.is_file():
                Path.unlink(child)

        for child in repository_directory.iterdir():
            if child.is_dir():
                if child not in [repository_directory/'fmt', repository_directory/'.git']:
                    shutil.rmtree(child)

        shutil.move(repository_directory/'fmt', repository_directory/'src')

    fmt_codebase = \
        CodeBase('fmt',
                 repository_directory,
                 warnings=['Avoid a lot of questionable coding practices',
                           'Avoid even more questionable coding practices',
                           'Follow Effective C++ Style Guidelines',
                           'Avoid potentially value-changing implicit conversions',
                           'Avoid potentially sign-changing implicit conversions for integers'])

    fmt_codebase.generate_as_dependency(False)
