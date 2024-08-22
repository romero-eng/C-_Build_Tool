import subprocess


def run_command(command_description: str,
                command: str,
                working_directory: str | None = None,
                successful_return_code: int = 0) -> bool:

    results: subprocess.CompletedProcess[bytes] = \
        subprocess.run(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       cwd=working_directory,
                       shell=True) if working_directory else subprocess.run(command,
                                                                            stdout=subprocess.PIPE,
                                                                            stderr=subprocess.PIPE)

    success: bool = results.returncode == successful_return_code

    formatted_results: list[str] = [f'\tWorking directory: {working_directory:s}'] if working_directory else []
    formatted_results.append(f'\tCommand: {command:s}')

    if results.stdout:
        formatted_results.append(f'\tOutput:\n\n{results.stdout.decode('utf-8'):s}')

    if results.stderr:
        formatted_results.append(f'\t Error:\n\n{results.stderr.decode('utf-8'):s}')

    title: str = f'{command_description:s}: {'Succesful' if success else 'Failure':s}'
    print(f'\n{title:s}\n{'':{'-':s}>{len(title):d}s}\n{'\n'.join(formatted_results):s}\n')  # noqa: E231, E501

    return success
