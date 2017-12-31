import os
from unittest import TestCase, mock

from exceptions import InvalidPath
from main import MainLoop
from tree import PathTree as Tree


class BaseCommandTest(TestCase):

    def setUp(self):
        self.main = MainLoop()
        self.main.root = self.create_tree()
        self.main.current_node = self.main.root

    def create_tree(self):
        """
        root           <folder>
        └─ n1          <folder>
           ├─ n2       <folder>
           │  ├─ n4    <file>
           │  └─ n5    <folder>
           └─ n3       <folder>
        """
        self.root = self._create_node('root', None, {'type': 'folder'})
        self.node1 = self._create_node('n1', self.root, {'type': 'folder'})
        self.node2 = self._create_node('n2', self.node1, {'type': 'folder'})
        self.node3 = self._create_node('n3', self.node1, {'type': 'folder'})
        self.node4 = self._create_node('n4', self.node2, {'type': 'file', 'modified': '2012-12-25', 'size': '12345'})
        self.node5 = self._create_node('n5', self.node2, {'type': 'folder'})
        return self.root

    def _create_node(self, val, parent, meta):
        node = Tree(val)
        if parent:
            parent.add_child(node)
        node.meta = meta
        return node


class CDCommandTests(BaseCommandTest):

    def test_cd_to_child(self):
        self.main._cd('n1')
        self.assertEqual(self.main.current_node, self.node1)

    def test_cd_dot_dot_moves_to_parent(self):
        self.main.current_node = self.node1
        self.main._cd('..')
        self.assertEqual(self.main.current_node, self.root)

    def test_cd_dot_dot_when_no_parent_stays_in_current_directory(self):
        self.main._cd('..')
        self.assertEqual(self.main.current_node, self.root)

    def test_trying_to_cd_into_a_file_sets_current_node_to_parent_of_file(self):
        self.main.current_node = self.node2
        self.main._cd('n4')
        self.assertEqual(self.main.current_node, self.node2)

    def test_cd_to_a_node_that_does_not_exist_raises_InvalidPath_exception(self):
        with self.assertRaises(InvalidPath):
            self.main._cd('nope')

    def test_cd_without_location_argument_raises_InvalidPath_exception(self):
        with self.assertRaises(InvalidPath):
            self.main._cd('')

    def test_cd_with_only_slash_goes_to_root_node(self):
        self.main._cd('/')
        self.assertEqual(self.main.current_node, self.root)

    def test_cd_to_an_absolute_path(self):
        self.main._cd('/root/n1/n2')
        self.assertEqual(self.main.current_node, self.node2)

    def test_cd_to_a_relative_path(self):
        self.main.current_node = self.node1
        self.main._cd('n2/n5')
        self.assertEqual(self.main.current_node, self.node5)


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
