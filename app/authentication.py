from sentinelsat.sentinel import SentinelAPI



def read_authentication_file(auth_file_dir):
    """This function reads .txt file that contains the user's login
    and password to authenticate the access to the COPERNICUS SCIHUB platform.
    :param auth_file_dir: directory of authentication file. 
    """

    with open(auth_file_dir) as f:
        login, password = f.readlines()
        return login.strip(), password.strip()



def authenticate_access(auth_file_dir):
    """This function uses the user's login and password to authenticate
    the access to COPERNICUS SCIHUB platform.
    :param auth_file_dir: directory of authentication file.
    """

    login, password = read_authentication_file(auth_file_dir)

    return SentinelAPI(login,
            password,
            'https://apihub.copernicus.eu/apihub',
            show_progressbars=True)
