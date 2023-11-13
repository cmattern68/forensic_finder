class PhotorecFinderFilterException(Exception):
    """
    Main class for all program related exceptions
    """
    pass


class ConfigurationException(PhotorecFinderFilterException):
    """
    All exception that occurred within configuration scope
    """
    pass


class FinderException(PhotorecFinderFilterException):
    """
    All exception that occurred within finder scope
    """
    pass
