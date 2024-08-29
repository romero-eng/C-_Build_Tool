from urllib.parse import urlunsplit

if (__name__=='__main__'):

    github_username: str = 'romero-eng'
    github_repo_name: str = 'MinGW_Build_Tool'

    print(f'\ngit clone {urlunsplit(('https',
                                     '.'.join(['github', 'com']),
                                     '/'.join([github_username, f'{github_repo_name:s}.git']),
                                     None, None)):s}\n')
