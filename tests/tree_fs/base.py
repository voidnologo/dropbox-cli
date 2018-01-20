from unittest import TestCase

from tree_fs import TreeFS
from tree import PathTree as Tree


class BaseCommandTest(TestCase):

    def setUp(self):
        tree = self.create_tree()
        self.main = TreeFS(tree)

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
