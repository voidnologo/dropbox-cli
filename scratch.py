
# SOURCE == list of filepaths from dropbox

# def prepare_source(source):
#     elements = source.split('/')
#     return elements, elements.pop()


# def add_key(elements, file_name):
#     result = dict()
#     if len(elements) > 1:
#         result[elements[0]] = add_key(elements[1:], file_name)
#     else:
#         result[elements[0]] = {file_name: 'file'}
#     return result


# def merge(a, b, path=None):
#     if path is None:
#         path = []
#     for key in b:
#         if key in a:
#             if isinstance(a[key], dict) and isinstance(b[key], dict):
#                 merge(a[key], b[key], path + [str(key)])
#             elif isinstance(a[key], int) and isinstance(b[key], int):
#                 a[key] += b[key]
#             else:
#                 print('a>{}<     b>{}<    path>{}<     key>{}<'.format(a, b, path, key))
#                 raise Exception('Conflict at {}'.format('.'.join(path + [str(key)])))
#         else:
#             a[key] = b[key]
#     return a


# result = dict()
# for source in sources:
#     result = merge(result, add_key(*prepare_source(source)))

# # print(json.dumps(result, indent=4, sort_keys=True))
