import sys
import logging


class Logger:

    def __init__(self, verbose):
        self._root = logging.getLogger()
        self._root.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        debug_handler = logging.StreamHandler(sys.stdout)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        if not verbose:
            debug_handler = logging.NullHandler()
        info_handler = logging.StreamHandler(sys.stdout)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        error_handler = logging.StreamHandler(sys.stdout)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self._root.addHandler(debug_handler)
        self._root.addHandler(info_handler)
        self._root.addHandler(error_handler)
