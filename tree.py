class PathTree:

    def __init__(self, val=None):
        self.value = val or '/'
        self.children = None
        self.parent = None

    def __str__(self):
        return self.value

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

    def insert_path(self, node_path):
        parts = node_path.split('/')
        parts = parts[1:] if node_path.startswith('/') else parts
        self._insert_node(parts)

    def _insert_node(self, path):
        val = path.pop(0)
        contains = self.get_child(val)
        if contains and len(path) > 0:
            contains._insert_node(path)
        else:
            child = PathTree(val)
            self.add_child(child)
            if len(path) > 0:
                child._insert_node(path)
