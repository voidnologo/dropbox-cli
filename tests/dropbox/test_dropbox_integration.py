from unittest import TestCase

from .helper import DropboxHelper


class DropboxIntegrationTests(TestCase):

    def setUp(self):
        self.helper = DropboxHelper()
        self.helper.purge_files()

    def test_x(self):
        # helper.create_file_with_contents('a', 'test1.txt', 'This is a test file.')
        self.fail("x")
