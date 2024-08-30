import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlunsplit

from compile import CodeBase

def run_command(command_description: str,
                command: str,
                working_directory: Path | None = None,
                successful_return_code: int = 0) -> None:

    results: subprocess.CompletedProcess[bytes] = \
        subprocess.run(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       cwd=working_directory,
                       shell=True) if working_directory else subprocess.run(command,
                                                                            stdout=subprocess.PIPE,
                                                                            stderr=subprocess.PIPE)

    success: bool = results.returncode == successful_return_code

    formatted_results: list[str] = [f'\tWorking directory: {str(working_directory):s}'] if working_directory else []
    formatted_results.append(f'\tCommand: {command:s}')
    if results.stdout:
        formatted_results.append(f'\tOutput:\n\n{results.stdout.decode('utf-8'):s}')
    if results.stderr:
        formatted_results.append(f'\t Error:\n\n{results.stderr.decode('utf-8'):s}')

    msg_title: str = f'{command_description:s}: {'Succesful' if success else 'Failure':s}'
    msg = f'\n{msg_title:s}\n{'':{'-':s}>{len(msg_title):d}s}\n{'\n'.join(formatted_results):s}\n'  # noqa: E231

    if success:
        print(msg)
    else:
        raise Exception('\n' + msg)


if (__name__=='__main__'):

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
