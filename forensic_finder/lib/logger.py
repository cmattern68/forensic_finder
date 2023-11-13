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
        error_handler = logging.StreamHandler(sys.stdout)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self._root.addHandler(debug_handler)
        self._root.addHandler(error_handler)
