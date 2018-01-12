from contextlib import closing
from pathlib import Path

import dropbox

from exceptions import InvalidPath
from tree_fs import TreeFS


ENDC = '\033[0m'
BOLD = '\033[1m'
FG_BOLD_YELLOW = '\033[93m'
FG_CYAN = '\033[36m'


class DropboxCLI(TreeFS):
    welcome = 'Dropbox-CLI'
    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def __init__(self, tree, *args, token=None, **kwargs):  # flake8: noqa
        assert token is not None, 'Dropbox oauth token required to use Dropbox'
        self.client = dropbox.Dropbox(token)
        super().__init__(tree, *args, **kwargs)

    def preloop(self):
        print(self.welcome)

    def do_get(self, args):
        try:
            self._get(args)
        except InvalidPath as e:
            self.fprint(str(e))

    def _get(self, file_path, download_location):
        if not self.tree.find_path(file_path):
            raise InvalidPath(file_path)
        if not Path(download_location).exists():
            raise InvalidPath('Destination path {} does not exist.  Perhaps you need to create directories first?'.format(download_location))
        if not Path(download_location).is_dir():
            raise InvalidPath('Destination path {} is not a directory.'.format(download_location))
        meta_data, dropbox_file = self.client.files_download(file_path)
        with closing(dropbox_file) as db_file:
            content = db_file.content
        target = Path(download_location).joinpath(meta_data.name)
        try:
            with open(target, 'wb') as dl:
                dl.write(content)
        except FileNotFoundError as e:
            raise InvalidPath(download_location)

    @property
    def prompt(self):
        return '{}[{}] --> {}'.format(FG_BOLD_YELLOW, self.current_node.get_path(), ENDC)
