from .base import BaseCommandTest
from exceptions import InvalidPath


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
