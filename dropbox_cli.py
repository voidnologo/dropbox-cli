import argparse

import authenticate
from dropbox_utils import DropboxUtils
from tree import PathTree
from tree_fs import TreeFS


class DropboxCLI(TreeFS):
    welcome = 'Dropbox-CLI'
    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def preloop(self):
        print(self.welcome)


def cmd_line_options():
    parser = argparse.ArgumentParser(prog='Dropbox-CLI', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.description = """
    Purpose:

    Input: -

    Output:

    Usage:

    Note:
    """
    parser.add_argument(
        '-f', '--file',
        dest='input_file',
        help='File containing file paths to initialize tree with'
    )
    args = parser.parse_args()
    return args


def init_tree_from_dropbox_account():
    token = authenticate.get_user_creds()
    dbutil = DropboxUtils(token=token)
    tree = dbutil.get_tree()
    return tree


def init_tree_from_file(input_file):
    with open(input_file, 'r') as f:
        tree = PathTree(root=True)
        for line in f:
            tree.insert_path(line.strip())
            node = tree.find_path(line.strip())
            node.meta = {
                'type': 'file',
                'id': '',
                'modified': '',
                'size': '',
                'details': 'added from file'
            }
    return tree


if __name__ == "__main__":
    args = cmd_line_options()
    if args.input_file:
        tree = init_tree_from_file(args.input_file)
    else:
        tree = init_tree_from_dropbox_account()

    DropboxCLI(tree).cmdloop()
