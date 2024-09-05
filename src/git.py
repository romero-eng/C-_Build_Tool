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
