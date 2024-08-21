import os


def get_file_paths(source_directory: str) -> tuple[list[str], list[str], str, str]:

    build_directory: str = os.path.join(os.path.dirname(source_directory), 'build')
    include_directory: str = os.path.join(os.path.dirname(source_directory), 'include')
    library_directory: str = os.path.join(os.path.dirname(source_directory), 'library')

    return (build_directory,
            include_directory,
            library_directory)
