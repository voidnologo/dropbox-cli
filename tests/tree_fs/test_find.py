import argparse
from .base import BaseCommandTest


class FindCommandTests(BaseCommandTest):

    def test_find(self):
        nodes = self.main._find(self.inp(t='n2'))
        self.assertEqual(nodes, [self.node2])

    def test_find_multiple_items_in_a_tree(self):
        a1 = self._create_node('a', self.node1, {})
        a2 = self._create_node('a', self.node5, {})
        nodes = self.main._find(self.inp(t='a'))
        self.assertEqual(nodes, [a1, a2])

    def test_find_all_items_that_contain_search_term(self):
        a1 = self._create_node('abc', self.node1, {})
        a2 = self._create_node('xyzabcqrs', self.node5, {})
        nodes = self.main._find(self.inp(t='abc'))
        self.assertCountEqual(nodes, [a1, a2])

    def test_find_only_items_that_match_exactly_if_e_flag_passed(self):
        a = self._create_node('abc', self.node1, {})
        self._create_node('xyzabcqrs', self.node5, {})
        nodes = self.main._find(self.inp(t='abc', e=True))
        self.assertCountEqual(nodes, [a])

    def test_find_only_items_relative_to_current_node_if_r_flag_passed(self):
        self.main.current_node = self.node2
        self._create_node('abc', self.node1, {})
        a = self._create_node('xyzabcqrs', self.node5, {})
        nodes = self.main._find(self.inp(t='abc', r=True))
        self.assertCountEqual(nodes, [a])

    def test_find_for_terms_with_space_in_them_finds_whole_term(self):
        a1 = self._create_node('ab cd', self.node1, {})
        self._create_node('abother', self.node1, {})
        self._create_node('xyab nope', self.node1, {})
        nodes = self.main._find(self.inp(t='ab cd'))
        self.assertCountEqual(nodes, [a1])

    def test_find_can_use_multiple_switches(self):
        self.main.current_node = self.node2
        self._create_node('abc', self.node1, {})
        a = self._create_node('abc', self.node5, {})
        self._create_node('xyzabcqrs', self.node5, {})
        nodes = self.main._find(self.inp(r=True, e=True, t='abc'))
        self.assertCountEqual(nodes, [a])

    def inp(self, t=None, r=False, e=False):
        target = t.split(' ')
        return argparse.Namespace(target=target, relative=r, exact=e)

