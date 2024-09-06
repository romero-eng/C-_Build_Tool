from pathlib import Path
from command import run_command
from urllib.parse import urlunsplit


def retrieve_repository_from_github(parent_directory: Path,
                                    repository_name: str,
                                    username: str,
                                    branch: str | None = None,
                                    domains: list[str] = ['github', 'com']) -> tuple[Path, bool]:

    repository_directory: Path = parent_directory/repository_name
    repo_already_exists: bool = repository_directory.exists()

    if not repo_already_exists:

        run_command(f'Clone the \'{repository_name:s}\' Repository',
                    f'git clone {urlunsplit(('https',
                                             '.'.join(domains),
                                             '/'.join([username, f'{repository_name:s}.git']),
                                             None, None)):s}',
                    parent_directory)

        if branch:
            run_command(f'Switch to the \'{branch:s}\' of the \'{repository_name:s}\' Repository',
                        f'git checkout {branch:s}',
                        repository_directory)

    return (repository_directory,
            repo_already_exists)
