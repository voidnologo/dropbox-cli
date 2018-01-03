import argparse

import authenticate
from dropbox_utils import DropboxUtils
from tree import PathTree
from tree_fs import TreeFS


ENDC = '\033[0m'
BOLD = '\033[1m'
FG_BOLD_YELLOW = '\033[93m'
FG_CYAN = '\033[36m'


class DropboxCLI(TreeFS):
    welcome = 'Dropbox-CLI'
    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def preloop(self):
        print(self.welcome)

    @property
    def prompt(self):
        return '{}[{}] --> {}'.format(FG_BOLD_YELLOW, self.current_node.get_path(), ENDC)

    # def _ls(self):
    #     items = []
    #     for child in self.current_node.children:
              # TODO: color code adds 8 characters to item when calculating column, but since they are color codes, not displayed
              #       by the terminal causing the line alignment to be off
    #         ind, color, endc = ('/', FG_CYAN, ENDC) if child.meta.get('type') == 'folder' else ('', '', '')
    #         items.append('{}{}{}{}'.format(color, child.value, ind, endc))
    #     if items:
    #         items.sort()
    #         yield from self._column_format(items)  # flake8: noqa


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
