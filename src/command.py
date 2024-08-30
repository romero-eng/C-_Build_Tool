import subprocess
from pathlib import Path


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
