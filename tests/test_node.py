from unittest import TestCase

from tree import PathTree as Tree


class TreeTests(TestCase):

    def test_node_has_with_no_children_has_None(self):
        node = Tree('a')
        self.assertEqual(node.value, 'a')
        self.assertIsNone(node.children)

    def test_add_child(self):
        root = Tree('root')
        c1 = Tree('c1')
        root.add_child(c1)
        self.assertEqual(1, len(root.children))
        self.assertEqual(root.children, [c1])

    def test_iterating_over_node_yields_children(self):
        root = Tree('root')
        c1 = Tree('c1')
        root.add_child(c1)
        result = [x for x in root]
        self.assertEqual(1, len(result))
        self.assertEqual(result, [c1])

    def test_iterating_over_node_with_no_children_gives_nothing(self):
        root = Tree('root')
        result = [x for x in root]
        self.assertEqual(0, len(result))
        self.assertEqual(result, [])

    def test_adding_child_sets_parent(self):
        root = Tree('root')
        c1 = Tree('c1')
        root.add_child(c1)
        self.assertEqual(c1.parent, root)

    def test_get_child_returns_child_node(self):
        root = Tree('root')
        c1 = Tree('c1')
        root.add_child(c1)
        result = root.get_child('c1')
        self.assertEqual(result, c1)

    def test_get_child_returns_none_if_there_are_no_children(self):
        root = Tree('root')
        result = root.get_child('c1')
        self.assertIsNone(result)

    def test_get_child_returns_none_if_query_is_not_a_child(self):
        root = Tree('root')
        root.add_child(Tree('diff'))
        result = root.get_child('c1')
        self.assertIsNone(result)

    def test_nodes_are_equal_if_they_have_the_same_value(self):
        a1 = Tree('a')
        a2 = Tree('a')
        b = Tree('b')
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, b)

    def test_in_operator_works_for_checking_if_node_is_in_children(self):
        root = Tree('root')
        c1 = Tree('c1')
        root.add_child(c1)
        self.assertTrue('c1' in root.children)

    def test_adding_a_node_by_path(self):
        tree = Tree()
        tree.insert_path('/a')
        self.assertIsNotNone(tree.get_child('a'))

    def test_adding_a_nested_path(self):
        root = Tree()
        root.insert_path('/a/b')
        self.assertIsNone(root.parent)
        self.assertEqual(['a'], [_.value for _ in root.children])
        a = root.get_child('a')
        self.assertEqual(a.parent, root)
        print(a.children)
        self.assertEqual(['b'], [_.value for _ in a.children])
        b = a.get_child('b')
        self.assertEqual(b.parent, a)

    def test_adding_multiple_nodes_adds_to_children(self):
        root = Tree()
        root.insert_path('/a')
        root.insert_path('/b')
        self.assertEqual(['a', 'b'], [_.value for _ in root.children])
        a = root.get_child('a')
        self.assertEqual(a.parent, root)
        b = root.get_child('b')
        self.assertEqual(b.parent, root)

    def test_adding_multiple_nodes_adds_to_children_for_nested_paths(self):
        root = Tree()
        root.insert_path('/child/a')
        root.insert_path('/child/b')
        self.assertEqual(['child'], [_.value for _ in root.children])
        child = root.get_child('child')
        self.assertEqual(child.parent, root)
        a = child.get_child('a')
        self.assertEqual(a.parent, child)
        b = child.get_child('b')
        self.assertEqual(b.parent, child)

    def test_adding_a_node_more_than_once_only_creates_one_instance(self):
        root = Tree()
        root.insert_path('a')
        root.insert_path('a')
        print(root.children)
        self.assertEqual(1, len(root.children))
        self.assertEqual(['a'], [_.value for _ in root.children])

    def test_find_node(self):
        root = Tree()
        child = Tree('a')
        root.add_child(child)
        node = root.find_path('/a')
        self.assertEqual(node, child)

    def test_find_node_returns_None_if_node_does_not_exist(self):
        root = Tree()
        child = Tree('a')
        root.add_child(child)
        node = root.find_path('/b')
        self.assertIsNone(node)

    def test_find_nested_node(self):
        root = Tree()
        a = Tree('a')
        root.add_child(a)
        b = Tree('b')
        a.add_child(b)
        node = root.find_path('/a/b')
        self.assertEqual(node, b)
