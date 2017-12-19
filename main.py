import cmd
# import textwrap

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

    def do_print(self, args):
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
            if child.children:
                dirs.append('{}/'.format(child.value))
            else:
                leafs.append(child.value)
        print(sorted(dirs))
        print(sorted(leafs))

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
            if new_node and new_node.children:
                self.current_node = new_node
            else:
                print('Invalid path')


if __name__ == "__main__":
    MainLoop().cmdloop()
