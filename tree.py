class Node:

    def __init__(self, val):
        self.value = val
        self.children = None
        self.parent = None

    def add_child(self, node):
        node.parent = self
        if self.children:
            self.children.append(node)
        else:
            self.children = [node]

    def __iter__(self):
        if self.children is None:
            raise StopIteration
        yield from self.children
