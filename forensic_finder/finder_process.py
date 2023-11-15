import os
import logging
from rich import print
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

        logging.info(f"Run process on pid {self._pid}.")

        if self._folders is None:
            return self._results
        for path in self._folders:
            folder = FolderManipulator(path, self._config)
            if folder.exist():
                files = folder.get_files_by_ext()
                if len(files) == 0:
                    logging.info(f"Folder {folder.path} does not contain targeted files extensions. Skipping.")
                    continue
                i = 0
                for file in files:
                    file.get_file_metadata()
                    if file.is_movable():
                        file.move()
        logging.info(f"Process on pid {self._pid} finished.")

