import os
import logging
from forensic_finder.schema import FinderResult, ProcessParamSchema
from forensic_finder.lib.folder_manipulator import FolderManipulator


class FinderProcess:

    _results = None
    _folders = None
    _config = None
    _pid = None

    def run(self, param: ProcessParamSchema):
        self._results = FinderResult()
        self._pid = os.getpid()
        self._folders = param.folders
        self._config = param.config

        logging.debug(f"Run process on pid {self._pid}.")

        if self._folders is None:
            return self._results
        for path in self._folders:
            folder = FolderManipulator(path, self._config)
            if folder.exist():
                folder_files = folder.get_files_by_ext()
                if len(folder_files) == 0:
                    logging.debug(f"Folder {folder.path} does not contain targeted files extensions. Skipping.")

        logging.debug(f"Process on pid {self._pid} stopping.")

