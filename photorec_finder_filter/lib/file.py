import os


class File:

    @staticmethod
    def exist(path: str):
        return os.path.exists(path)

    @staticmethod
    def readline(path: str):
        with open(path, 'rt') as file:
            return file.read().splitlines()
