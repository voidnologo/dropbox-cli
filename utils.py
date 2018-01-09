import argparse
from contextlib import redirect_stdout
from io import StringIO
import dropbox

from tree import PathTree


class ParserError(Exception):
    pass


class Parser(argparse.ArgumentParser):

    def error(self, message):
        raise ParserError(message)

    def exit(self, *args, **kwargs):
        pass


class cached_property:
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """  # noqa

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class DropboxUtils:

    def __init__(self, token=None, client=None):
        self.client = client or dropbox.Dropbox(token)

    def do_process(self, delta_response):
        return (delta_response is None) or delta_response.has_more

    def get_changes(self, cursor):
        if cursor is None:
            return self.client.files_list_folder('', recursive=True)
        return self.client.files_list_folder_continue(cursor)

    def get_cursor(self, delta_response):
        if delta_response:
            return delta_response.cursor
        return None

    def get_all_files(self):
        delta_response = None
        while self.do_process(delta_response):
            cursor = self.get_cursor(delta_response)
            delta_response = self.get_changes(cursor)
            yield delta_response

    def get_tree(self):
        tree = PathTree(root=True)
        for response in self.contents:
            for entry in response.entries:
                tree.insert_path(entry.path_display)
                node = tree.find_path(entry.path_display)
                if isinstance(entry, dropbox.files.FileMetadata):
                    node.meta = {
                        'type': 'file',
                        'id': entry.id,
                        'modified': entry.server_modified,
                        'size': entry.size
                    }
                if isinstance(entry, dropbox.files.FolderMetadata):
                    node.meta = {
                        'type': 'folder',
                        'id': entry.id
                    }
        return tree

    @cached_property
    def contents(self):
        return list(self.get_all_files())


def set_docstring_from_parser(parser):
    def wrapper(func):
        out = StringIO()
        with redirect_stdout(out):
            parser().print_help()
        func.__doc__ = out.getvalue()
        return func
    return wrapper
