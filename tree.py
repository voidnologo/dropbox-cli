class PathTree:

    DRAW_TYPE = {
        'ascii': ('|', '|- ', '.- '),
        'ascii-ex': ('\u2502', '\u251c\u2500 ', '\u2514\u2500 '),
        'ascii-exr': ('\u2502', '\u251c\u2500 ', '\u2570\u2500 '),
        'ascii-em': ('\u2551', '\u2560\u2550 ', '\u255a\u2550 '),
        'ascii-emv': ('\u2551', '\u255f\u2500 ', '\u2559\u2500 '),
        'ascii-emh': ('\u2502', '\u255e\u2550 ', '\u2558\u2550 '),
    }

    def __init__(self, val=None):
        self.value = val or '/'
        self.children = []
        self.parent = None
        self.meta = dict()

    def __str__(self):
        return self.value

    def __repr__(self):
        return "PathTree('{}')".format(self.value)

    def __iter__(self):
        if self.children is None:
            raise StopIteration
        yield from self.children  # flake8: noqa

    def __eq__(self, comp):
        return self.value == comp

    def add_child(self, node):
        node.parent = self
        if self.children:
            self.children.append(node)
        else:
            self.children = [node]

    def get_child(self, identifier):
        if not self.children:
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

    def display(self, level=0):
        out = '    ' * level + self.value + '\n'
        if self.children:
            for child in self.children:
                out += child.display(level + 1)
        return out

# ====================================================================================================

    def formated_print(self, node=None, line_type='ascii-ex', func=print):
        dt = self.DRAW_TYPE[line_type]
        node = self if node is None else node
        for pre, node in self.__draw_tree(node, dt, []):
            func('{0}{1}'.format(pre, node.value))

    def __draw_tree(self, node, draw_type, is_last, level=0):
        dt_vline, dt_line_box, dt_line_corner = draw_type

        if node.parent is None or level == 0:
            yield '', node
        else:
            leading = ''.join([dt_vline + ' ' * 2 if not x else ' ' * 3 for x in is_last[0:-1]])
            node_marker = dt_line_corner if is_last[-1] else dt_line_box
            yield leading + node_marker, node

        level += 1
        if node.children:
            idxlast = len(node.children)-1
            for idx, child in enumerate(node.children):
                is_last.append(idx == idxlast)
                for item in self.__draw_tree(child, draw_type, is_last, level):
                    yield item
                is_last.pop()
