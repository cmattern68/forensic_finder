import os
from forensic_finder.lib.file import File
from forensic_finder.config import ConfigurationModel


class FileManipulator:

    def __init__(self, path: str, config: ConfigurationModel):
        self._path = path
        self._file_name = os.path.split(path)[1]
        self._ext = os.path.splitext(self._file_name)[1][1:]
        self._config = config

    @property
    def ext(self):
        return self._ext

    def exist(self):
        return File.exist(self._path)
