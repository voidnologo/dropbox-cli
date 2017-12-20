import cmd
from itertools import islice, chain, repeat
import shutil

import authenticate
from dropbox_utils import DropboxUtils
from tree import PathTree


class MainLoop(cmd.Cmd):
    welcome = 'Dropbox-CLI'
    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def preloop(self):
        print(self.welcome)
        self.initialize()

    def initialize(self):
        token = authenticate.get_user_creds()
        dbutil = DropboxUtils(token=token)
        self.tree = dbutil.get_tree()
        self.current_node = self.tree

    @property
    def prompt(self):
        return '[{}] --> '.format(self.current_node.get_path())

    def do_tree(self, args):
        """
        Pretty print tree.
        Draw Types:
            'ascii': plain ascii
            'ascii-ex': line drawing
            'ascii-exr': line drawing, rounded corners
            'ascii-em': emphasis line drawing
            'ascii-emv': vertical lines emphasized line drawing
            'ascii-emh': horizontal lines emphasized line drawing
        """
        default_style = 'ascii-ex'
        line_type = args if args in PathTree.DRAW_TYPE.keys() else default_style
        self.current_node.formated_print(line_type=line_type)

    def do_ls(self, args):
        dirs = []
        leafs = []
        for child in self.current_node.children:
            if child.meta.get('type') == 'folder':
                dirs.append('{}/'.format(child.value))
            else:
                leafs.append(child.value)
        words = sorted(dirs + leafs)
        if words:
            width = shutil.get_terminal_size().columns
            biggest = max(len(_) for _ in words)
            size = biggest + 3
            cols = width // size
            outs = '{{:<{size}}}'.format(size=size)
            padding = ''
            w = chain(iter(words), repeat(padding))
            x = iter(lambda: tuple(islice(w, cols)), (padding,) * cols)
            for row in list(x):
                print((outs * cols).format(*row))

    def do_cd(self, args):
        next = args.strip()
        if next == '..':
            if self.current_node.parent:
                new_node = self.current_node.parent
                self.current_node = new_node
            else:
                return
        else:
            new_node = self.current_node.get_child(next)
            if new_node and new_node.meta.get('type') == 'folder':
                self.current_node = new_node
            else:
                print('Invalid path')


if __name__ == "__main__":
    MainLoop().cmdloop()
