import shutil
from pathlib import Path
from command import run_command
from urllib.parse import urlunsplit


def retrieve_repository_from_github(repository_directory: Path,
                                    username: str,
                                    branch: str | None = None) -> None:

    run_command('Test git clone',
                f'git clone {urlunsplit(('https',
                                         '.'.join(['github', 'com']),
                                         '/'.join([username, f'{repository_directory.stem:s}.git']),
                                         None, None)):s}',
                repository_directory.parent)

    if branch:
        run_command('Test git clone',
                    f'git checkout {branch:s}',
                    repository_directory)

    for child in repository_directory.iterdir():
        if child.is_file():
            Path.unlink(child)

    for child in repository_directory.iterdir():
        if child.is_dir():
            if child not in [repository_directory/'src',
                             repository_directory/'include',
                             repository_directory/'.git']:
                shutil.rmtree(child)
