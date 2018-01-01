#!python

import configparser
import os
from pathlib import Path


try:
    CREDS_PATH = Path.home().joinpath('.dropbox_cli')
except AttributeError:
    CREDS_PATH = Path(os.path.expanduser('~')).joinpath('.dropbox_cli')
CREDS_FILE = CREDS_PATH.joinpath('dropbox_cli.ini')


def get_keys():
    app_key = input('What is your app key? > ')
    secret_key = input('What is your secret key? > ')
    return app_key, secret_key


def create_configfile():
    if not CREDS_PATH.is_dir():
        CREDS_PATH.mkdir()
    app_key, secret_key = get_keys()
    parser = configparser.ConfigParser()
    parser['APP_CREDS'] = {
        'app_key': app_key,
        'secret_app_key': secret_key
    }
    print('Creating config file at: {}'.format(CREDS_PATH))
    with open(CREDS_FILE, 'w') as configfile:
        parser.write(configfile)


def verify_config_file():
    if not CREDS_FILE.exists():
        create_configfile()
        return 'created'
    return 'exists'


if __name__ == '__main__':
    print(verify_config_file())
