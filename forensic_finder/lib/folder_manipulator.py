import os
from forensic_finder.lib.folder import Folder
from forensic_finder.lib.file_manipulator import FileManipulator
from forensic_finder.config import ConfigurationModel


class FolderManipulator:

    _files = []

    def __init__(self, path: str, config: ConfigurationModel):
        self._path = path
        self._config = config

    @property
    def path(self):
        return self._path

    def exist(self):
        return Folder.exist(self._path)

    def get_files_by_ext(self):
        for file in os.listdir(self._path):
            if os.path.isfile(os.path.join(self._path, file)):
                file = FileManipulator(f"{self._path}/{file}", self._config)
                if file.ext in self._config.extensions:
                    self._files.append(file)
        return self._files

    def get_folder_size(self):
        return len(self._files)
