import cmd
from itertools import zip_longest
import shutil

import authenticate
from exceptions import InvalidPath
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
        self.root = dbutil.get_tree()
        self.current_node = self.root

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
        for line in self._ls():
            print(line)

    def _ls(self):
        items = []
        for child in self.current_node.children:
            ind = '/' if child.meta.get('type') == 'folder' else ''
            items.append('{}{}'.format(child.value, ind))
        items.sort()
        if items:
            size = max(len(_) for _ in items) + 3
            cols = shutil.get_terminal_size().columns // size
            entry = '{{:<{size}}}'.format(size=size)
            for row in zip_longest(*[iter(items)] * cols, fillvalue=''):
                yield (entry * cols).format(*row)

    def do_cd(self, args):
        try:
            self._cd(args)
        except InvalidPath as e:
            print('Invalid Path: {}'.format(e))

    def _cd(self, args):
        next_node = args.strip()
        if next_node == '..':
            if self.current_node.parent:
                self.current_node = self.current_node.parent
            return
        node = self.current_node.find_path(next_node)
        if node is None:
            raise InvalidPath(args)
        self.current_node = node
        if node.meta.get('type') == 'file':
            self.current_node = node.parent or node

    def do_quit(self, args):
        return True

    def do_exit(self, args):
        return True


if __name__ == "__main__":
    MainLoop().cmdloop()
