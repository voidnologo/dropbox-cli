import cmd
from itertools import zip_longest
import shlex
import shutil
import textwrap

from exceptions import InvalidPath
from utils import DropboxUtils, Parser, set_docstring_from_parser
from tree import PathTree


class TreeFSParsers:

    @classmethod
    def _find_parser(cls):
        parser = Parser(prog='find')
        parser.add_argument(
            '-e', '--exact',
            action='store_true',
            default=False,
            help='Do an exact string match'
        )
        parser.add_argument(
            '-r', '--relative',
            action='store_true',
            default=False,
            help='Search relative to current path'
        )
        parser.add_argument(
            'target',
            nargs='*',
            help='Target to search for'
        )
        return parser


class TreeFS(cmd.Cmd):
    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def __init__(self, tree, *args, **kwargs):
        self.tree = tree
        self.current_node = self.tree
        super().__init__(*args, **kwargs)

    @property
    def prompt(self):
        return '[{}] --> '.format(self.current_node.get_path())

    def fprint(self, line):
        prefix = ' ' * 4
        print(textwrap.indent(line, prefix))

    def do_tree(self, args):
        """
        Pretty print tree.

        --> tree [style]

        Draw Styles:
            'ascii'    : plain ascii
            'ascii-ex' : line drawing
            'ascii-exr': line drawing, rounded corners
            'ascii-em' : emphasis line drawing
            'ascii-emv': vertical lines emphasized line drawing
            'ascii-emh': horizontal lines emphasized line drawing
        """
        default_style = 'ascii-ex'
        line_type = args if args in PathTree.DRAW_TYPE.keys() else default_style
        self.current_node.formated_print(line_type=line_type)

    def do_ls(self, args):
        for line in self._ls():
            self.fprint(line)

    def _ls(self):
        items = []
        for child in self.current_node.children:
            ind = '/' if child.meta.get('type') == 'folder' else ''
            items.append('{}{}'.format(child.value, ind))
        if items:
            items.sort()
            yield from self._column_format(items)  # flake8: noqa

    def _column_format(self, items):
        size = max(len(_) for _ in items) + 3
        cols = shutil.get_terminal_size().columns // size
        entry = '{{:<{size}}}'.format(size=size)
        for row in zip_longest(*[iter(items)] * cols, fillvalue=''):
            yield (entry * cols).format(*row)

    def do_cd(self, args):
        try:
            self._cd(args)
        except InvalidPath as e:
            self.fprint(str(e))

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


    @set_docstring_from_parser(TreeFSParsers._find_parser)
    def do_find(self, args):
        parser = TreeFSParsers._find_parser()
        args = parser.parse_args(shlex.split(args, posix=True))
        if not args.target:
            return
        try:
            found = self._find(args)
        except ParserError as e:
            print(e)
            return
        if found:
            for line in sorted(_.get_path() for _ in found):
                self.fprint(line)
        else:
            self.fprint('No search results found')

    def _find(self, args):
        target = ' '.join(args.target)
        return self.current_node.search(target, exact=args.exact, relative=args.relative)

    def do_quit(self, args):
        return True

    def do_exit(self, args):
        return True
