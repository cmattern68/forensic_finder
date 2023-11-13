import os
import shutil


class Folder:

    @staticmethod
    def exist(path: str):
        return os.path.exists(path)

    @staticmethod
    def create(path: str):
        os.mkdir(path, 0o755)

    @staticmethod
    def delete(path: str):
        shutil.rmtree(path)

    @staticmethod
    def fetch_sub_folders(path: str):
        sub_folders = []
        for path, folders, files in os.walk(path):
            sub_folders.append(path)
        return sub_folders
