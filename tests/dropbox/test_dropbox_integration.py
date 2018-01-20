from pathlib import Path
import tempfile
from unittest import TestCase

from .helper import DropboxHelper
from dropbox_cli import DropboxCLI
from exceptions import InvalidPath
from main import init_tree_from_dropbox_account


class DropboxIntegrationTests(TestCase):

    def setUp(self):
        self.helper = DropboxHelper()
        self.helper.purge_files()
        self.populate_fs()
        self.tree, _ = init_tree_from_dropbox_account(token=self.helper.dropbox_token)
        self.dropbox_tree = DropboxCLI(self.tree, token=self.helper.dropbox_token)

    def test_download_to_a_chosen_directory_on_local_system(self):
        path = self.build_path('a/b/c/c1.txt')
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.dropbox_tree._get(path, tmpdirname)
            downloaded_files = [x.name for x in Path(tmpdirname).iterdir()]
        expected = ['c1.txt']
        self.assertEqual(downloaded_files, expected)

    def test_download_path_that_doesnt_exist(self):
        path = self.build_path('a/x/nonexistant.txt')
        with self.assertRaises(InvalidPath) as exc:
            with tempfile.TemporaryDirectory() as tmpdirname:
                self.dropbox_tree._get(path, tmpdirname)
        expected = 'Invalid Path: {}'.format(path)
        self.assertEqual(str(exc.exception), expected)

    def test_local_directory_does_not_exist(self):
        path = self.build_path('a/b/c/c2.txt')
        with self.assertRaises(InvalidPath) as exc:
            with tempfile.TemporaryDirectory() as tmpdirname:
                invalid_target = Path(tmpdirname).joinpath('invalid')
                self.dropbox_tree._get(path, invalid_target)
        expected = 'Invalid Path: Destination path {} does not exist.  '.format(invalid_target)
        expected += 'Perhaps you need to create directories first?'
        self.assertEqual(str(exc.exception), expected)

    def test_download_destination_is_not_a_directory(self):
        path = self.build_path('a/b/c/c2.txt')
        with self.assertRaises(InvalidPath) as exc:
            with tempfile.TemporaryDirectory() as tmpdirname:
                invalid_target = Path(tmpdirname).joinpath('invalid.txt')
                invalid_target.touch()
                self.dropbox_tree._get(path, invalid_target)
        expected = 'Invalid Path: Destination path {} is not a directory.'.format(invalid_target)
        self.assertEqual(str(exc.exception), expected)

    def test_if_destination_not_provided_downloads_to_project_download_directory(self):
        pass

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
