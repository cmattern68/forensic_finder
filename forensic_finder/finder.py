import logging
import math

from multiprocessing import Pool
from forensic_finder.schema import ProcessParamSchema
from forensic_finder.lib.utils import chunks
from forensic_finder.lib.folder import Folder
from forensic_finder.lib.exceptions import FinderException
from forensic_finder.finder_process import FinderProcess
from forensic_finder.config import ConfigurationModel


class Finder:

    _folders_pool = []
    _folders_pool_size = 1

    def __init__(self, config: ConfigurationModel):
        self._config = config

    def prepare(self):
        if not Folder.exist(self._config.source_path):
            raise FinderException(f"{self._config.source_path} does not exists.")
        if self._config.dest_path is not None:
            if Folder.exist(self._config.dest_path):
                if input(f"{self._config.dest_path} already exists, do you want "
                         f"to delete it's content ? If not, folders and files "
                         f"with the same name will be rewritten. (Y/n): "
                         f"").lower() == 'y':
                    Folder.delete(self._config.dest_path)
                    Folder.create(self._config.dest_path)
                    logging.info(f"{self._config.dest_path} folder purged.")
            else:
                Folder.create(self._config.dest_path)
                logging.info(f"{self._config.dest_path} folder created.")
        folders = Folder.fetch_sub_folders(self._config.source_path)
        if len(folders) == 0:
            raise FinderException(f"{self._config.source_path} is empty.")
        folders_len = math.ceil(len(folders) / 100)
        folders_pool_size = folders_len if 1 <= folders_len <= self._config.max_process_pool else 1
        folders_pool = list(
            chunks(folders, math.ceil(len(folders) / folders_pool_size))
        )
        for folders in folders_pool:
            self._folders_pool.append(
                ProcessParamSchema(
                    folders=folders,
                    config=self._config
                )
            )
        self._folders_pool_size = len(self._folders_pool)
        logging.info(f"Split all folders into a pool of {str(self._folders_pool_size)} chunks.")

    def run(self):
        logging.info(f"Filtering will run in {str(self._folders_pool_size)} process.")
        with Pool(self._folders_pool_size) as p_pool:
            p_pool.map((FinderProcess()).run, self._folders_pool)
        logging.info(f"All filtering processes have finished")
