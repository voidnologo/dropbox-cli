import dropbox
import json

import authenticate


separator = '=' * 100 + '\n'


token = authenticate.get_user_creds()
client = dropbox.Dropbox(token)

# print(client.users_get_current_account())
# print('=' * 100 + '\n')


def do_process(delta_response):
    return (delta_response is None) or delta_response.has_more


def get_changes(cursor):
    if cursor is None:
        return client.files_list_folder('', recursive=True)
    return client.files_list_folder_continue(cursor)


def get_cursor(delta_response):
    if delta_response:
        return delta_response.cursor
    return None


def get_all_files():
    delta_response = None
    while do_process(delta_response):
        cursor = get_cursor(delta_response)
        delta_response = get_changes(cursor)
        yield delta_response


sources = []
for response in get_all_files():
    for entry in response.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            sources.append(entry.path_display)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def prepare_source(source):
    elements = source.split('/')
    return elements, elements.pop()


def add_key(elements, file_name):
    result = dict()
    if len(elements) > 1:
        result[elements[0]] = add_key(elements[1:], file_name)
    else:
        result[elements[0]] = {file_name: 'file'}
    return result


def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], int) and isinstance(b[key], int):
                a[key] += b[key]
            else:
                print('a>{}<     b>{}<    path>{}<     key>{}<'.format(a, b, path, key))
                raise Exception('Conflict at {}'.format('.'.join(path + [str(key)])))
        else:
            a[key] = b[key]
    return a


result = dict()
for source in sources:
    result = merge(result, add_key(*prepare_source(source)))

# print(json.dumps(result, indent=4, sort_keys=True))


import asciitree

tr = asciitree.LeftAligned()
print(tr(result['']))
