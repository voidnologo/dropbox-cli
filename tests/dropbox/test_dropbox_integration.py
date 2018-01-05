from pathlib import Path
import tempfile
from unittest import TestCase

from .helper import DropboxHelper
from dropbox_cli import DropboxCLI
from main import init_tree_from_dropbox_account


class DropboxIntegrationTests(TestCase):

    def setUp(self):
        self.helper = DropboxHelper()
        self.helper.purge_files()
        self.populate_fs()
        self.tree = init_tree_from_dropbox_account(token=self.helper.dropbox_token)
        self.dropbox_tree = DropboxCLI(self.tree, token=self.helper.dropbox_token)

    def test_download_file(self):
        path = self.build_path('a/b/c/c1.txt')
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.dropbox_tree._get(path, tmpdirname)
            downloaded_files = [x.name for x in Path(tmpdirname).iterdir()]
        expected = ['c1.txt']
        self.assertEqual(downloaded_files, expected)

    def build_path(self, path):
        return '{}/{}'.format(DropboxHelper.ALLOWED_PATH, path)

    def populate_fs(self):
        """
        dropbox-cli_test
        └─ a
           ├─ b
           │  └─ c
           │     ├─ c1.txt
           │     └─ c2.txt
           └─ d
              └─ d1.txt
        """
        self.helper.create_files('a/b/c', 'c1.txt')
        self.helper.create_files('a/b/c', 'c2.txt')
        self.helper.create_files('a/d', 'd1.txt')
