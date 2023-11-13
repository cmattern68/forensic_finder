import logging
from config import Configuration
from finder import Finder
from lib.exceptions import PhotorecFinderFilterException


def main():
    try:
        config = Configuration()
        config.parse_arguments()
        finder = Finder(config.config)
        finder.prepare()
        finder.run()
        exit(0)
    except PhotorecFinderFilterException as expt:
        logging.error(expt)
        exit(1)


if __name__ == "__main__":
    main()
