from rich import print
from typing import Optional, List
from argparse import ArgumentParser
from pydantic import BaseModel, Field, ValidationError, validator
from lib.logger import Logger
from lib.exceptions import ConfigurationException
from lib.file import File


class ConfigurationModel(BaseModel):
    source_path: str
    dest_path: Optional[str] = Field(default=None)
    extensions: Optional[List[str]] = Field(default=None)
    verbose: bool = Field(default=False)
    clamav: bool = Field(default=False)
    max_process_pool: int = 10

    @validator('extensions', pre=True)
    def load_ext(cls, path):
        if File.exist(path):
            return File.readline(path)
        raise ValueError("File does not exists")


class Configuration:
    _config: Optional[ConfigurationModel]

    def __init__(self):
        self._root_logger = None
        self._parser = ArgumentParser(
            description="Process all files and folder to retrieve only interesting content."
        )
        self._parser.add_argument(
            "source",
            metavar="<source>",
            help="source folder of findings to be used."
        )
        self._parser.add_argument(
            "--dest",
            metavar="<dest>",
            help="destination folder to be used.",
            required=False,
            dest="dest"
        )
        self._parser.add_argument(
            "--ext",
            metavar="<extension_file>",
            help="file containing all file extensions to be searched by the script (each extension to be separated "
                 "with a line break)",
            required=False,
            dest="ext"
        )
        self._parser.add_argument(
            "--verbose",
            help="Print everything",
            required=False,
            action="store_true",
            dest="verbose"
        )
        self._parser.add_argument(
            "--clamav",
            help="Run clamav analysis on --dest at the end",
            required=False,
            action="store_true",
            dest="clamav"
        )

    @property
    def config(self) -> ConfigurationModel:
        return self._config

    def parse_arguments(self):
        args = self._parser.parse_args()
        try:
            self._config = ConfigurationModel(
                source_path=args.source,
                dest_path=args.dest,
                extensions=args.ext,
                verbose=args.verbose,
                clamav=args.clamav
            )
            self._root_logger = Logger(self._config.verbose)
        except ValidationError as expt:
            raise ConfigurationException(f"Unable to init ConfigurationModel:\n{str(expt)}")
