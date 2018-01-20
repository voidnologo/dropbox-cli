from contextlib import closing
from pathlib import Path
import shlex

import dropbox

from exceptions import InvalidPath
from utils import Parser, set_docstring_from_parser, ParserError
from tree_fs import TreeFS


ENDC = '\033[0m'
BOLD = '\033[1m'
FG_BOLD_YELLOW = '\033[93m'
FG_CYAN = '\033[36m'


class DropboxCLIParsers:

    @classmethod
    def _get_parser(cls):
        parser = Parser(prog='get')
        parser.add_argument(
            '-t', '--target',
            nargs='*',
            help='File to download'
        )
        parser.add_argument(
            '-d', '--destination',
            nargs='*',
            help='Directory to download file to'
        )
        return parser


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

    @set_docstring_from_parser(DropboxCLIParsers._get_parser)
    def do_get(self, args):
        parser = DropboxCLIParsers._get_parser()
        try:
            args = parser.parse_args(shlex.split(args, posix=True))
        except ParserError:
            return
        try:
            self._get(' '.join(args.target), ' '.join(args.destination))
        except InvalidPath as e:
            self.fprint(str(e))

    def _get(self, file_path, download_location):
        target_node = self.tree.find_path(file_path)
        if target_node is None:
            raise InvalidPath(file_path)
        if not Path(download_location).exists():
            raise InvalidPath('Destination path {} does not exist.  Perhaps you need to create directories first?'.format(download_location))
        if not Path(download_location).is_dir():
            raise InvalidPath('Destination path {} is not a directory.'.format(download_location))
        meta_data, dropbox_file = self.client.files_download(target_node.get_path())
        with closing(dropbox_file) as db_file:
            content = db_file.content
        target = Path(download_location).joinpath(meta_data.name)
        try:
            with open(str(target), 'wb') as dl:
                dl.write(content)
        except FileNotFoundError as e:
            raise InvalidPath(download_location)

    @property
    def prompt(self):
        return '{}[{}] --> {}'.format(FG_BOLD_YELLOW, self.current_node.get_path(), ENDC)
