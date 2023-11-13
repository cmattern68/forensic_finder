import logging
import math

from rich import print
from lib.utils import chunks
from lib.folder import Folder
from lib.exceptions import FinderException
from config import ConfigurationModel


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
                    logging.debug(f"{self._config.dest_path} folder purged.")
            else:
                Folder.create(self._config.dest_path)
                logging.debug(f"{self._config.dest_path} folder created.")
        folders = Folder.fetch_sub_folders(self._config.source_path)
        if len(folders) == 0:
            raise FinderException(f"{self._config.source_path} is empty.")
        folders_len = math.ceil(len(folders) / 100)
        folders_pool_size = folders_len if 1 <= folders_len <= self._config.max_process_pool else 1
        self._folders_pool = list(chunks(folders, math.ceil(len(folders) / folders_pool_size)))
        self._folders_pool_size = len(self._folders_pool)
        logging.debug(f"Split all folders into a pool of {str(self._folders_pool_size)} chunks.")

    def run(self):
        logging.debug(f"Filtering will run in {str(self._folders_pool_size)} process.")
