import argparse

import authenticate
from dropbox_cli import DropboxCLI
from utils import DropboxUtils
from tree import PathTree
from tree_fs import TreeFS


def cmd_line_options():
    parser = argparse.ArgumentParser(prog='Dropbox-CLI')
    parser.add_argument(
        '-f', '--file',
        dest='input_file',
        help='File containing file paths to initialize tree with'
    )
    parser.add_argument(
        '-t', '--token',
        default=None,
        dest='dropbox_token',
        help='Dropbox oauth token'
    )
    args = parser.parse_args()
    return args


def init_tree_from_dropbox_account(token=None):
    if token is None:
        token = authenticate.get_user_creds()
    dbutil = DropboxUtils(token=token)
    tree = dbutil.get_tree()
    return tree, token


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
        TreeFS(tree).cmdloop()
    else:
        tree, token = init_tree_from_dropbox_account(args.dropbox_token)
        DropboxCLI(tree, token=token).cmdloop()
