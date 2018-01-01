from contextlib import redirect_stdout
from io import StringIO
import textwrap
from unittest import TestCase

from tree import PathTree as Tree


class TreeDisplayTests(TestCase):

    def setUp(self):
        self.tree = Tree(root=True)
        self.tree.insert_path('/a/b/c/d')
        self.tree.insert_path('/a/b/f')
        self.tree.insert_path('/a/b/f/g')
        self.tree.insert_path('/a/b/f/i')
        self.tree.insert_path('/a/b/f/j')
        self.tree.insert_path('/a/h')

    def test_display_tree(self):
        root = Tree(root=True)
        root.insert_path('/a')
        expected = textwrap.dedent('''
        /
            a
        ''').lstrip()
        self.assertEqual(root.display(), expected)

    def test_formatted_print_ascii(self):
        expected = textwrap.dedent('''
        /
        .- a
           |- b
           |  |- c
           |  |  .- d
           |  .- f
           |     |- g
           |     |- i
           |     .- j
           .- h
        ''').lstrip()
        out = StringIO()
        with redirect_stdout(out):
            self.tree.formated_print(line_type='ascii')
        self.assertEqual(expected, out.getvalue())

    def test_formatted_print_ascii_ex(self):
        expected = textwrap.dedent('''
        /
        └─ a
           ├─ b
           │  ├─ c
           │  │  └─ d
           │  └─ f
           │     ├─ g
           │     ├─ i
           │     └─ j
           └─ h
        ''').lstrip()
        out = StringIO()
        with redirect_stdout(out):
            self.tree.formated_print(line_type='ascii-ex')
        self.assertEqual(expected, out.getvalue())

    def test_formatted_print_ascii_exr(self):
        expected = textwrap.dedent('''
        /
        ╰─ a
           ├─ b
           │  ├─ c
           │  │  ╰─ d
           │  ╰─ f
           │     ├─ g
           │     ├─ i
           │     ╰─ j
           ╰─ h
        ''').lstrip()
        out = StringIO()
        with redirect_stdout(out):
            self.tree.formated_print(line_type='ascii-exr')
        self.assertEqual(expected, out.getvalue())

    def test_formatted_print_ascii_em(self):
        expected = textwrap.dedent('''
        /
        ╚═ a
           ╠═ b
           ║  ╠═ c
           ║  ║  ╚═ d
           ║  ╚═ f
           ║     ╠═ g
           ║     ╠═ i
           ║     ╚═ j
           ╚═ h
        ''').lstrip()
        out = StringIO()
        with redirect_stdout(out):
            self.tree.formated_print(line_type='ascii-em')
        self.assertEqual(expected, out.getvalue())

    def test_formatted_print_ascii_emv(self):
        expected = textwrap.dedent('''
        /
        ╙─ a
           ╟─ b
           ║  ╟─ c
           ║  ║  ╙─ d
           ║  ╙─ f
           ║     ╟─ g
           ║     ╟─ i
           ║     ╙─ j
           ╙─ h
        ''').lstrip()
        out = StringIO()
        with redirect_stdout(out):
            self.tree.formated_print(line_type='ascii-emv')
        self.assertEqual(expected, out.getvalue())

    def test_formatted_print_ascii_emh(self):
        expected = textwrap.dedent('''
        /
        ╘═ a
           ╞═ b
           │  ╞═ c
           │  │  ╘═ d
           │  ╘═ f
           │     ╞═ g
           │     ╞═ i
           │     ╘═ j
           ╘═ h
        ''').lstrip()
        out = StringIO()
        with redirect_stdout(out):
            self.tree.formated_print(line_type='ascii-emh')
        self.assertEqual(expected, out.getvalue())
