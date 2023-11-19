import os
import logging
from rich import print
from forensic_finder.schema import FinderResult, ProcessParamSchema, RecoveringStatus, RecoveringSchema
from forensic_finder.lib.folder_manipulator import FolderManipulator
from forensic_finder.lib.exceptions import CorruptedFile


class FinderProcess:

    _results = None
    _folders = None
    _config = None
    _pid = None

    def run(self, param: ProcessParamSchema) -> FinderResult:
        self._results = FinderResult(
            total=RecoveringSchema()
        )
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
                    file_status = RecoveringStatus.IGNORED
                    try:
                        file.get_file_metadata()
                        if file.is_movable():
                            file_status = file.move()
                    except CorruptedFile:
                        file_status = RecoveringStatus.CORRUPTED
                    self._results.add_result(file.ext, file_status)
        if self._config.clamav:
            self._results.total.nb_files_infected = 0
            for key, detail in self._results.details.items():
                detail.nb_files_infected = 0
        logging.info(f"Process on pid {self._pid} finished.")
        return self._results

