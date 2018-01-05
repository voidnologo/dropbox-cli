import configparser
from functools import wraps
import json
import os

from dropbox import Dropbox

from config import CREDS_FILE


class TestConfigException(Exception):
    pass


class InvalidTestPath(Exception):
    pass


def restrict_test_paths(f):
    @wraps(f)
    def wrapper(self, folder_path, *args, **kwargs):
        if not folder_path.startswith(self.ALLOWED_PATH):
            folder_path = '{}/{}/'.format(self.ALLOWED_PATH, folder_path)
            # raise InvalidTestPath('{} does not meet path requirements.'.format(folder_path))
        f(self, folder_path, *args, **kwargs)
    return wrapper


class DropboxHelper():

    ALLOWED_PATH = '/dropbox-cli_test'

    def __init__(self):
        self.client = self.get_dropbox_client()

    def get_token_from_credential_file(self):
        if CREDS_FILE.exists():
            config_file = configparser.ConfigParser()
            config_file.read(CREDS_FILE)
            if 'TEST_CREDENTIALS' not in config_file.sections():
                raise TestConfigException('Cannot find test credentials')
            return config_file['TEST_CREDENTIALS']['oauth_key']
        raise TestConfigException('Config file does not exist')

    def get_token_from_env_variables(self):
        test_token = os.environ.get('DROPBOX_TEST_OAUTH', None)
        if test_token is None:
            raise TestConfigException('Test token not in environmental variables.')
        return test_token

    def get_dropbox_client(self):
        return Dropbox(self.dropbox_token)

    @property
    def dropbox_token(self):
        try:
            return self.get_token_from_env_variables()
        except TestConfigException:
            return self.get_token_from_credential_file()

    def purge_files(self):
        try:
            self.client.files_delete(self.ALLOWED_PATH)
        except Exception as e:
            print('YO:', e)
            pass

    @restrict_test_paths
    def create_files(self, folder_path, *files, **kwargs):
        for name in files:
            f = json.dumps(dict({
                'name': name,
                'from_test_clss': type(self).__name__,
            }, **kwargs))
            self.client.files_upload(f.encode(), "{}{}".format(folder_path, name))

    @restrict_test_paths
    def file_in_dropbox(self, folder_path, filename):
        try:
            return self.client.files_download("{}{}".format(folder_path, filename))
        except Exception:
            return False

    @restrict_test_paths
    def create_file_with_contents(self, folder_path, file_name, contents):
        content = contents.encode() if isinstance(contents, str) else contents
        self.client.files_upload(content, "{}{}".format(folder_path, file_name))
