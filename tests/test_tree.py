from unittest import TestCase

from tree import Node


class TreeTests(TestCase):

    def test_node_has_with_no_children_has_None(self):
        node = Node('a')
        self.assertEqual(node.value, 'a')
        self.assertIsNone(node.children)

    def test_add_child(self):
        root = Node('root')
        c1 = Node('c1')
        root.add_child(c1)
        self.assertEqual(1, len(root.children))
        self.assertEqual(root.children, [c1])

    def test_iterating_over_node_yields_children(self):
        root = Node('root')
        c1 = Node('c1')
        root.add_child(c1)
        result = [x for x in root]
        self.assertEqual(1, len(result))
        self.assertEqual(result, [c1])

    def test_iterating_over_node_with_no_children_gives_nothing(self):
        root = Node('root')
        result = [x for x in root]
        self.assertEqual(0, len(result))
        self.assertEqual(result, [])

    def test_children_know_about_their_parent(self):
        root = Node('root')
        c1 = Node('c1')
        root.add_child(c1)
        self.assertEqual(c1.parent, root)
