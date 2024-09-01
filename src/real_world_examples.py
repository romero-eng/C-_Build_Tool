import shutil
from pathlib import Path

from compile import CodeBase, Dependency
from git import retrieve_repository_from_github


def get_fmt_dependency(example_repos_dir: Path) -> Dependency:

    name: str = 'fmt'
    repository_directory: Path = example_repos_dir/name
    fmt_dependency: Dependency

    if not repository_directory.exists():

        retrieve_repository_from_github(repository_directory,
                                        'fmtlib')

        for child in repository_directory.iterdir():
            if child.is_file():
                Path.unlink(child)

        for child in repository_directory.iterdir():
            if child.is_dir():
                if child not in [repository_directory/'src',
                                 repository_directory/'include',
                                 repository_directory/'.git']:
                    shutil.rmtree(child)

        shutil.move(repository_directory/'include'/name, repository_directory/'src')
        shutil.rmtree(repository_directory/'include')

        with open(repository_directory/'src'/'fmt.cc', 'r') as C_Plus_Plus_Source_File:
            source_code_lines = C_Plus_Plus_Source_File.readlines()

        source_code_lines.pop(127)
        source_code_lines.pop(126)
        source_code_lines.pop(125)
        source_code_lines.pop(124)
        source_code_lines.pop(89)
        source_code_lines.pop(88)
        source_code_lines.pop(87)
        source_code_lines.pop(81)
        source_code_lines.pop(0)

        with open(repository_directory/'src'/'fmt.cc', 'w') as C_Plus_Plus_Source_File:
            C_Plus_Plus_Source_File.writelines(source_code_lines)

        fmt_codebase = \
            CodeBase(name,
                     repository_directory,
                     warnings=['Avoid a lot of questionable coding practices',
                               'Avoid even more questionable coding practices',
                               'Follow Effective C++ Style Guidelines',
                               'Avoid potentially value-changing implicit conversions',
                               'Avoid potentially sign-changing implicit conversions for integers'])

        fmt_dependency = fmt_codebase.generate_as_dependency(False)

    else:

        fmt_dependency = \
            Dependency(name,
                       False,
                       repository_directory/'build'/'include',
                       repository_directory/'build'/'lib')

    return fmt_dependency


if (__name__ == '__main__'):

    fmt_dependency: Dependency = get_fmt_dependency(Path.cwd()/'example_repos')
    print(fmt_dependency)
