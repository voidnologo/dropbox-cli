class InvalidPath(Exception):

    def __init__(self, file_path):
        message = 'Invalid Path: {}'.format(file_path)
        super().__init__(message)
