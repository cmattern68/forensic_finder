class ForensicFinderException(Exception):
    """
    Main class for all program related exceptions
    """
    pass


class ConfigurationException(ForensicFinderException):
    """
    All exception that occurred within configuration scope
    """
    pass


class FinderException(ForensicFinderException):
    """
    All exception that occurred within finder scope
    """
    pass


class CorruptedFile(ForensicFinderException):
    """
    Corrupted File
    """
    pass
