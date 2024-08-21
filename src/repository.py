import os


def get_file_paths(source_directory: str) -> tuple[list[str], list[str], str, str]:

    build_directory: str = os.path.join(os.path.dirname(source_directory), 'build')
    include_directory: str = os.path.join(os.path.dirname(source_directory), 'include')
    library_directory: str = os.path.join(os.path.dirname(source_directory), 'library')

    relative_source_file_paths: list[str] = [os.path.join(root.split(source_directory)[1], file) for root, _, files in os.walk(source_directory) for file in files if os.path.splitext(file)[1] == '.cpp']  # noqa: E501
    relative_object_file_build_paths: list[str] = [f'{os.path.splitext(os.path.basename(file_path))[0]:s}.o' for file_path in relative_source_file_paths]                                                   # noqa: E501

    return (relative_source_file_paths,
            relative_object_file_build_paths,
            build_directory,
            include_directory,
            library_directory)
