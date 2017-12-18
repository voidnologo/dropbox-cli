import itertools


class PathTree:

    def __init__(self, val=None):
        self.value = val or '/'
        self.children = None
        self.parent = None

    def __str__(self):
        return self.value

    def __repr__(self):
        return "PathTree('{}')".format(self.value)

    def __iter__(self):
        if self.children is None:
            raise StopIteration
        yield from self.children

    def __eq__(self, comp):
        return self.value == comp

    def add_child(self, node):
        node.parent = self
        if self.children:
            self.children.append(node)
        else:
            self.children = [node]

    def get_child(self, identifier):
        if self.children is None:
            return None
        return next((child for child in self.children if child.value == identifier), None)

    def _get_path_parts(self, node_path):
        parts = node_path.split('/')
        return parts[1:] if node_path.startswith('/') else parts

    def insert_path(self, node_path):
        parts = self._get_path_parts(node_path)
        self._insert_node(parts)

    def _insert_node(self, path):
        val = path.pop(0)
        contains = self.get_child(val)
        if contains:
            if len(path) > 0:
                contains._insert_node(path)
        else:
            child = PathTree(val)
            self.add_child(child)
            if len(path) > 0:
                child._insert_node(path)

    def find_path(self, node_path):
        parts = self._get_path_parts(node_path)
        return self._find_node(parts)

    def _find_node(self, path):
        val = path.pop(0)
        contains = self.get_child(val)
        if len(path) > 0:
            return contains._find_node(path)
        return contains

    def get_ancestors(self):
        if self.parent is not None:
            yield self.parent
            yield from self.parent.get_ancestors()

    def get_path(self):
        return '/'.join(reversed([self.value] + [_.value for _ in self.get_ancestors()]))[1:]
