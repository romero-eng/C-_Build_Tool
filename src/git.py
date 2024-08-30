import shutil
from pathlib import Path
from urllib.parse import urlunsplit

from compile import CodeBase
from command import run_command


if (__name__ == '__main__'):

    github_repo_name: str = 'fmt'
    github_username: str = 'fmtlib'
    github_branch: str = '4.x'

    repository_directory: Path = Path.cwd()/'example_repos'/github_repo_name

    if not repository_directory.exists():

        run_command('Test git clone',
                    f'git clone {urlunsplit(('https',
                                             '.'.join(['github', 'com']),
                                             '/'.join([github_username, f'{github_repo_name:s}.git']),
                                             None, None)):s}',
                    repository_directory.parent)

        run_command('Test git clone',
                    f'git checkout {github_branch:s}',
                    repository_directory)

        for child in repository_directory.iterdir():
            if child.is_file():
                Path.unlink(child)

        for child in repository_directory.iterdir():
            if child.is_dir():
                if child not in [repository_directory/github_repo_name, repository_directory/'.git']:
                    shutil.rmtree(child)

        shutil.move(repository_directory/github_repo_name, repository_directory/'src')

    fmt_codebase = \
        CodeBase('Arithmetic',
                 repository_directory,
                 warnings=['Avoid a lot of questionable coding practices',
                           'Avoid even more questionable coding practices',
                           'Avoid potentially value-changing implicit conversions'])

    fmt_codebase.generate_as_dependency(False)
