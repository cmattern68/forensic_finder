import logging
import os
from rich import print
from forensic_finder.lib.file import File
from forensic_finder.config import ConfigurationModel
from forensic_finder.schema import Exif
from PIL.ExifTags import TAGS
from PIL import Image, UnidentifiedImageError
from imghdr import what


class FileManipulator:
    _stat = None
    _exif = None

    def __init__(self, path: str, config: ConfigurationModel):
        self._path = path
        self._file_name = os.path.split(path)[1]
        self._ext = os.path.splitext(self._file_name)[1][1:]
        self._config = config

    @property
    def ext(self) -> str:
        return self._ext

    def exist(self) -> bool:
        return File.exist(self._path)

    def _get_exif(self) -> None:
        image = None
        try:
            image = Image.open(self._path)
            image.verify()
            exif = image.getexif()
            if len(exif) > 0:
                exif_table = {}
                for k, v in exif.items():
                    tag = TAGS.get(k)
                    if tag is not None:
                        exif_table[tag] = v
                self._exif = Exif(**exif_table)
        except UnidentifiedImageError as e:
            logging.error(f"Unidentified image {self._path}. Probably corrupted.")
        except Exception as e:
            logging.error(f"Unable to retrieve exif data from {self._path}. Probably corrupted.")
        if image is not None:
            image.close()

    def get_file_metadata(self) -> None:
        if what(self._path) is not None:
            self._get_exif()
        self._stat = os.stat(self._path)

    def is_movable(self) -> bool:
        return True

    def move(self) -> None:
        return
