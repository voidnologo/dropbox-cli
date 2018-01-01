from unittest import TestCase

from tree import PathTree as Tree


class TreeTests(TestCase):

    def test_node_has_with_no_children_has_None(self):
        node = Tree('a')
        self.assertEqual(node.value, 'a')
        self.assertEqual(node.children, [])

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

    def test_adding_a_node_by_absolute_path(self):
        tree = Tree('root')
        tree.insert_path('/root/a')
        node = tree.get_child('a')
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 'a')

    def test_insert_path_adding_a_nested_absolute_path(self):
        root = Tree('root')
        root.insert_path('/root/a/b')
        self.assertIsNone(root.parent)
        self.assertEqual(['a'], [_.value for _ in root.children])
        a = root.get_child('a')
        self.assertEqual(a.parent, root)
        self.assertEqual(['b'], [_.value for _ in a.children])
        b = a.get_child('b')
        self.assertEqual(b.parent, a)

    def test_insert_path_adding_a_absolute_path_from_a_nested_node(self):
        root = Tree('root')
        c1 = Tree('c1')
        root.add_child(c1)
        c1.insert_path('/root/a/b')
        root.formated_print()
        self.assertIsNone(root.parent)
        self.assertEqual(['c1', 'a'], [_.value for _ in root.children])
        a = root.get_child('a')
        self.assertEqual(a.parent, root)
        self.assertEqual(['b'], [_.value for _ in a.children])
        b = a.get_child('b')
        self.assertEqual(b.parent, a)

    def test_insert_path_adding_a_node_by_relative_path(self):
        tree = Tree('root')
        tree.insert_path('a')
        node = tree.get_child('a')
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 'a')

    def test_insert_path_adding_a_nested_relative_path(self):
        root = Tree('root')
        root.insert_path('a/b')
        self.assertIsNone(root.parent)
        self.assertEqual(['a'], [_.value for _ in root.children])
        a = root.get_child('a')
        self.assertEqual(a.parent, root)
        self.assertEqual(['b'], [_.value for _ in a.children])
        b = a.get_child('b')
        self.assertEqual(b.parent, a)

    def test_insert_path_multiple_nodes_adds_to_children(self):
        root = Tree('root')
        root.insert_path('/root/a')
        root.insert_path('/root/b')
        self.assertEqual(['a', 'b'], [_.value for _ in root.children])
        a = root.get_child('a')
        self.assertEqual(a.parent, root)
        b = root.get_child('b')
        self.assertEqual(b.parent, root)

    def test_insert_path_multiple_nodes_adds_to_children_for_nested_paths(self):
        root = Tree('root')
        root.insert_path('/root/child/a')
        root.insert_path('/root/child/b')
        self.assertEqual(['child'], [_.value for _ in root.children])
        child = root.get_child('child')
        self.assertEqual(child.parent, root)
        a = child.get_child('a')
        self.assertEqual(a.parent, child)
        b = child.get_child('b')
        self.assertEqual(b.parent, child)

    def test_origin_from_path_returns_relative_to_root_if_path_starts_with_slash(self):
        root = Tree('root')
        child = Tree('child')
        root.add_child(child)
        node, parts = child._origin_from_path('/root/child')
        self.assertEqual(root, node)
        self.assertEqual(['child'], parts)

    def test_origin_from_path_returns_relative_to_current_node_if_path_does_not_start_with_slash(self):
        root = Tree('root')
        child1 = Tree('child1')
        child2 = Tree('child2')
        root.add_child(child1)
        child1.add_child(child2)
        node, parts = child1._origin_from_path('child2')
        self.assertEqual(child1, node)
        self.assertEqual(['child2'], parts)

    def test_adding_a_node_more_than_once_only_creates_one_instance(self):
        root = Tree('root')
        root.insert_path('a')
        root.insert_path('a')
        self.assertEqual(1, len(root.children))
        self.assertEqual(['a'], [_.value for _ in root.children])

    def test_get_root(self):
        root = Tree('root')
        child = Tree('a')
        root.add_child(child)
        found = child.get_root()
        self.assertEqual(found, root)

    def test_get_root_returns_self_if_starting_at_root(self):
        root = Tree('root')
        found = root.get_root()
        self.assertEqual(found, root)

    def test_find_node_with_absolute_path(self):
        root = Tree('root')
        child = Tree('a')
        root.add_child(child)
        node = root.find_path('/root/a')
        self.assertEqual(node, child)

    def test_find_node_with_absolute_path_returns_None_if_node_does_not_exist(self):
        root = Tree('root')
        child = Tree('a')
        root.add_child(child)
        node = root.find_path('/root/b')
        self.assertIsNone(node)
        node = root.find_path('/b')
        self.assertIsNone(node)

    def test_find_nested_node_with_absoulte_path(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        b = Tree('b')
        a.add_child(b)
        node = root.find_path('/root/a/b')
        self.assertEqual(node, b)

    def test_find_node_with_relative_path(self):
        root = Tree('root')
        child = Tree('a')
        root.add_child(child)
        node = root.find_path('a')
        self.assertEqual(node, child)

    def test_find_node_with_relative_path_returns_None_if_node_does_not_exist(self):
        root = Tree('root')
        child = Tree('a')
        root.add_child(child)
        node = root.find_path('b')
        self.assertIsNone(node)
        node = root.find_path('/b')
        self.assertIsNone(node)

    def test_find_nested_node_with_relative_path(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        b = Tree('b')
        a.add_child(b)
        node = root.find_path('a/b')
        self.assertEqual(node, b)

    def test_find_with_just_a_slash_returns_root_node(self):
        root = Tree('root')
        node = root.find_path('/')
        self.assertEqual(node, root)

    def test_find_with_just_a_slash_returns_root_node_from_a_nested_path(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        b = Tree('b')
        a.add_child(b)
        node = b.find_path('/')
        self.assertEqual(node, root)

    def test_find_with_absolute_path_with_root_node_is_defaulted_slash(self):
        root = Tree(root=True)
        a = Tree('a')
        root.add_child(a)
        b = Tree('b')
        a.add_child(b)
        node = b.find_path('/a/b')
        self.assertEqual(node, b)

    def test_get_ancestors(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        ancestors = list(a.get_ancestors())
        self.assertEqual(ancestors, [root])

    def test_get_ancestors_on_nested_path(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        b = Tree('b')
        a.add_child(b)
        ancestors = list(b.get_ancestors())
        self.assertEqual(ancestors, [a, root])

    def test_get_path_string(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        path = a.get_path()
        self.assertEqual(path, '/root/a')

    def test_get_path_string_on_nested_path(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        b = Tree('b')
        a.add_child(b)
        path = b.get_path()
        self.assertEqual(path, '/root/a/b')

    def test_root_node_has_path_of_forward_slash_plus_value(self):
        root = Tree('root')
        path = root.get_path()
        self.assertEqual(path, '/root')

    def test_get_path_when_root_node_has_value_of_slash_doesnt_show_double_slash(self):
        root = Tree(root=True)
        path = root.get_path()
        self.assertEqual(path, '/')

    def test_if_node_is_marked_as_root_and_no_value_passed_set_val_to_slash(self):
        root = Tree(root=True)
        self.assertEqual(root.value, '/')

    def test_if_node_is_marked_as_root_and_value_passed_set_val_to_passed(self):
        root = Tree('root', root=True)
        self.assertEqual(root.value, 'root')

    def test_if_node_is_not_marked_as_root_and_no_value_passed_set_val_to_None(self):
        root = Tree()
        self.assertIsNone(root.value)

    def test_search(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        results = root.search('a')
        self.assertEqual(results, [a])

    def test_search_returns_empty_list_if_no_finds(self):
        root = Tree('root')
        a = Tree('a')
        root.add_child(a)
        results = root.search('nope')
        self.assertEqual(results, [])

    def test_search_returns_multiple_nodes_if_match_search_target(self):
        root = Tree('root')
        a1 = Tree('a')
        root.add_child(a1)
        a2 = Tree('a')
        root.add_child(a2)
        results = root.search('a')
        self.assertEqual(results, [a1, a2])

    def test_search_returns_multiple_nodes_even_if_at_different_parts_of_the_tree(self):
        root = Tree('root')
        a1 = Tree('a')
        root.add_child(a1)
        b = Tree('b')
        a1.add_child(b)
        a2 = Tree('a')
        b.add_child(a2)
        results = root.search('a')
        self.assertEqual(results, [a1, a2])

    def test_search_finds_all_nodes_whose_value_contains_seach_string(self):
        root = Tree('root')
        a1 = Tree('abc')
        root.add_child(a1)
        b = Tree('b')
        a1.add_child(b)
        a2 = Tree('xyzabc')
        b.add_child(a2)
        results = root.search('abc')
        self.assertEqual(results, [a1, a2])

    def test_search_finds_only_nodes_with_exact_match_if_exact_param_set_to_true(self):
        root = Tree('root')
        a1 = Tree('abc')
        root.add_child(a1)
        b = Tree('b')
        a1.add_child(b)
        a2 = Tree('xyzabc')
        b.add_child(a2)
        results = root.search('abc', exact=True)
        self.assertEqual(results, [a1])

    def test_search_finds_only_nodes_relative_to_current_node_if_relative_set_to_true(self):
        root = Tree('root')
        a1 = Tree('abc')
        root.add_child(a1)
        b = Tree('b')
        a1.add_child(b)
        a2 = Tree('xyzabc')
        b.add_child(a2)
        results = b.search('abc', relative=True)
        self.assertEqual(results, [a2])
