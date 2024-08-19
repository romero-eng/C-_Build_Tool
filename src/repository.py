import os


def get_file_paths(source_directory: str,
                   executable_name: str) -> tuple[list[str], list[str], str]:

    build_directory: str = os.path.join(os.path.dirname(source_directory), 'build')

    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    cpp_file_paths: list[str] = [os.path.join(root, file) for root, _, files in os.walk(source_directory) for file in files if os.path.splitext(file)[1] == '.cpp']  # noqa: E501
    object_file_paths: list[str] = [f'{os.path.join(build_directory, os.path.splitext(os.path.basename(file_path))[0]):s}.o' for file_path in cpp_file_paths]        # noqa: E501
    executable_path: str = os.path.join(build_directory, f'{executable_name:s}.exe')

    return (cpp_file_paths, object_file_paths, executable_path)
