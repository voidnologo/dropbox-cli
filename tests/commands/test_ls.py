import os
from unittest import mock

from .base import BaseCommandTest


class LSCommandTests(BaseCommandTest):

    def test_initial_path(self):
        self.assertEqual('[/root] --> ', self.main.prompt)

    @mock.patch('shutil.get_terminal_size')
    def test_ls(self, term_size):
        term_size.return_value = os.terminal_size((80, 40))
        output = self.main._ls()
        self.assertEqual(list(output), ['n1/' + (' ' * 75)])

    @mock.patch('shutil.get_terminal_size')
    def test_ls_folders_have_trailing_slash_and_files_do_not(self, term_size):
        term_size.return_value = os.terminal_size((80, 40))
        self.main.current_node = self.node2
        output = self.main._ls()
        self.assertEqual(list(output), ['n4    n5/' + (' ' * 69)])

    @mock.patch('shutil.get_terminal_size')
    def test_ls_size_of_columns_changes_based_on_longest_len_of_names(self, term_size):
        term_size.return_value = os.terminal_size((80, 40))
        a = self._create_node('a' * 10, self.root, {'type': 'folder'})
        b = self._create_node('b' * 8, self.root, {'type': 'folder'})
        c = self._create_node('c' * 4, self.root, {'type': 'folder'})
        output = self.main._ls()
        expected = ['aaaaaaaaaa/   bbbbbbbb/     cccc/         n1/' + (' ' * 25)]
        self.assertEqual(expected, list(output))
        a.value = 'a' * 5
        b.value = 'b' * 3
        c.value = 'c'
        output = self.main._ls()
        expected = ['aaaaa/   bbb/     c/       n1/' + (' ' * 42)]
        self.assertEqual(expected, list(output))

    @mock.patch('shutil.get_terminal_size')
    def test_ls_changing_size_of_terminal_changes_number_of_columns(self, term_size):
        self._create_node('a' * 10, self.root, {'type': 'folder'})
        self._create_node('b' * 10, self.root, {'type': 'folder'})
        self._create_node('c' * 10, self.root, {'type': 'folder'})
        term_size.return_value = os.terminal_size((80, 40))
        output = list(self.main._ls())
        expected = ['aaaaaaaaaa/   bbbbbbbbbb/   cccccccccc/   n1/' + (' ' * 25)]
        self.assertEqual(1, len(output))
        self.assertEqual(expected, output)
        term_size.return_value = os.terminal_size((30, 40))
        output = list(self.main._ls())
        expected = [
            'aaaaaaaaaa/   bbbbbbbbbb/   ',
            'cccccccccc/   n1/           '
        ]
        self.assertEqual(2, len(output))
        self.assertEqual(expected, output)
