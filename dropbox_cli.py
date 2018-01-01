import authenticate
from dropbox_utils import DropboxUtils
from tree_fs import TreeFS


class DropboxCLI(TreeFS):
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


if __name__ == "__main__":
    DropboxCLI().cmdloop()
